"""Train matched-date Conv3D input-window ablation (3/7/14 days)."""
import csv, json, math, os, random, time
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import yaml
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from models.model_utils import get_model
from training.losses import get_loss

OUT = Path(__file__).resolve().parent / "window_ablation"
OUT.mkdir(exist_ok=True)
DEVICE = torch.device("cuda:0")

class WindowData(Dataset):
    def __init__(self, array, window, target_indices):
        self.array, self.window, self.target_indices = array, window, target_indices
    def __len__(self): return len(self.target_indices)
    def __getitem__(self, i):
        end = int(self.target_indices[i]); start = end - self.window
        x = np.array(self.array[start:end, None], dtype=np.float32, copy=True)
        y = np.array(self.array[end, None], dtype=np.float32, copy=True)
        return torch.from_numpy(x), torch.from_numpy(y)

def metrics(pred, target):
    p, y = pred.ravel(), target.ravel()
    if p.shape != y.shape or not np.isfinite(p).all() or not np.isfinite(y).all(): raise ValueError("Invalid metric arrays")
    return {"rmse_celsius": float(mean_squared_error(y,p)**.5), "mae_celsius": float(mean_absolute_error(y,p)), "r2": float(r2_score(y,p)), "pearson_r": float(np.corrcoef(p,y)[0,1])}

def evaluate(model, loader, mean, std):
    model.eval(); ps=[]; ys=[]
    with torch.no_grad():
        for x,y in loader:
            z=model(x.to(DEVICE)).cpu().numpy(); t=y.numpy()
            ps.append(z[:,0]*std+mean); ys.append(t[:,0]*std+mean)
    return np.concatenate(ps), np.concatenate(ys)

def main():
    torch.manual_seed(42); np.random.seed(42); random.seed(42); torch.cuda.manual_seed_all(42)
    if not torch.cuda.is_available() or "4070" not in torch.cuda.get_device_name(0): raise RuntimeError("RTX 4070 CUDA device unavailable")
    cfg=yaml.safe_load((ROOT/"config.yaml").read_text()); stats=json.loads((ROOT/"data/processed/mean_std.json").read_text())
    mean,std=float(stats["mean"]),float(stats["std"]); loss=get_loss(cfg["training"])
    arrays={s:np.load(ROOT/f"data/processed/{s}.npy",mmap_mode="r") for s in ("train","val","test")}
    ntest=len(arrays["test"]); common=np.arange(14,ntest)
    results=[]
    for window in (3,7,14):
        torch.manual_seed(42); torch.cuda.manual_seed_all(42)
        train=DataLoader(WindowData(arrays["train"],window,np.arange(window,len(arrays["train"]))),batch_size=16,shuffle=True)
        val=DataLoader(WindowData(arrays["val"],window,np.arange(window,len(arrays["val"]))),batch_size=16,shuffle=False)
        test=DataLoader(WindowData(arrays["test"],window,common),batch_size=16,shuffle=False)
        model=get_model({**cfg,"model":{**cfg["model"],"name":"convlstm"}}).to(DEVICE)
        opt=torch.optim.Adam(model.parameters(),lr=cfg["training"]["learning_rate"])
        history=[]; best=float("inf"); best_epoch=0; checkpoint=OUT/f"conv3d_window{window}_best.pth"
        start=time.perf_counter()
        for ep in range(1,51):
            model.train(); tl=[]
            for x,y in train:
                opt.zero_grad(set_to_none=True); pred=model(x.to(DEVICE)); target=y.to(DEVICE); l=loss(pred,target)
                if not torch.isfinite(l): raise FloatingPointError(f"window {window} train loss non-finite epoch {ep}")
                l.backward(); opt.step(); tl.append(l.item())
            model.eval(); vl=[]
            with torch.no_grad():
                for x,y in val:
                    l=loss(model(x.to(DEVICE)),y.to(DEVICE))
                    if not torch.isfinite(l): raise FloatingPointError(f"window {window} validation loss non-finite epoch {ep}")
                    vl.append(l.item())
            v=float(np.mean(vl)); history.append({"epoch":ep,"train_loss":float(np.mean(tl)),"validation_loss":v})
            if v<best:
                best,best_epoch=v,ep; torch.save(model.state_dict(),checkpoint)
            payload={"window_days":window,"status":"running","epochs_completed":ep,"best_epoch":best_epoch,"best_validation_loss":best,"seed":42,"batch_size":16,"loss":"ExtremeWeightedMSE; training-only p95; weight=5","history":history}
            tmp=OUT/f"conv3d_window{window}_history.json.tmp"; tmp.write_text(json.dumps(payload,indent=2)); os.replace(tmp,OUT/f"conv3d_window{window}_history.json")
            print(f"window={window} epoch={ep}/50 train={np.mean(tl):.6f} val={v:.6f}",flush=True)
        model.load_state_dict(torch.load(checkpoint,map_location=DEVICE,weights_only=True))
        p,y=evaluate(model,test,mean,std); result={"window_days":window,"epochs_completed":len(history),"best_epoch":best_epoch,"best_validation_loss":best,"training_seconds":round(time.perf_counter()-start,3),"common_test_dates":"2025-01-15 through 2025-12-31","common_test_samples":len(common),"test":metrics(p,y),"checkpoint":str(checkpoint.relative_to(ROOT)),"history_file":str((OUT/f"conv3d_window{window}_history.json").relative_to(ROOT))}
        results.append(result); payload.update({"status":"complete","result":result}); (OUT/f"conv3d_window{window}_history.json").write_text(json.dumps(payload,indent=2,allow_nan=False))
        print(f"window={window} selected_epoch={best_epoch} common_test={result['test']}",flush=True)
    (OUT/"window_ablation_results.json").write_text(json.dumps({"protocol":{"model":"Conv3D encoder-decoder","epochs_requested":50,"seed":42,"selection":"minimum validation loss","common_test_dates":"2025-01-15 through 2025-12-31","test_used_for_selection":False,"device":torch.cuda.get_device_name(0)},"results":results},indent=2,allow_nan=False))
    with (OUT/"window_ablation_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["window_days","epochs_completed","best_epoch","best_validation_loss","training_seconds","common_test_samples","rmse_celsius","mae_celsius","r2","pearson_r","checkpoint","history_file"]);w.writeheader()
        for r in results:w.writerow({**{k:r[k] for k in ("window_days","epochs_completed","best_epoch","best_validation_loss","training_seconds","common_test_samples","checkpoint","history_file")},**r["test"]})
    print(f"ABLaTION_COMPLETE {OUT}",flush=True)
if __name__=="__main__": main()
