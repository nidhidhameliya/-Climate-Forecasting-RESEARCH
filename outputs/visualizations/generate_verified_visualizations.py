"""Regenerate visualizations from the corrected saved checkpoints and tensors."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
EXPERIMENT = ROOT / "experiments" / "reviewer_final_20261014"
COMPARISON = ROOT / "experiments" / "reviewer_comparison_with_recurrent_convlstm_20261014" / "comparison_results.csv"
sys.path.insert(0, str(ROOT))
from models.convlstm import ConvLSTMModel

STATS = json.loads((ROOT / "data/processed/mean_std.json").read_text(encoding="utf-8"))
MEAN, STD = float(STATS["mean"]), float(STATS["std"])
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.titlesize":10,
                     "axes.labelsize":9,"savefig.dpi":350,"axes.spines.top":False,
                     "axes.spines.right":False,"axes.grid":True,"grid.alpha":.25})


def get_model() -> ConvLSTMModel:
    model=ConvLSTMModel({"model":{"hidden_dim":32}})
    state=torch.load(EXPERIMENT/"convlstm_best.pth",map_location="cpu",weights_only=True)
    model.load_state_dict(state)
    model.to(DEVICE).eval()
    return model


def infer_split(model:ConvLSTMModel,name:str):
    x=np.load(ROOT/f"data/processed/tensors/{name}_X.npy",mmap_mode="r")
    y=np.load(ROOT/f"data/processed/tensors/{name}_y.npy",mmap_mode="r")
    predictions=[]
    with torch.inference_mode():
        for start in range(0,len(x),4):
            xb=torch.from_numpy(np.array(x[start:start+4],copy=True)).to(DEVICE)
            predictions.append(model(xb).cpu().numpy())
    pred=np.concatenate(predictions,axis=0)[:,0]*STD+MEAN
    target=np.array(y,copy=True)[:,0]*STD+MEAN
    previous=np.array(x[:,-1],copy=True)[:,0]*STD+MEAN
    return previous,pred,target


def calc_metrics(pred,target):
    p=pred.ravel();y=target.ravel();e=p-y
    return {"rmse":float(np.sqrt(np.mean(e*e))),"mae":float(np.mean(np.abs(e))),
            "r2":float(1-np.sum(e*e)/np.sum((y-y.mean())**2)),
            "pearson_r":float(np.corrcoef(p,y)[0,1]),"bias":float(np.mean(e))}


def save(fig,name):
    fig.savefig(OUT/f"{name}.png",dpi=350,bbox_inches="tight",facecolor="white")
    plt.close(fig)


def evaluation_plot(split,pred,target,metrics):
    p=pred.ravel();y=target.ravel();e=p-y
    fig,(a,b)=plt.subplots(1,2,figsize=(8.2,3.5),gridspec_kw={"width_ratios":[1.3,1]})
    h=a.hexbin(y,p,gridsize=55,mincnt=1,bins="log",cmap="viridis",linewidths=0)
    lo=min(float(y.min()),float(p.min()));hi=max(float(y.max()),float(p.max()))
    a.plot([lo,hi],[lo,hi],"--",color="#C65353",lw=1.2)
    a.set(xlabel="ERA5 target (°C)",ylabel="Conv3D prediction (°C)",title="Observed vs predicted")
    a.text(.04,.96,(f"RMSE {metrics['rmse']:.3f}°C\nMAE {metrics['mae']:.3f}°C\n"
                    f"R² {metrics['r2']:.4f}\nPearson r {metrics['pearson_r']:.4f}"),
           transform=a.transAxes,va="top",bbox={"facecolor":"white","alpha":.9,"edgecolor":"#cccccc"},fontsize=8)
    cb=fig.colorbar(h,ax=a,fraction=.046,pad=.04);cb.set_label("Count per hexagon (log scale)")
    b.hist(e,bins=70,color="#2878A5",edgecolor="white",linewidth=.2)
    b.axvline(0,color="#C65353",ls="--",lw=1)
    b.axvline(metrics["bias"],color="#E39138",ls=":",lw=1.5,label=f"Mean error {metrics['bias']:.3f}°C")
    b.set(xlabel="Prediction − target (°C)",ylabel="Grid-cell/date count",title="Error distribution")
    b.legend(frameon=False,fontsize=7)
    fig.suptitle(f"Conv3D {split} results · saved selected checkpoint",x=.02,ha="left",fontweight="bold")
    fig.text(.02,.005,"Targets are ERA5 reanalysis. Validation is used for checkpoint selection; test is the held-out 2025 evaluation.",fontsize=7,color="#666666")
    fig.tight_layout(rect=(0,.06,1,.92),w_pad=1.2)
    prefix="val" if split=="Validation" else "test"
    save(fig,f"{prefix}_evaluation")


def prediction_map(split,previous,pred,target):
    daily_rmse=np.sqrt(np.mean((pred-target)**2,axis=(1,2)))
    idx=int(np.argsort(daily_rmse)[len(daily_rmse)//2])
    lat=np.linspace(35,5,121);lon=np.linspace(65,100,141);extent=(65,100,5,35)
    err=np.abs(pred[idx]-target[idx])
    vmin=min(float(previous[idx].min()),float(pred[idx].min()),float(target[idx].min()))
    vmax=max(float(previous[idx].max()),float(pred[idx].max()),float(target[idx].max()))
    fig,axes=plt.subplots(1,4,figsize=(10.2,3.1))
    panels=[(previous[idx],"Previous day"),(target[idx],"ERA5 target"),(pred[idx],"Conv3D prediction")]
    for ax,(grid,title) in zip(axes[:3],panels):
        im=ax.imshow(grid,extent=extent,origin="upper",aspect="auto",cmap="coolwarm",vmin=vmin,vmax=vmax)
        ax.set_title(title,fontweight="bold");ax.set_xlabel("Longitude (°E)");ax.set_xticks([65,80,100]);ax.set_yticks([5,20,35])
    axes[0].set_ylabel("Latitude (°N)")
    imerr=axes[3].imshow(err,extent=extent,origin="upper",aspect="auto",cmap="magma",vmin=0,vmax=max(1,float(np.percentile(err,99))))
    axes[3].set_title("Absolute error",fontweight="bold");axes[3].set_xlabel("Longitude (°E)");axes[3].set_xticks([65,80,100]);axes[3].set_yticks([5,20,35])
    date0=np.datetime64("2024-01-08" if split=="Validation" else "2025-01-08")
    date=date0+np.timedelta64(idx,"D")
    fig.suptitle(f"{split} one-day forecast example · target {date}",x=.02,ha="left",fontweight="bold")
    temp_cax=fig.add_axes([.12,.045,.54,.026])
    fig.colorbar(im,cax=temp_cax,orientation="horizontal",label="Daily maximum temperature (°C)")
    fig.colorbar(imerr,ax=axes[3],fraction=.046,pad=.035,label="Absolute error (°C)")
    fig.subplots_adjust(left=.055,right=.97,bottom=.25,top=.79,wspace=.3)
    prefix="val" if split=="Validation" else "test"
    save(fig,f"{prefix}_prediction_map")


def history_plot():
    fig,ax=plt.subplots(figsize=(7,3.5))
    items=[("convlstm","Conv3D","#2878A5",EXPERIMENT),
           ("cnn_lstm","CNN-LSTM","#4D9A87",EXPERIMENT),
           ("transformer","Transformer","#8064A2",EXPERIMENT),
           ("lstm","LSTM","#E39138",ROOT/"experiments/reviewer_lstm_repaired_20261014"),
           ("recurrent_convlstm","ConvLSTM","#C65353",ROOT/"experiments/reviewer_recurrent_convlstm_20261014")]
    for key,label,color,directory in items:
        data=json.loads((directory/f"{key}_history.json").read_text(encoding="utf-8"));h=data["history"]
        ax.plot([r["epoch"] for r in h],[r["validation_loss"] for r in h],label=label,color=color,lw=1.5)
        best=int(data["best_epoch"]);ax.scatter(best,h[best-1]["validation_loss"],color=color,s=20,edgecolor="white",zorder=3)
    ax.set(xlabel="Epoch",ylabel="Validation weighted MSE (normalized)",title="Training history and validation-based checkpoint selection")
    ax.legend(frameon=False,ncol=2);fig.tight_layout();save(fig,"training_validation_curves")


def method_comparison():
    with (COMPARISON).open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
    names=["Persistence","LSTM","CNN-LSTM","Conv3D","Transformer","ConvLSTM"]
    fig,axes=plt.subplots(1,3,figsize=(9.2,3.3))
    for ax,key,title,ylim in zip(axes,["test_rmse","test_mae","test_r2"],["RMSE (°C)","MAE (°C)","R²"],[(0,1.7),(0,1.1),(.965,.99)]):
        values=[float(r[key]) for r in rows]
        bars=ax.bar(np.arange(6),values,color=["#6B7280","#2878A5","#4D9A87","#E39138","#8064A2","#C65353"])
        ax.set_title(title,fontweight="bold");ax.set_xticks(np.arange(6),names,rotation=35,ha="right");ax.set_ylim(*ylim);ax.grid(axis="y",alpha=.45)
        for bar,val in zip(bars,values):ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+(ylim[1]-ylim[0])*.018,f"{val:.3f}",ha="center",fontsize=7)
    fig.suptitle("Model comparison · held-out 2025 test set",x=.02,ha="left",fontweight="bold")
    fig.text(.02,.005,"358 aligned target dates · R² axis is truncated to show small differences · single seed",fontsize=7,color="#666666")
    fig.tight_layout(rect=(0,.06,1,.9),w_pad=1.3);save(fig,"model_comparison_test")


def supplementary_errors(pred,target):
    err=json.loads((EXPERIMENT/"error_analysis.json").read_text(encoding="utf-8"))
    ab=list(csv.DictReader((EXPERIMENT/"window_ablation_final"/"window_ablation_results.csv").open(encoding="utf-8-sig",newline="")))
    fig,(a,b)=plt.subplots(1,2,figsize=(8.4,3.4))
    days=[int(r["window_days"]) for r in ab];rmse=[float(r["rmse_celsius"]) for r in ab]
    a.plot(days,rmse,marker="o",color="#2878A5",label="Conv3D RMSE")
    a.axhline(1.395853,color="#6B7280",ls="--",label="Persistence RMSE")
    for x,y in zip(days,rmse):a.annotate(f"{y:.3f}",(x,y),xytext=(0,7),textcoords="offset points",ha="center")
    a.set(xlabel="Input history (days)",ylabel="Test RMSE (°C; zoomed axis)",title="Window ablation · 351 matched dates")
    a.legend(frameon=False,fontsize=7);a.grid(alpha=.4)
    seasons=["DJF","MAM","JJA","SON"];x=np.arange(4);w=.34;s=err["seasonal"]
    b.bar(x-w/2,[s[k]["rmse_celsius"] for k in seasons],w,label="RMSE",color="#2878A5")
    b.bar(x+w/2,[s[k]["mae_celsius"] for k in seasons],w,label="MAE",color="#E39138")
    b.set_xticks(x,[f"{k}\n(n={s[k]['target_days']})" for k in seasons]);b.set(ylabel="Test error (°C)",title="Seasonal errors · 358 dates")
    b.legend(frameon=False,ncol=2,loc="upper left");b.grid(axis="y",alpha=.4)
    fig.suptitle("Input-history and seasonal diagnostics",x=.02,ha="left",fontweight="bold")
    fig.text(.02,.005,"One-seed results; differences are descriptive and not significance-tested.",fontsize=7,color="#666666")
    fig.tight_layout(rect=(0,.06,1,.9),w_pad=1.2);save(fig,"window_seasonal_errors")
    residual=pred-target;bias=residual.mean(axis=0);spatial_rmse=np.sqrt(np.mean(residual**2,axis=0))
    extent=(65,100,5,35)
    fig,axes=plt.subplots(1,2,figsize=(8,3.8),sharex=True,sharey=True)
    im=axes[0].imshow(bias,origin="upper",extent=extent,aspect="auto",cmap="RdBu_r",vmin=-1.5,vmax=1.5)
    im2=axes[1].imshow(spatial_rmse,origin="upper",extent=extent,aspect="auto",cmap="magma",vmin=0,vmax=5.6)
    axes[0].set_title("Mean bias (forecast − target)");axes[1].set_title("Gridpoint RMSE")
    for ax in axes:ax.set_xlabel("Longitude (°E)");ax.set_xticks([65,70,80,90,100]);ax.set_yticks([5,10,20,30,35]);ax.grid(color="white",alpha=.25,lw=.4)
    axes[0].set_ylabel("Latitude (°N)")
    fig.colorbar(im,ax=axes[0],fraction=.046,pad=.04,label="Bias (°C)");fig.colorbar(im2,ax=axes[1],fraction=.046,pad=.04,label="RMSE (°C)")
    fig.suptitle("Spatial errors · held-out 2025 test set",x=.02,ha="left",fontweight="bold")
    fig.text(.02,.005,"Full rectangular ERA5 grid (including ocean cells); no land mask or political borders.",fontsize=7,color="#666666")
    fig.tight_layout(rect=(0,.06,1,.9),w_pad=1.1);save(fig,"spatial_test_errors")


def main():
    model=get_model()
    val_previous,val_pred,val_target=infer_split(model,"val")
    test_previous,test_pred,test_target=infer_split(model,"test")
    val_metrics=calc_metrics(val_pred,val_target);test_metrics=calc_metrics(test_pred,test_target)
    evaluation_plot("Validation",val_pred,val_target,val_metrics)
    evaluation_plot("Test",test_pred,test_target,test_metrics)
    prediction_map("Validation",val_previous,val_pred,val_target)
    prediction_map("Test",test_previous,test_pred,test_target)
    history_plot();method_comparison();supplementary_errors(test_pred,test_target)
    # These old training-set pictures were produced from an unrecoverable legacy run.
    for name in ("train_evaluation.png","train_prediction_map.png"):
        path=OUT/name
        if path.exists():path.unlink()
    for name in ("validation_evaluation.png","validation_prediction_map.png"):
        path=OUT/name
        if path.exists():path.unlink()
    print(f"Updated visualizations from checkpoint {EXPERIMENT/'convlstm_best.pth'}")
    print(f"Device used for fresh inference: {DEVICE}")
    print(f"Validation metrics: {val_metrics}")
    print(f"Held-out 2025 test metrics: {test_metrics}")


if __name__=="__main__":main()
