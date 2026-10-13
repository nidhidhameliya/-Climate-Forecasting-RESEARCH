import sys
sys.path.insert(0, r'C:\Users\25mdsml006\Desktop\deep_learning\project\climate\climate2')
from evaluate_model import ClimateModelEvaluator
p=r'experiments\reviewer_final_20261014\convlstm_best.pth'
e=ClimateModelEvaluator(model_path=p)
r,_,_=e.evaluate('val',save=False,visualize=False)
print('VAL_ALIGNMENT_CROSSCHECK',r['alignment'],r['metrics'])
