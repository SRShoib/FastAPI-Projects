# 🏥 MediCore — Patient Management API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A **production-style FastAPI project** for managing patient health records with automatic health metric calculations.

This project demonstrates clean **REST API design**, modular architecture, and real-world backend development practices.

---

# ✨ Features

✔ CRUD operations for patients
✔ Automatic **patient ID generation** (`patient_001`, `patient_002`, ...)
✔ Automatic **health metric calculations**

* BMI
* BMI Category
* BMR (Basal Metabolic Rate)
* BSA (Body Surface Area)
* IBW (Ideal Body Weight)

✔ Sorting support
✔ JSON-based database
✔ Pydantic v2 validation
✔ RESTful API design

---

# 🧱 Project Architecture

```
MediCore
│
├── app
│   ├── __init__.py  
│   ├── main.py           # FastAPI entrypoint
│   ├── models.py         # Pydantic data models
│   ├── storage.py        # JSON database layer
│   │
│   └── routers
│       ├── __init__.py 
│       └── patients.py   # Patient API routes
│
├── database
│   └── patient_data.json
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| **FastAPI**       | Web framework                   |
| **Pydantic v2**   | Data validation & serialization |
| **Uvicorn**       | ASGI server                     |
| **Python 3.12**   | Runtime                         |
| **JSON Database** | Lightweight storage for demo    |

---

# 📸 API Demo

## Swagger UI

<img width="1171" height="911" alt="Swagger UI" src="https://github.com/user-attachments/assets/3fd05c1d-7c3c-4b84-8df9-4c45458408d4" />

# 🚀 Getting Started

## 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/medicore-api.git
cd medicore-api
```

---

## 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the API

```bash
uvicorn app.main:app --reload
```

Server starts at:

```
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates documentation.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Endpoints

| Method | Endpoint                 | Description           |
| ------ | ------------------------ | --------------------- |
| GET    | `/patients`              | Get all patients      |
| GET    | `/patients/{patient_id}` | Get a single patient  |
| POST   | `/patients`              | Create a patient      |
| PUT    | `/patients/{patient_id}` | Replace a patient     |
| PATCH  | `/patients/{patient_id}` | Update patient fields |
| DELETE | `/patients/{patient_id}` | Delete patient        |

---

# 🧮 Health Calculations

### BMI

```
BMI = weight_kg / (height_m²)
```

| BMI         | Category    |
| ----------- | ----------- |
| < 18.5      | Underweight |
| 18.5 – 24.9 | Normal      |
| 25 – 29.9   | Overweight  |
| ≥ 30        | Obese       |

---

### BMR (Mifflin-St Jeor)

Male

```
10 × weight + 6.25 × height_cm − 5 × age + 5
```

Female

```
10 × weight + 6.25 × height_cm − 5 × age − 161
```

---

### BSA (Mosteller)

```
sqrt((height_cm × weight_kg) / 3600)
```

---

### IBW (Devine)

Male

```
50 + 2.3 × (inches_over_5ft)
```

Female

```
45.5 + 2.3 × (inches_over_5ft)
```

---

# 🗄 Example Patient Record

```json
{
  "name": "Rahim Ahmed",
  "age": 25,
  "gender": "male",
  "home_town": "Dhaka",
  "height_m": 1.75,
  "weight_kg": 70,
  "height_cm": 175,
  "bmi": 22.86,
  "bmi_category": "Normal",
  "bmr_kcal_day": 1673,
  "bsa_m2": 1.85,
  "ibw_kg_est": 70.5,
  "created_at": "2026-03-05T10:30:00Z",
  "id": "patient_001"
}
```

---

# 📈 Future Improvements

* Add **SQLite / PostgreSQL database**
* Add **authentication (JWT)**
* Add **pagination**
* Add **filtering**
* Add **Docker support**
* Add **unit tests (pytest)**

---

# 👨‍💻 Author

Built with ❤️ using **FastAPI** for learning and demonstration.

If you like this project, ⭐ the repository.
