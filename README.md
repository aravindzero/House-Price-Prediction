# 🏠 House Price Prediction System

A full-stack machine learning application that predicts California house prices using a **Random Forest Regressor** trained on the [California Housing dataset](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset). The project features a **Flask REST API** backend and a vanilla **HTML/CSS/JS** frontend.

---

## 📁 Project Structure

```
Py_Project/
├── backend/
│   ├── app.py               # Flask API server
│   ├── train_model.py        # Model training script
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # UI markup
│   ├── style.css             # Styling
│   └── main.js               # Frontend logic (API calls, formatting)
├── model/
│   ├── model.joblib           # Trained model artifact (~193 MB)
│   └── metrics.json           # Evaluation metrics (MAE, R²)
├── .gitignore
└── README.md                  # ← You are here
```

---

## ✨ Features

| Area      | Details                                                                 |
|-----------|-------------------------------------------------------------------------|
| **Model** | Random Forest Regressor (300 trees, scikit-learn)                       |
| **API**   | Flask REST API with health-check, model-info, and prediction endpoints  |
| **UI**    | Responsive form with instant USD & INR price display                    |
| **Metrics** | MAE ≈ 0.336 (×$100k) · R² ≈ 0.80                                    |

---

## 🛠️ Prerequisites

- **Python 3.9+**
- **pip** (comes with Python)
- A modern web browser (Chrome, Edge, Firefox, etc.)

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Py_Project
```

### 2. Create & activate a virtual environment

```bash
# Create
python -m venv .venv

# Activate (Windows – PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Windows – CMD)
.venv\Scripts\activate.bat

# Activate (macOS / Linux)
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Train the model *(optional — a pre-trained model is already included)*

```bash
python backend/train_model.py
```

This downloads the California Housing dataset, trains the model, and saves `model/model.joblib` and `model/metrics.json`.

### 5. Start the backend server

```bash
python backend/app.py
```

The API will be available at **http://127.0.0.1:5000**.

### 6. Open the frontend

Open `frontend/index.html` directly in your browser:

```bash
# Windows
start frontend/index.html

# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html
```

> **Tip:** You can also use a local HTTP server for a more realistic setup:
> ```bash
> cd frontend
> python -m http.server 8080
> ```
> Then visit **http://localhost:8080** in your browser.

---

## 🌐 API Reference

| Method | Endpoint       | Description                          |
|--------|----------------|--------------------------------------|
| GET    | `/health`      | Health check — returns `{"status": "ok"}` |
| GET    | `/model-info`  | Returns feature list and evaluation metrics |
| POST   | `/predict`     | Accepts feature values, returns predicted price |

### `POST /predict` — Example

**Request:**

```json
{
  "median_income": 8.3,
  "avg_rooms": 6.9,
  "avg_bedrooms": 1.0,
  "population": 322,
  "house_age": 42,
  "latitude": 37.88,
  "longitude": -122.23
}
```

**Response:**

```json
{
  "prediction": 4.526,
  "currency": "100k USD"
}
```

> The prediction value is in **$100k units** (the dataset's native scale).  
> Multiply by 100,000 to get the dollar amount — e.g. `4.526 → $452,600`.

---

## 📊 Input Features

| Feature          | Description                             | Example |
|------------------|-----------------------------------------|---------|
| `median_income`  | Median household income (×$10k)         | 8.3     |
| `avg_rooms`      | Average number of rooms per household   | 6.9     |
| `avg_bedrooms`   | Average number of bedrooms per household| 1.0     |
| `population`     | Block group population                  | 322     |
| `house_age`      | Median house age in years               | 42      |
| `latitude`       | Block group latitude                    | 37.88   |
| `longitude`      | Block group longitude                   | -122.23 |

---

## 🧰 Tech Stack

- **Backend:** Python · Flask · scikit-learn · NumPy · pandas · joblib
- **Frontend:** HTML5 · CSS3 · Vanilla JavaScript
- **ML Model:** `RandomForestRegressor` (scikit-learn 1.4.2)

---

## 📝 License

This project is for educational / academic purposes.
