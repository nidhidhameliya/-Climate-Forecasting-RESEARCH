"""Create an explainable paper figure set from the verified experiment outputs."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXP = ROOT / "experiments" / "reviewer_final_20261014"
COMPARISON = ROOT / "experiments" / "reviewer_comparison_with_recurrent_convlstm_20261014" / "comparison_results.csv"
sys.path.insert(0, str(ROOT / "paper_figures"))
from generate_paper_figures import get_test_outputs  # actual saved checkpoint + test tensors

NAVY, BLUE, TEAL, ORANGE, RED, PURPLE, GRAY = (
    "#17324D", "#2878A5", "#4D9A87", "#E39138", "#C65353", "#8064A2", "#6B7280")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.titlesize": 10, "axes.labelsize": 9,
                     "xtick.labelsize": 8, "ytick.labelsize": 8,
                     "legend.fontsize": 8, "savefig.dpi": 600,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#9AA8B4", "axes.linewidth": .7,
                     "grid.color": "#D9E1E8", "grid.linewidth": .6})


def save(fig, name: str) -> None:
    fig.savefig(HERE / f"{name}.png", bbox_inches="tight", dpi=600, facecolor="white")
    plt.close(fig)


def architecture() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.5))
    fig.suptitle("Forecasting architectures evaluated", x=.02, ha="left",
                 fontsize=13, fontweight="bold", color=NAVY)
    panels = [
        (axes[0], "Proposed model: Conv3D", "29,441 trainable parameters", [
            ("Input: 7 daily maps", "(B, 7, 1, 121, 141)", "#DCEEF4"),
            ("Reorder time/channel axes", "(B, 1, 7, 121, 141)", "#E8EEF4"),
            ("Conv3D 1 -> 32; 3x3x3; ReLU", "32 feature channels", "#DCEEF4"),
            ("Conv3D 32 -> 32; 3x3x3; ReLU", "32 feature channels", "#E6F2E4"),
            ("Conv3D 32 -> 1; 3x3x3", "one output channel at each time index", "#FFF0DC"),
            ("Select final time slice", "next-day map (B, 1, 121, 141)", "#F8E3E1"),
        ]),
        (axes[1], "Baseline: ConvLSTM", "38,177 trainable parameters; one layer, 32 hidden channels", [
            ("Input sequence", "7 maps (B, 7, 1, 121, 141)", "#DCEEF4"),
            ("For each of 7 time steps", "use current map and previous hidden state", "#E8EEF4"),
            ("3x3 gate convolution", "33 input -> 128 maps (i, f, o, candidate)", "#DCEEF4"),
            ("Update cell and hidden states", "sigmoid gates; tanh candidate", "#E6F2E4"),
            ("Final hidden state h_7", "32 channels (B, 32, 121, 141)", "#FFF0DC"),
            ("1x1 Conv2d projection", "next-day map (B, 1, 121, 141)", "#F8E3E1"),
        ]),
    ]
    for ax, title, subtitle, blocks in panels:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
        ax.text(5, 9.55, title, ha="center", fontsize=11, fontweight="bold", color=NAVY)
        ax.text(5, 9.12, subtitle, ha="center", fontsize=8, color=GRAY)
        ys = [7.95, 6.72, 5.49, 4.26, 3.03, 1.80]
        for y, (label, shape, color) in zip(ys, blocks):
            rect = patches.FancyBboxPatch((.45, y), 9.1, .88,
                boxstyle="round,pad=0.025,rounding_size=0.10", linewidth=.8,
                edgecolor="#9AA8B4", facecolor=color)
            ax.add_patch(rect)
            ax.text(5, y+.56, label, ha="center", va="center", fontweight="bold", color=NAVY, fontsize=8.2)
            ax.text(5, y+.27, shape, ha="center", va="center", color="#355265", fontsize=7.2)
        for y in [7.95, 6.72, 5.49, 4.26, 3.03]:
            ax.annotate("", xy=(5, y-.15), xytext=(5, y-.35),
                        arrowprops={"arrowstyle":"-|>","lw":1.1,"color":GRAY})
    fig.text(.02, .015,
        "The proposed implementation is Conv3D. The separately implemented ConvLSTM is the baseline; the historic Figure 3 source was unavailable for exact matching.",
        fontsize=7.5, color=GRAY)
    fig.tight_layout(rect=(0, .045, 1, .91), w_pad=1.4)
    save(fig, "figure_1_actual_architecture")

def dataset_and_split() -> None:
    fig, (a,b)=plt.subplots(2,1,figsize=(8.2,3.7),gridspec_kw={"height_ratios":[1,1.15]})
    a.set_xlim(2018.5,2026); a.set_ylim(0,1); a.set_yticks([]); a.set_xticks(range(2019,2026))
    for left,right,label,color in [(2019,2024,"Train\n2019–2023",BLUE),
                                   (2024,2025,"Validation\n2024",TEAL),
                                   (2025,2026,"Test\n2025",ORANGE)]:
        a.barh(.52,right-left,left=left,height=.4,color=color)
        a.text((left+right)/2,.52,label,ha="center",va="center",color="white",fontweight="bold",fontsize=8)
    a.set_xlabel("Year (source: 2019-01-01 00:00 to 2025-12-31 23:00 UTC)")
    a.set_title("Chronological split",loc="left",fontweight="bold",color=NAVY)
    a.grid(axis="x",alpha=.55);a.set_axisbelow(True)
    x=np.arange(3);w=.34
    bars1=b.bar(x-w/2,[1826,366,365],w,color="#B7CAD6",label="Daily maps")
    bars2=b.bar(x+w/2,[1819,359,358],w,color=[BLUE,TEAL,ORANGE],label="Input/target sequences")
    b.set_xticks(x,["Train","Validation","Test"]);b.set_ylabel("Count")
    b.set_title("Samples after 7-day windowing",loc="left",fontweight="bold",color=NAVY)
    b.legend(frameon=False,ncol=2,loc="upper right");b.grid(axis="y",alpha=.55);b.set_axisbelow(True)
    for bars in [bars1,bars2]:
        for bar in bars:b.text(bar.get_x()+bar.get_width()/2,bar.get_height()+22,f"{int(bar.get_height())}",ha="center",fontsize=7.5)
    fig.text(.02,.015,"Each sequence uses seven daily maps to predict the next day; windows do not cross split boundaries.",
             fontsize=7.5,color=GRAY)
    fig.suptitle("ERA5 study data and evaluation design",x=.02,ha="left",fontweight="bold",color=NAVY)
    fig.tight_layout(rect=(0,.06,1,.92),h_pad=1.1)
    save(fig,"figure_0_data_and_split")


def time_series(inputs: np.ndarray, pred: np.ndarray, target: np.ndarray) -> tuple[int,int,float,float]:
    lat = np.linspace(35, 5, 121)
    lon = np.linspace(65, 100, 141)
    i = int(np.argmin(abs(lat - 28.6))); j = int(np.argmin(abs(lon - 77.2)))
    actual = target[:, i, j]; forecast = pred[:, i, j]; persistence = inputs[:, i, j]
    dates = np.arange(np.datetime64("2025-01-08"), np.datetime64("2025-01-08") + len(actual))
    local_rmse = float(np.sqrt(np.mean((forecast-actual)**2)))
    local_mae = float(np.mean(np.abs(forecast-actual)))
    fig, ax = plt.subplots(figsize=(8.2,3.5))
    ax.plot(dates, actual, color=NAVY, lw=1.1, label="ERA5 target")
    ax.plot(dates, forecast, color=BLUE, lw=1.0, alpha=.9, label="Conv3D forecast")
    ax.plot(dates, persistence, color=ORANGE, lw=.85, alpha=.8, label="Persistence (previous day)")
    ax.set_ylabel("Daily maximum temperature (°C)")
    ax.set_xlabel("Target date (2025)")
    ax.set_title(f"One-day forecasts at {lat[i]:.2f}°N, {lon[j]:.2f}°E (nearest grid point to Delhi)",
                 loc="left", fontweight="bold", color=NAVY)
    ax.grid(alpha=.75); ax.legend(ncol=3, frameon=False, loc="upper left")
    ax.text(.99,.03,f"Conv3D RMSE {local_rmse:.2f}°C · MAE {local_mae:.2f}°C",
            transform=ax.transAxes, ha="right", fontsize=8, color=GRAY)
    fig.tight_layout()
    save(fig,"figure_2_delhi_point_forecast")
    return i,j,local_rmse,local_mae


def scatter_and_errors(pred: np.ndarray, target: np.ndarray) -> tuple[float,float,float,float,float]:
    p, y = pred.ravel(), target.ravel()
    residual = p-y
    rmse = float(np.sqrt(np.mean(residual**2)))
    mae = float(np.mean(np.abs(residual)))
    r2 = float(1-np.sum(residual**2)/np.sum((y-y.mean())**2))
    corr = float(np.corrcoef(p,y)[0,1])
    bias = float(np.mean(residual))
    fig, (a,b) = plt.subplots(1,2,figsize=(8.2,3.5),gridspec_kw={"width_ratios":[1.35,1]})
    hb=a.hexbin(y,p,gridsize=65,mincnt=1,bins="log",cmap="viridis",linewidths=0)
    lo=float(min(y.min(),p.min())); hi=float(max(y.max(),p.max()))
    a.plot([lo,hi],[lo,hi],"--",color=RED,lw=1.3)
    a.set(xlabel="ERA5 target (°C)",ylabel="Conv3D forecast (°C)",title="All test grid cells and dates")
    a.text(.98,.04,"Dashed line: perfect agreement",transform=a.transAxes,ha="right",va="bottom",
           fontsize=7.5,color=RED,bbox={"facecolor":"white","alpha":.85,"edgecolor":"none"})
    cb=fig.colorbar(hb,ax=a,fraction=.046,pad=.04); cb.set_label("Count per hexagon (log scale)")
    a.text(.04,.96,f"RMSE {rmse:.3f}°C\nMAE {mae:.3f}°C\nR² {r2:.4f}\nPearson r {corr:.4f}",
           transform=a.transAxes,va="top",ha="left",fontsize=8,
           bbox={"boxstyle":"round","facecolor":"white","alpha":.92,"edgecolor":"#D9E1E8"})
    b.hist(residual,bins=70,color=BLUE,alpha=.9,edgecolor="white",linewidth=.2)
    b.axvline(0,color=RED,ls="--",lw=1.2)
    b.axvline(bias,color=ORANGE,ls=":",lw=1.5,label=f"Mean error (bias) {bias:.3f}°C")
    b.set(xlabel="Forecast − target (°C)",ylabel="Grid-cell / date count",title="Test residual distribution")
    b.legend(frameon=False,fontsize=7,loc="upper right"); b.grid(axis="y",alpha=.5)
    fig.suptitle("Forecast quality across the independent 2025 test set",x=.02,ha="left",fontweight="bold",color=NAVY)
    fig.text(.02,.005,"358 target dates × 121 × 141 grid cells · metrics computed on the same flattened test predictions and targets",
             color=GRAY,fontsize=7.5)
    fig.tight_layout(rect=(0,.07,1,.92),w_pad=1.3)
    save(fig,"figure_3_test_scatter_and_residuals")
    return rmse,mae,r2,corr,bias


def method_comparison() -> None:
    with (COMPARISON).open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    names=["Persistence","LSTM","CNN-LSTM","Conv3D","Transformer","ConvLSTM"]
    vals=[float(r["test_rmse"]) for r in rows]
    colors=[GRAY,BLUE,TEAL,ORANGE,PURPLE,"#C65353"]
    fig,ax=plt.subplots(figsize=(7.2,3.6))
    bars=ax.bar(names,vals,color=colors,width=.67)
    ax.set_ylabel("Test RMSE (°C; lower is better)")
    ax.set_ylim(0,1.72); ax.grid(axis="y",alpha=.8); ax.set_axisbelow(True)
    ax.set_title("Like-for-like comparison on the 2025 test dates",loc="left",fontweight="bold",color=NAVY)
    for bar,val in zip(bars,vals): ax.text(bar.get_x()+bar.get_width()/2,val+.008,f"{val:.3f}",ha="center",fontsize=8)
    ax.tick_params(axis="x",rotation=12)
    ax.text(.99,.96,"358 aligned targets · one seed",transform=ax.transAxes,ha="right",va="top",color=GRAY,fontsize=8)
    fig.tight_layout()
    save(fig,"figure_4_model_comparison_rmse")


def ablation_and_seasonal() -> None:
    ab=list(csv.DictReader((EXP/"window_ablation_final"/"window_ablation_results.csv").open(encoding="utf-8-sig",newline="")))
    err=json.loads((EXP/"error_analysis.json").read_text(encoding="utf-8"))
    fig,(a,b)=plt.subplots(1,2,figsize=(8.4,3.5))
    days=[int(r["window_days"]) for r in ab]
    rmse=[float(r["rmse_celsius"]) for r in ab]
    mae=[float(r["mae_celsius"]) for r in ab]
    a.plot(days,rmse,color=BLUE,marker="o",lw=1.8,label="Conv3D RMSE")
    a.axhline(1.395853,color=GRAY,ls="--",lw=1.2,label="Persistence RMSE")
    for x,y in zip(days,rmse):a.annotate(f"{y:.3f}",(x,y),xytext=(0,7),textcoords="offset points",ha="center",fontsize=7)
    a.set_xticks(days);a.set_xlabel("Past days supplied to model");a.set_ylabel("Test RMSE (°C; zoomed axis)")
    a.set_title("Input-window ablation",loc="left",fontweight="bold",color=NAVY)
    a.legend(frameon=False);a.grid(axis="y",alpha=.65)
    seasons=["DJF","MAM","JJA","SON"]
    sm=err["seasonal"]; x=np.arange(4);w=.34
    bb1=b.bar(x-w/2,[sm[s]["rmse_celsius"] for s in seasons],w,color=BLUE,label="RMSE")
    bb2=b.bar(x+w/2,[sm[s]["mae_celsius"] for s in seasons],w,color=ORANGE,label="MAE")
    b.set_xticks(x,[f"{s}\n(n={sm[s]['target_days']})" for s in seasons]);b.set_ylabel("Test error (°C)")
    b.set_title("Seasonal error breakdown",loc="left",fontweight="bold",color=NAVY)
    b.set_ylim(0,1.8)
    b.legend(frameon=False,ncol=2,loc="upper right");b.grid(axis="y",alpha=.65);b.set_axisbelow(True)
    for group in (bb1,bb2):
        for bar in group:b.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.02,f"{bar.get_height():.2f}",ha="center",fontsize=7)
    fig.suptitle("Sensitivity to input history and season",x=.02,ha="left",fontweight="bold",color=NAVY)
    fig.text(.02,.005,"Ablation uses 351 common dates; seasonal scores use all 358 test forecasts. Zoomed RMSE axis; single seed, no significance test.",fontsize=7.2,color=GRAY)
    fig.tight_layout(rect=(0,.08,1,.9),w_pad=1.4)
    save(fig,"figure_5_window_and_seasonal_analysis")


def spatial_error(pred: np.ndarray,target:np.ndarray,point:tuple[int,int])->None:
    residual=pred-target
    bias=np.mean(residual,axis=0)
    rmse=np.sqrt(np.mean(residual**2,axis=0))
    lat=np.linspace(35,5,121);lon=np.linspace(65,100,141); extent=(65,100,5,35)
    fig,axes=plt.subplots(1,2,figsize=(8.5,3.9),sharex=True,sharey=True)
    im0=axes[0].imshow(bias,origin="upper",extent=extent,aspect="auto",cmap="RdBu_r",vmin=-1.5,vmax=1.5,interpolation="nearest")
    im1=axes[1].imshow(rmse,origin="upper",extent=extent,aspect="auto",cmap="magma",vmin=0,vmax=5.6,interpolation="nearest")
    titles=["Mean bias: forecast − target","Gridpoint RMSE"]
    for ax,title in zip(axes,titles):
        ax.set_title(title,loc="left",fontweight="bold",color=NAVY);ax.set_xlabel("Longitude (°E)")
        ax.set_xticks([65,70,80,90,100]);ax.set_yticks([5,10,20,30,35]);ax.grid(color="white",alpha=.28,lw=.45)
        ax.scatter([lon[point[1]]],[lat[point[0]]],s=26,marker="o",facecolor="none",edgecolor="cyan",lw=1.3)
    axes[0].set_ylabel("Latitude (°N)")
    cb0=fig.colorbar(im0,ax=axes[0],fraction=.046,pad=.04);cb0.set_label("Bias (°C)")
    cb1=fig.colorbar(im1,ax=axes[1],fraction=.046,pad=.04);cb1.set_label("RMSE (°C)")
    fig.suptitle("Where does the model over/under-predict, and where is error largest?",x=.02,ha="left",fontweight="bold",color=NAVY)
    fig.text(.02,.01,"Computed per grid cell over 358 test dates; cyan circle marks the Delhi-nearest grid point. Grid display, no administrative boundaries.",fontsize=7.4,color=GRAY)
    fig.tight_layout(rect=(0,.07,1,.9),w_pad=1.1)
    save(fig,"figure_6_spatial_bias_and_rmse")


def main()->None:
    HERE.mkdir(exist_ok=True)
    inputs,pred,target,_,_=get_test_outputs()
    dataset_and_split()
    architecture()
    lat_i,lon_i,local_rmse,local_mae=time_series(inputs,pred,target)
    rmse,mae,r2,corr,bias=scatter_and_errors(pred,target)
    method_comparison()
    ablation_and_seasonal()
    spatial_error(pred,target,(lat_i,lon_i))
    print(f"Created explainable figures under {HERE}")
    print(f"Global test metrics: RMSE={rmse:.6f} C, MAE={mae:.6f} C, R2={r2:.6f}, Pearson r={corr:.6f}, bias={bias:.6f} C")
    print(f"Delhi-nearest ({np.linspace(35,5,121)[lat_i]:.2f}N, {np.linspace(65,100,141)[lon_i]:.2f}E): RMSE={local_rmse:.4f} C, MAE={local_mae:.4f} C")


if __name__=="__main__": main()
