# 🗂️ Credit Card Fraud Detection — DVC Data Versioning Pipeline

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6?logo=dvc&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2.2-F7931E?logo=scikit-learn&logoColor=white)
![Google Drive](https://img.shields.io/badge/Remote-Google%20Drive-4285F4?logo=google-drive&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/Minhal-Zafar/DVC/main.yml?label=DVC%20CI&logo=github-actions)

An end-to-end **MLOps data versioning pipeline** using **DVC (Data Version Control)** to version a 150MB credit card fraud dataset stored on **Google Drive**, train a **Decision Tree classifier**, track model accuracy as a reproducible metric, and automatically publish **metrics diffs** on every pull request via **GitHub Actions**.

---

## 🎯 What It Does

1. **Versions a large dataset** (150MB `creditcard.csv`) on Google Drive using DVC — keeping the actual data out of Git
2. **Pulls the dataset** on demand via `dvc pull` using a Google Drive service account
3. **Trains a Decision Tree classifier** on the credit card fraud dataset
4. **Writes accuracy to `metrics.json`** — tracked by DVC as a pipeline output
5. **Reproduces the full pipeline** with `dvc repro`, only re-running stages when dependencies change
6. **Posts a metrics diff** as a PR comment on every GitHub push via GitHub Actions

---

## 📊 Model Performance

| Metric   | Value      |
|----------|------------|
| Accuracy | **99.95%** |

> Achieved by a `DecisionTreeClassifier` with `max_depth=10`, trained on a 70/30 train-test split of the credit card fraud dataset.

---

## 🏗️ Project Structure

```
DVC/
├── .dvc/
│   ├── configure                           # DVC remote config (Google Drive + service account)
│   └── dvc-remote-386207-9fb83cae439c.json # GCP service account credentials
├── .github/
│   └── workflows/
│       └── main.yml                        # GitHub Actions: DVC repro + metrics diff on PR
└── MLOPs-main/
    ├── train.py                            # Decision Tree training script → outputs metrics.json
    ├── dvc.yaml                            # DVC pipeline stage definitions
    ├── dvc.lock                            # Locked pipeline state (checksums + sizes)
    ├── creditcard.csv.dvc                  # DVC pointer to the 150MB dataset on Google Drive
    ├── metrics.json                        # Tracked model accuracy output
    ├── requirements.txt                    # Python dependencies
    └── Makefile                            # Install shorthand
```

---

## 🔄 DVC Pipeline

The pipeline is defined in `dvc.yaml` with two stages:

```
┌─────────────────┐         ┌──────────────────────────────────────┐
│   Stage: test   │         │   Stage: train_data                  │
│                 │         │                                      │
│  echo "Hello"   │         │  Deps:    creditcard.csv             │
│  (smoke test)   │         │  Cmd:     python train.py            │
└─────────────────┘         │  Metrics: metrics.json (no cache)    │
                            └──────────────────────────────────────┘
```

DVC tracks the dataset by its **MD5 hash** (`e90efcb83d69faf99fcab8b0255024de`) and the metrics output by its own hash — ensuring full **reproducibility** and **change detection**.

---

## ☁️ Remote Storage — Google Drive

The large `creditcard.csv` dataset (150MB) is stored on **Google Drive** and accessed via a **GCP service account**, keeping the binary data out of the Git repository entirely.

```
DVC Remote:  gdrive://1Diui_zfFplG4Ugo1JGzJjBmALdYnV-GP
Auth:        GCP Service Account (dvc-account@dvc-remote-386207.iam.gserviceaccount.com)
```

The `.dvc/configure` file and service account JSON handle authentication automatically — no manual OAuth flow required.

---

## 🔁 CI/CD — GitHub Actions

Every push triggers the **DVC Tracking** workflow, which:

```
git push
    │
    ▼
┌──────────────────────────────────────────────────┐
│  DVC Tracking with GitHub Actions                │
│  ──────────────────────────────────────────────  │
│  1. make install      → install dependencies     │
│  2. dvc pull          → fetch dataset from Drive │
│  3. dvc repro         → re-run changed stages    │
│  4. dvc metrics diff  → compare vs main branch   │
│  5. gh pr comment     → post metrics diff to PR  │
└──────────────────────────────────────────────────┘
```

On pull requests, a **metrics comparison table** is automatically posted as a PR comment — showing exactly how accuracy changed between the feature branch and `main`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Git
- DVC with Google Drive support (`dvc-gdrive`)
- Access to the configured Google Drive remote (or substitute your own)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Minhal-Zafar/DVC.git
cd DVC/MLOPs-main

# 2. Install dependencies
make install
# or manually:
pip install --upgrade pip && pip install -r requirements.txt

# 3. Pull the dataset from Google Drive remote
dvc pull

# 4. Run the full pipeline
dvc repro

# 5. Check model metrics
dvc metrics show
```

---

## 🔍 Key DVC Commands

```bash
# Check pipeline status (what's changed)
dvc status

# Reproduce only changed stages
dvc repro

# View current metrics
dvc metrics show

# Compare metrics against another branch/commit
dvc metrics diff main

# Push data changes to Google Drive remote
dvc push

# Pull latest data from Google Drive remote
dvc pull
```

---

## 🤖 Model Details

**Algorithm:** `DecisionTreeClassifier` (scikit-learn 1.2.2)

```python
clf = DecisionTreeClassifier(max_depth=10)
clf.fit(X_train, y_train)          # 70% training split
accuracy = correct / total         # Written to metrics.json
```

**Dataset:** `creditcard.csv` — 150MB credit card transaction dataset with binary fraud labels (last column)

**Split:** 70% train / 30% test (`random_state=42` for reproducibility)

---

## 📦 Dependencies

```
scikit-learn==1.2.2   # Decision Tree classifier
dvc                   # Data & pipeline versioning
dvc-gdrive            # Google Drive remote support
```

---

## 📌 Key MLOps Concepts Demonstrated

| Concept                        | Implementation                                          |
|--------------------------------|---------------------------------------------------------|
| ✅ Data Versioning              | DVC tracks 150MB CSV by MD5 hash — not stored in Git   |
| ✅ Remote Data Storage          | Google Drive via GCP service account authentication    |
| ✅ Reproducible Pipelines       | `dvc.yaml` + `dvc.lock` ensure identical reruns        |
| ✅ Metrics Tracking             | `metrics.json` tracked as a DVC pipeline output        |
| ✅ Automated Metrics Reporting  | PR comments show accuracy diff vs `main` on every push |
| ✅ CI/CD Integration            | GitHub Actions runs `dvc repro` on every push          |
| ✅ Dependency-aware Execution   | DVC only reruns stages when deps change (MD5 check)    |
| ✅ Build Tooling                | Makefile for one-command install                       |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built as part of an MLOps coursework series — demonstrating DVC-based data versioning, reproducible ML pipelines, Google Drive remote storage, and automated metrics tracking integrated with GitHub Actions CI.
