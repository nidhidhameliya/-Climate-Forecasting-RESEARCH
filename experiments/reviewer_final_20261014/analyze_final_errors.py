"""Seasonal and gridpoint error analysis for the selected Conv3D test checkpoint."""
import json
from pathlib import Path
import sys
import numpy as np
import xarray as xr

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluate_model import ClimateModelEvaluator

def main():
    e=ClimateModelEvaluator(model_path=str(ROOT/'experiments/reviewer_final_20261014/convlstm_best.pth'))
    result,pred,target=e.evaluate('test',save=False,visualize=False)
    dates=np.asarray(result['alignment']['first_target_date'],dtype='datetime64[D]')+np.arange(len(pred))
    months=(dates.astype('datetime64[M]').astype(int)%12)+1
    season_sets={'DJF':(months==12)|(months<=2),'MAM':(months>=3)&(months<=5),'JJA':(months>=6)&(months<=8),'SON':(months>=9)&(months<=11)}
    seasonal={}
    err=pred-target
    for name,mask in season_sets.items():
        x=err[mask]
        seasonal[name]={'target_days':int(mask.sum()),'rmse_celsius':float(np.sqrt(np.mean(x*x))),'mae_celsius':float(np.mean(np.abs(x)))}
    grid_rmse=np.sqrt(np.mean(err**2,axis=0))[0]
    minidx=np.unravel_index(np.argmin(grid_rmse),grid_rmse.shape); maxidx=np.unravel_index(np.argmax(grid_rmse),grid_rmse.shape)
    with xr.open_dataset(ROOT/'data/interim/test_daily.nc') as ds:
        lat=np.asarray(ds.latitude.values); lon=np.asarray(ds.longitude.values)
    def point(idx): return {'latitude':float(lat[idx[0]]),'longitude':float(lon[idx[1]]),'rmse_celsius':float(grid_rmse[idx])}
    output={'checkpoint':'experiments/reviewer_final_20261014/convlstm_best.pth','aligned_test_dates':[str(dates[0]),str(dates[-1])],'samples':int(len(dates)),'seasonal':seasonal,'spatial_gridpoint_rmse':{'min':point(minidx),'mean':float(grid_rmse.mean()),'max':point(maxidx)},'high_error_point_35N_65E':json.loads((ROOT/'experiments/reviewer_final_20261014/high_error_point_35N_65E.json').read_text())}
    path=ROOT/'experiments/reviewer_final_20261014/error_analysis.json'; path.write_text(json.dumps(output,indent=2,allow_nan=False))
    print(json.dumps(output,indent=2))
if __name__=='__main__': main()
