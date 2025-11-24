# Spoken Introduction Scoring Tool

This project is a simple Streamlit application that evaluates a student’s spoken introduction using a rubric.
The transcript is analysed using **rule-based checks**, **semantic similarity**, and **rubric weights** to generate an overall score out of 100 along with per-criterion feedback.

---

## ⭐ What This App Does

* Lets the user **paste** a transcript or **upload a .txt file**
* Automatically loads the **rubric** from `data/rubric.xlsx`
* Uses:

  * **Keyword matching**
  * **Word-count validation**
  * **Sentence-transformer embeddings** for semantic similarity
* Combines all signals using the rubric weights
* Displays:

  * Final score (0–100)
  * Per-criterion scoring table
  * Detailed feedback for each criterion
* Allows downloading the entire result as a **JSON file**

---

## 🗂 Project Structure

```
project/
│
├── app.py
├── scorer.py
├── rubric_loader.py
├── utils.py
│
├── requirements.txt
├── README.md
│
└── data/
    ├── rubric.xlsx
    └── sample.txt
```

---

## 🚀 How to Run the App Locally (VS Code)

1. Create and activate a virtual environment:

   ```
   py -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Start the app:

   ```
   streamlit run app.py
   ```
4. The app will open in your browser automatically.

---

## ☁️ Deploying on Streamlit Cloud

1. Push this project to a **public GitHub repository**
2. Go to **streamlit.io → Deploy app**
3. Select your repo and choose:

   ```
   app.py
   ```
4. Streamlit Cloud will install everything from `requirements.txt`
5. The app will be live in a few minutes

---

## 🧠 Technologies Used

* **Python**
* **Streamlit** (frontend + backend execution)
* **Sentence Transformers** (`all-MiniLM-L6-v2`)
* **Pandas / NumPy**
* **Scikit-learn** (cosine similarity)
* **OpenPyXL** for reading Excel rubric

---

## 📌 Notes

* The rubric file must remain in `data/rubric.xlsx` for the app to function.
* The app is designed to be simple, readable, and easy to maintain.
* You can modify the rubric or adjust scoring weights without changing the core logic.

---
