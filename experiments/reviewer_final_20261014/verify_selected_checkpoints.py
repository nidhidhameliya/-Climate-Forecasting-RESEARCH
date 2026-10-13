"""Re-evaluate selected checkpoints against the recorded validation/test metrics."""
import json, sys
from pathlib import Path
import numpy as np
import torch, yaml
from torch.utils.data import DataLoader,TensorDataset
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from models.model_utils import get_model

def score(pred,target):
 p,t=pred.ravel(),target.ravel()
 return {'rmse':float(np.sqrt(mean_squared_error(t,p))),'mae':float(mean_absolute_error(t,p)),'r2':float(r2_score(t,p)),'correlation':float(np.corrcoef(p,t)[0,1])}
def main():
 torch_device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
 cfg=yaml.safe_load((ROOT/'config.yaml').read_text()); stats=json.loads((ROOT/'data/processed/mean_std.json').read_text());mean,std=float(stats['mean']),float(stats['std'])
 ref=json.loads((ROOT/'experiments/reviewer_final_20261014/comparison_results.json').read_text());checks=[]
 for entry in ref['results']:
  name=entry['model'].lower()
  if name=='persistence':continue
  config={**cfg,'model':{**cfg['model'],'name':name}}
  model=get_model(config).to(torch_device)
  cp=ROOT/entry['checkpoint'].replace('\\','/')
  model.load_state_dict(torch.load(cp,map_location=torch_device,weights_only=True));model.eval()
  split_scores={}
  for split in ('val','test'):
   X=np.load(ROOT/f'data/processed/tensors/{split}_X.npy');Y=np.load(ROOT/f'data/processed/tensors/{split}_y.npy')
   loader=DataLoader(TensorDataset(torch.from_numpy(X).float(),torch.from_numpy(Y).float()),batch_size=16,shuffle=False)
   ps=[];ys=[]
   with torch.no_grad():
    for x,y in loader:
     z=model(x.to(torch_device)).cpu().numpy()[:,0];ps.append(z*std+mean);ys.append(y.numpy()[:,0]*std+mean)
   measured=score(np.concatenate(ps),np.concatenate(ys)); expected=entry['validation' if split=='val' else 'test']
   delta={k:abs(measured[k]-float(expected['correlation' if k=='correlation' else k])) for k in measured}
   split_scores[split]={'metrics':measured,'max_abs_metric_delta':max(delta.values()),'matches_aggregate':max(delta.values())<=1e-5,'samples':len(X)}
  all_match=all(x['matches_aggregate'] for x in split_scores.values())
  checks.append({'model':name,'checkpoint':entry['checkpoint'],'checkpoint_metrics_match_aggregate':all_match,'splits':split_scores})
  print(name,split_scores,flush=True)
 out={'device':str(torch_device),'checkpoint_checks':checks,'all_match':all(x['checkpoint_metrics_match_aggregate'] for x in checks)};(ROOT/'experiments/reviewer_final_20261014/checkpoint_recheck.json').write_text(json.dumps(out,indent=2,allow_nan=False));print('ALL_SELECTED_CHECKPOINTS_MATCH',out['all_match'])
if __name__=='__main__':main()
