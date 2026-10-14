# 🌍 Climate Temperature Forecasting with Conv3D

[![Project Status](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)
![Dataset](https://img.shields.io/badge/Dataset-ERA5-green.svg)
![Deep Learning](https://img.shields.io/badge/Model-Conv3D-orange.svg)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-brightgreen?logo=streamlit)](https://climate-forecasting-9mfng65j47sierrx5jm6pe.streamlit.app/)

---

# 📖 Climate Temperature Forecasting

A research pipeline for **next-day ERA5 2 m temperature forecasting**. The proposed class named `ConvLSTMModel` is implemented as a **Conv3D encoder-decoder**, not a recurrent ConvLSTM.

The repository contains an ERA5 preprocessing and forecasting pipeline. The verified study run and its limits are summarized below; general-purpose pipeline scripts may require the original local data and configuration.

The project provides components for:

- 🌍 Climate data acquisition
- 🛰 Data preprocessing
- 📊 Sequence generation
- 🧠 Deep learning model training
- 📈 Model evaluation
- 🌡 Temperature prediction
- 📉 Performance visualization

The framework is modular, reproducible, and configurable, making it suitable for research and real-world climate forecasting applications.

---

# 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Workflow](#-workflow)
- [Dataset](#-dataset)
- [Methodology](#-methodology)
- [Results](#results)
- [Change log](changes.md)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Data Pipeline](#-data-pipeline)
- [Available Models](#-available-models)
- [Usage](#-usage)
- [Troubleshooting](#-troubleshooting)
- [Dependencies](#-dependencies)
- [Roadmap](#-roadmap)
- [Citation](#-citation)
- [Acknowledgements](#-acknowledgements)
- [License](#-license)

---

# 🎯 Project Overview

Climate temperature prediction is essential for agriculture, disaster management, environmental monitoring, renewable energy planning, and weather forecasting.

Traditional numerical weather prediction methods require significant computational resources and may struggle to accurately capture localized temperature variations over space and time.

The proposed implementation is a Conv3D encoder-decoder over seven daily temperature maps. Separate LSTM, CNN-LSTM, and Transformer implementations are included as comparison models. The `convlstm` identifier is a legacy compatibility name, not evidence of a recurrent ConvLSTM.

The framework automates the complete forecasting pipeline, including:

- ERA5 climate data download
- Data preprocessing
- Geographic region extraction
# Results

## Verified data and preprocessing

- ERA5 hourly 2 m temperature (`t2m`) in Kelvin: 2019-01-01 00:00 to 2025-12-31 23:00 UTC.
- Region: 5-35 N, 65-100 E; 121 x 141 grid at 0.25-degree spacing.
- Splits: train 2019-2023 (43,824 hourly, 1,826 daily, 1,819 sequences); validation 2024 (8,784 hourly, 366 daily, 359 sequences); test 2025 (8,760 hourly, 365 daily, 358 sequences).
- Daily fields are the maximum of 24 complete UTC hourly observations. Non-finite values are rejected, not imputed.
- Training-only normalization: mean 25.044549 degrees C, population std 10.995944 degrees C. Training-only 95th percentile 37.254114 degrees C; normalized loss threshold 1.110370 and extreme weight 5.
- Train/source equality was verified. Validation/test date ranges, cadence, dimensions, and finite values were checked; exact value-by-value equality against the raw source remains unverified.

## Corrected five-model comparison

RTX 4070, seed 42, batch size 16, Adam at 1e-4, 50 epochs per learned model. Checkpoints were selected by validation loss; test metrics use aligned 2025 predictions and targets. RMSE/MAE are degrees C; R-squared and Pearson r are separate dimensionless statistics.

| Model | Parameters | Actual epochs | Best epoch | Test RMSE C | Test MAE C | Test R2 | Pearson r |
|---|---:|---:|---:|---:|---:|---:|---:|
| Persistence | 0 | 0 | n/a | 1.402716 | 0.897498 | 0.981867 | 0.990937 |
| LSTM | 4,513 | 50 | 50 | 1.572731 | 1.016080 | 0.977206 | 0.988568 |
| CNN-LSTM | 18,049 | 50 | 48 | 1.400517 | 0.898668 | 0.981924 | 0.990928 |
| Conv3D encoder-decoder | 29,441 | 50 | 39 | 1.364915 | 0.874530 | 0.982832 | 0.991407 |
| Transformer | 275,105 | 50 | 36 | 1.403025 | 0.898712 | 0.981860 | 0.990936 |

The proposed code is Conv3D, not recurrent ConvLSTM. Conv3D modestly outperforms persistence in this single-seed test year. The manuscript values 1.8886/1.6200/0.9720/0.2477 are not verified results from this aligned test evaluation.

## Verified visualization and paper figures

The plots in [`outputs/visualizations/`](outputs/visualizations/) were regenerated from the selected checkpoint and the current validation/test tensors. The [visualization audit](outputs/visualizations/VISUALIZATION_AUDIT.md) documents their data sources, metric checks, and limitations. Recreate these plots from the repository root with:

```bash
python outputs/visualizations/generate_verified_visualizations.py
```

The script runs inference with the saved checkpoint; it does not retrain the model. The folder contains held-out test and validation diagnostics, representative forecast maps, model comparison, input-window and seasonal errors, spatial errors, and training/validation histories. Training-set evaluation maps were removed because verified training evaluation outputs were unavailable.

Manuscript-ready figure exports and captions are in [`paper_figures/`](paper_figures/FIGURE_CAPTIONS.md). They are generated by [`generate_paper_figures.py`](paper_figures/generate_paper_figures.py). PNG files are previews; PDF files are vector exports. The [figure captions](paper_figures/FIGURE_CAPTIONS.md) identify what each plot shows and the data used.

Final RMSE, MAE, and R² values in the corrected model comparison are calculated on the independent 2025 test set. Validation results are reported separately and are used for model/checkpoint selection. The daily normalization is a training-only z-score: convert Kelvin to Celsius, subtract the training-period mean, and divide by the training-period population standard deviation; apply those same training statistics to validation and test data. Non-finite values are rejected during preprocessing rather than silently imputed.

## Matched-date input-window ablation

Separate Conv3D models were selected on validation loss and evaluated on the same 351 dates, 2025-01-15 through 2025-12-31. Single-seed differences are small and not significance-tested.

| Input days | Best epoch | Test RMSE C | Test MAE C | Test R2 | Pearson r |
|---:|---:|---:|---:|---:|---:|
| Persistence | n/a | 1.395853 | 0.892756 | 0.981761 | 0.990882 |
| 3 | 48 | 1.367838 | 0.873910 | 0.982486 | 0.991278 |
| 7 | 41 | 1.361286 | 0.872670 | 0.982653 | 0.991375 |
| 14 | 40 | 1.358829 | 0.868374 | 0.982716 | 0.991394 |

Complete histories and checkpoints are in `experiments/reviewer_final_20261014/` (LSTM repair: `experiments/reviewer_lstm_repaired_20261014/`); ablation artifacts are in `experiments/reviewer_final_20261014/window_ablation_final/`. Seasonal and spatial error results and the 35 N, 65 E trace are in `experiments/reviewer_final_20261014/error_analysis.json` and `high_error_point_35N_65E.json`. Full reviewer answers are in [reviewer_questions_answers.md](reviewer_questions_answers.md); command outputs are in [terminal_outputs.md](terminal_outputs.md).

## Reproduction

```powershell
.\.venv\Scripts\python.exe -u preprocessing\compute_extremes.py
.\.venv\Scripts\python.exe -u verify_preprocessing.py
.\.venv\Scripts\python.exe -u run_baseline_experiments.py --epochs 50 --batch-size 16 --seed 42 --device cuda --models persistence,lstm,cnn_lstm,convlstm,transformer --output-dir experiments\NEW_RUN
.\.venv\Scripts\python.exe -u experiments\reviewer_final_20261014\run_window_ablation.py --output-dir experiments\reviewer_final_20261014\window_ablation_NEW_RUN
```

# 🔬 Methodology

The proposed implementation is a **Conv3D encoder-decoder**. It permutes `(B, 7, 1, 121, 141)` to Conv3D order `(B, 1, 7, 121, 141)`, applies two 3?3?3 Conv3D/ReLU layers with 32 channels and a 3?3?3 Conv3D decoder, then selects the last temporal index. It has 29,441 trainable parameters and no recurrent gates or cell state. The `convlstm` config value remains a compatibility alias; it does not describe the architecture.

The overall methodology consists of:

1. Download ERA5 climate data
2. Select the target geographic region
3. Convert hourly observations into daily maxima (as implemented in `preprocessing/rebuild_downstream.py`)
4. Normalize temperature values
5. Generate sliding-window sequences
6. Train the Conv3D encoder-decoder
7. Predict next-day temperature maps
8. Evaluate prediction accuracy
9. Visualize forecasting results

## Why 2-meter air temperature only?

The project focuses on `t2m` because it is the single target variable used by
the download, preprocessing, tensor-generation, model, dashboard, and
evaluation paths. Keeping one spatially gridded target makes the current study
a focused test of next-day spatiotemporal temperature prediction and avoids
introducing unsupported assumptions about how humidity, pressure, wind, or
precipitation should be encoded. This is a scope decision, not evidence that
additional variables are unnecessary. Multivariable inputs and independent
observations remain important future work.

---

# 📊 Results

The current data audit, metric definitions, unresolved source-equality checks, high-error point trace, and point-by-point response are in [reviewer_questions_answers.md](reviewer_questions_answers.md). The dated project change record is [changes.md](changes.md); command outputs and verification records are in [terminal_outputs.md](terminal_outputs.md). Historical metric tables in older notes are not results of the corrected run.

# 📂 Project Structure

The project is organized into modular components for easy development, maintenance, and experimentation.

```text
climate2/
│
├── models/                    # Deep Learning Models
│   ├── convlstm.py
│   ├── cnn_lstm.py
│   ├── transformer.py
│   └── model_utils.py
│
├── preprocessing/             # Data preprocessing pipeline
│   ├── data_download/
│   ├── merge_years.py
│   ├── subset_region.py
│   ├── split_by_year.py
│   ├── resample_time.py
│   ├── normalize.py
│   ├── create_sequences.py
│   └── main.py
│
├── training/                  # Model training and evaluation
│   ├── train.py
│   ├── validate.py
│   ├── test.py
│   ├── metrics.py
│   └── losses.py
│
├── data_loader/               # PyTorch DataLoader
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── metadata/
│   └── splits/
│
├── experiments/               # Saved experiments
├── outputs/                   # Predictions & Visualizations
├── notebooks/                 # Jupyter notebooks
│
├── dashboard.py               # Streamlit Dashboard
├── predict_by_date.py
├── evaluate_model.py
├── future_predict.py
├── config.yaml
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## Prerequisites

Before running the project, ensure your system has:

- Python 3.10 or later
- Git
- 8 GB RAM (16 GB recommended)
- CUDA-enabled GPU (optional but recommended)
- Copernicus Climate Data Store (CDS) API account

---

## Clone Repository

```bash
git clone https://github.com/nidhidhameliya/-Climate-Forecasting-RESEARCH.git

cd climate2
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## Verify Installation

```bash
python --version

python -c "import torch; print(torch.__version__)"

python -c "import xarray"
```

---

# ⚙ Configuration

All project settings are managed through a single configuration file.

```
config.yaml
```

The configuration includes:

| Category | Description |
|-----------|-------------|
| Variable | Climate variable (t2m) |
| Region | Latitude & Longitude bounds |
| Sequence Length | Number of historical days |
| Batch Size | Training batch size |
| Learning Rate | Optimizer learning rate |
| Epochs | Maximum training epochs |
| Model | Conv3D encoder-decoder / LSTM / CNN-LSTM / Transformer |
| Device | CUDA or CPU |

---

## Example Configuration

```yaml
variable: t2m

sequence_length: 7

training:
  batch_size: 8
  epochs: 100
  learning_rate: 0.0001

model:
  name: convlstm
  hidden_dim: 32
  num_layers: 2
```

---

# 🌍 Data Pipeline

The preprocessing pipeline converts raw ERA5 climate data into model-ready tensors.

```text
ERA5 Dataset
      │
      ▼
Download Climate Data
      │
      ▼
Merge Yearly Files
      │
      ▼
Region Selection
      │
      ▼
Train / Validation / Test Split
      │
      ▼
Daily Resampling
      │
      ▼
Normalization
      │
      ▼
Sliding Window Sequence Generation
      │
      ▼
Model Ready Dataset
```

---

## Preprocessing Steps

### 1. Download ERA5 Data

```bash
python preprocessing/data_download/download_era5.py
```

---

### 2. Merge Yearly Files

```bash
python preprocessing/merge_years.py
```

---

### 3. Extract Study Region

```bash
python preprocessing/subset_region.py
```

---

### 4. Split Dataset

```bash
python preprocessing/split_by_year.py
```

---

### 5. Daily Resampling

```bash
python preprocessing/rebuild_downstream.py
```

---

### 6. Normalize Data

```bash
python preprocessing/normalize.py
```

---

### 7. Generate Sequences

```bash
python preprocessing/create_sequences.py
```

---

### Complete Preprocessing Pipeline

Instead of executing every step individually:

```bash
python preprocessing/main.py --preprocess
```

---

# 🧠 Available Models

The project supports multiple deep learning architectures for spatiotemporal forecasting.

---

## 1. Conv3D Encoder-Decoder (Proposed)

The class is named `ConvLSTMModel` and selected with the compatibility value `model.name: convlstm`; internally it is three Conv3D layers with ReLU after the first two. It is not a genuine ConvLSTM. In the corrected 50-epoch run it achieved test RMSE 1.364915 deg C and MAE 0.874530 deg C, selected at epoch 39 by validation loss.

```yaml
model:
  name: convlstm
  hidden_dim: 32
```

---

## 2. CNN-LSTM

**Architecture**

CNN Feature Extractor + LSTM Temporal Model

**Advantages**

- Strong spatial feature extraction
- Good temporal learning
- Effective for complex climate patterns

**Configuration**

```yaml
model:
  name: cnn_lstm
```

---

## 3. Transformer

**Architecture**

Multi-Head Self Attention

**Advantages**

- Captures long-range dependencies
- Parallel computation
- Suitable for long climate sequences

**Configuration**

```yaml
model:
  name: transformer
```

---

## Model Comparison

| Model name | Implemented structure | Trainable parameters |
|---|---|---:|
| `convlstm` | Conv3D encoder-decoder; no recurrence | 29,441 |
| `lstm` | Shared per-grid-cell LSTM | 4,513 |
| `cnn_lstm` | Per-day CNN, pooled temporal LSTM, spatial decoder | 18,049 |
| `transformer` | Pooled temporal Transformer encoder with spatial skip | 275,105 |

Use the measured validation/test results above; no architecture is claimed to be universally best.

# 💻 Usage

After completing the installation and preprocessing steps, you can train, evaluate, and visualize the model using the commands below.

---

## 🚀 Train the Model

Train the configured Conv3D encoder-decoder. The `convlstm` model identifier remains for code compatibility.

```bash
python main.py
```

Or specify a custom configuration file.

```bash
python main.py --config config.yaml
```

The training pipeline automatically performs:

- Dataset loading
- Model initialization
- Training
- Validation
- Checkpoint saving
- Performance logging

All trained models are stored inside the `experiments/` directory.

---

# 🔍 Evaluate the Model

Evaluate the trained model on the test dataset.

```bash
python evaluate_model.py \
--model-path experiments/exp_02_convlstm/best_model.pth
```

The evaluation reports:

- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)
- R² Score
- Temperature prediction maps
- Performance graphs

Results are automatically saved in:

```text
outputs/
```

---

# 🌡 Make Temperature Predictions

Predict temperature for a specific day.

```bash
python predict_by_date.py --date 2023-06-15
```

Predict temperatures for multiple days.

```bash
python predict_by_date.py \
--start-date 2023-06-01 \
--end-date 2023-06-30
```

Predictions are stored inside

```text
outputs/predictions/
```

---

# 🔮 Future Forecasting

Generate forecasts for future days.

```bash
python future_predict.py --days-ahead 30
```

Example

```text
Input :
Last 7 Days Temperature Maps

↓

Output :

Next 30 Days Temperature Forecast
```

---

# 📊 Interactive Dashboard

Launch the Streamlit dashboard.

```bash
streamlit run dashboard.py
```

The dashboard provides

- Prediction visualization
- Temperature maps
- Model comparison
- Evaluation metrics
- Interactive charts
- Regional forecasting

---

# 🧪 Quick Testing

Generate a synthetic dataset.

```bash
python generate_synthetic_data.py --samples 1000
```

Run a quick validation.

```bash
python quick_test.py
```

Verify prediction outputs.

```bash
python verify_results.py
```

Debug predictions.

```bash
python debug_predictions.py
```

---

# 🔎 Data Validation

Validate the processed dataset.

```bash
python check_available_data.py

python check_data.py

python check_merged.py

python check_tensors.py
```

These scripts verify

- Missing files
- Dataset integrity
- Tensor dimensions
- Data consistency
- Merge correctness

---

# 🛠 Troubleshooting

## Installation Issues

### Missing PyTorch

```bash
pip install torch torchvision torchaudio
```

---

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

---

## GPU Issues

### CUDA Not Available

Check CUDA availability.

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If CUDA is unavailable, switch to CPU.

```yaml
training:
    device: cpu
```

---

### CUDA Out of Memory

Reduce batch size.

```yaml
training:
    batch_size: 4
```

---

## Data Issues

### Missing ERA5 Files

Download again.

```bash
python preprocessing/data_download/download_era5.py
```

---

### Corrupted Data

Run

```bash
python check_data.py

python fix_data.py
```

---

### Tensor Errors

```bash
python check_tensors.py

python preprocessing/create_sequences.py
```

---

## Training Issues

### Loss Becomes NaN

Reduce learning rate.

```yaml
learning_rate: 0.00001
```

Increase regularization.

```yaml
weight_decay: 1e-5
```

---

### Overfitting

Increase

```yaml
dropout: 0.3
```

or

```yaml
weight_decay: 1e-4
```

---

### Slow Training

Increase

```yaml
batch_size: 16
```

if GPU memory permits.

---

# 📦 Dependencies

Major libraries used in this project.

| Library | Purpose |
|----------|----------|
| PyTorch | Deep Learning |
| Xarray | NetCDF Processing |
| NumPy | Numerical Computing |
| Pandas | Data Analysis |
| NetCDF4 | Climate Data |
| Scikit-learn | Metrics & Preprocessing |
| Matplotlib | Visualization |
| CDS API | ERA5 Download |
| Streamlit | Dashboard |
| PyYAML | Configuration |

Install all dependencies.

```bash
pip install -r requirements.txt
```

---

# 🚀 Deployment

The project can be deployed using Streamlit.

## Streamlit Cloud

1. Push repository to GitHub.
2. Create a Streamlit Cloud application.
3. Select

```
dashboard.py
```

as the entry point.

---

## Render

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
streamlit run dashboard.py
```

---

## Recommended Deployment

| Platform | Status |
|----------|--------|
| Streamlit Cloud | ✅ Recommended |
| Render | ✅ Recommended |
| Railway | ✅ Supported |
| Docker | ✅ Supported |
| Vercel | ❌ Not Recommended |

> **Note:** Vercel is not suitable for this project because of its serverless execution limits and the large machine learning dependencies required by PyTorch and Streamlit.
>
> ---

# 🗺️ Project Roadmap

The project is continuously evolving with additional models, optimization techniques, and deployment capabilities.

## ✅ Completed

- [x] ERA5 Climate Data Integration
- [x] Automated Data Preprocessing Pipeline
- [x] Conv3D encoder-decoder implementation (not recurrent ConvLSTM)
- [x] Model Training & Validation Pipeline
- [x] Temperature Prediction
- [x] Model Evaluation Metrics
- [x] Streamlit Dashboard
- [x] Configuration Management
- [x] Experiment Tracking

---

## 🚧 In Progress

- [ ] CNN-LSTM Performance Optimization
- [ ] Transformer Model Training
- [ ] Real-Time Temperature Prediction
- [ ] Model Performance Benchmarking
- [ ] Improved Visualization Dashboard

---

## 📌 Planned Features

- [ ] Multi-Step Temperature Forecasting
- [ ] Extreme Weather Event Prediction
- [ ] Ensemble Learning Models
- [ ] Hyperparameter Optimization
- [ ] Model Explainability (XAI)
- [ ] Docker Support
- [ ] REST API using FastAPI
- [ ] Cloud Deployment
- [ ] CI/CD Pipeline
- [ ] Automated Experiment Tracking

---

# 📈 Performance Summary

| Metric | Value |
|----------|--------|
| Dataset | ERA5 Climate Reanalysis |
| Climate Variable | 2m Air Temperature (t2m) |
| Input Sequence Length | 7 Days |
| Forecast Horizon | Next Day |
| Framework | PyTorch |
| Proposed Implementation | Conv3D encoder-decoder (`ConvLSTMModel`) |
| Spatial Resolution | 121 × 141 Grid |
| Data Format | NetCDF (.nc) |

---

# 📚 Documentation

Additional project documentation is available in the repository.

| Document | Description |
|----------|-------------|
| `reviewer_questions_answers.md` | Evidence-based reviewer responses, verified results, and unresolved items |
| `changes.md` | Dated summary of project documentation and experiment updates |
| `terminal_outputs.md` | Important commands, outputs, and exit statuses |
| `IMPLEMENTATION_ROADMAP.md` | Development Timeline |
| `DECISION_TREE.md` | Workflow Guide |
| `LIVE_STREAMING_GUIDE.md` | Streaming Prediction |
| `STATIC_VS_STREAMING_GUIDE.md` | Architecture Comparison |
| `SIMPLE_AUTOMATION_GUIDE.md` | Automation Guide |

---

# 📓 Jupyter Notebooks

The repository also includes notebooks for experimentation and debugging.

| Notebook | Purpose |
|-----------|----------|
| `01_explore_data.ipynb` | Data Exploration |
| `02_preprocessing_debug.ipynb` | Preprocessing Pipeline |
| `03_model_debug.ipynb` | Model Debugging |

---

# 📜 Citation

If you use this repository in your research or publications, please cite it as:

```bibtex
@software{ClimateForecasting2026,
  author = {Nidhi Dhameliya},
  title = {AI-Powered Climate Temperature Forecasting using a Conv3D Encoder-Decoder},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/your-username/your-repository}
}
```

---

## ERA5 Dataset Citation

```bibtex
@article{hersbach2020era5,
  title={The ERA5 Global Reanalysis},
  author={Hersbach, H. and others},
  journal={Quarterly Journal of the Royal Meteorological Society},
  year={2020}
}
```

---

# 🙏 Acknowledgements

This project was made possible through the support of the following open-source tools and datasets:

- **ECMWF** – ERA5 Climate Reanalysis Dataset
- **Copernicus Climate Change Service (C3S)**
- **PyTorch**
- **Xarray**
- **NetCDF4**
- **NumPy**
- **Pandas**
- **Scikit-learn**
- **Matplotlib**
- **Streamlit**
- **CDS API**

Special thanks to the open-source community for providing high-quality tools that made this research possible.

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

Please ensure your code follows the existing project structure and coding style.

---

# 🐛 Reporting Issues

If you encounter a bug or have a feature request, please open a GitHub Issue with:

- Problem description
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- System information

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more details.

---

# ⭐ Support the Project

If you find this repository useful for your research, learning, or development, please consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.

---

## 👩‍💻 Author

**Nidhi Dhameliya**

M.Tech – Data Science & Machine Learning

Deep Learning • Climate Informatics • Artificial Intelligence • Spatiotemporal Forecasting

---

<div align="center">

### ⭐ If you like this project, don't forget to star the repository! ⭐

**Happy Forecasting! 🌍📈**

</div>
