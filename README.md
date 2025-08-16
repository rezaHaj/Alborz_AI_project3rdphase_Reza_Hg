# Alborz_AI_project3rdphase_Reza_Hg
NeoScreenBot  —  A lightweight decision-support system that helps healthcare workers interpret newborn screening results for PKU and Congenital Hypothyroidism (CH) accurately, quickly, and based on Iran’s Ministry of Health guideline


# NeoScreenBot 🍼🤖

**An Intelligent Assistant for Newborn Screening of PKU and Congenital Hypothyroidism**

---

## 📌 Problem

In Iran, according to the Ministry of Health guidelines, every newborn must be screened for **Congenital Hypothyroidism (CH)** and **Phenylketonuria (PKU)** in their early days of life.

Currently:

* Results are interpreted manually.
* Healthcare staff (especially in rural/under-resourced areas) face difficulty following complex clinical algorithms.
* This can lead to **delayed diagnosis, wrong referrals, and preventable complications** like irreversible neurological damage.

---

## 💡 Our Solution: NeoScreenBot

NeoScreenBot is a **lightweight decision-support system** that helps healthcare workers interpret newborn screening results **fast, accurately, and consistently** according to the Ministry of Health’s official protocol.

✔️ Automates clinical decision trees
✔️ Reduces human error in result interpretation
✔️ Provides clear, standardized recommendations
✔️ Easy-to-use web or mobile interface

---

## ✨ Key Features

* 📊 **Input & Recommendation** → User enters screening results, system instantly gives standardized advice.
* 🎨 **UI Helpers** → Color-coded badges (`Normal`, `Repeat`, `Confirm`, `Urgent`) for clarity.
* 🧩 **Lightweight Implementation** → Uses Python + Flask/Streamlit, deployable even in low-resource settings.
* 🔒 **Safe** → No real patient data stored.

---

## 🏗️ Tech Stack

* **Core Logic:** Python
* **UI Framework:** Streamlit / Flask
* **Data Handling:** NumPy, Pandas
* **Rule Storage:** JSON / SQLite
* **Utilities:** Custom HTML helpers (for headers & badges)

---

## 📂 Repository Structure

```
NeoScreenBot/
│── core/            # Decision-making logic (CH & PKU protocols)
│── ui/              # Flask/Streamlit UI
│── utils/           # Presentational helpers (case_header, badge, etc.)
│── tests/           # Synthetic test cases
│── README.md        # Project documentation
```

---

## 🚀 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/NeoScreenBot.git
   cd NeoScreenBot
   ```
2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   streamlit run app.py
   ```
4. Open in browser:

   ```
   http://localhost:8501
   ```

---

## 📊 Evaluation Metrics

* **Accuracy:** ≥ 95% compared to official guidelines
* **Response Time:** < 5 seconds per case
* **User Satisfaction:** Positive feedback from pilot tests

---

## ⚠️ Ethical Considerations

* NeoScreenBot is a **decision support tool**, not a replacement for medical professionals.
* Future versions must ensure **data security** if real patient data is added.

---

## 👥 Team

* **Team Member:** Reza H.G. ([rhg1819@gmail.com](mailto:rhg1819@gmail.com))
* **Mentor:** Mr. Ali Shabestari

---

## 🔮 Future Work

* Adding support for more metabolic & genetic disorders
* Integration with national EHR systems
* AI-based anomaly detection for rare cases



📌 *NeoScreenBot = Fast, Accurate, Life-Saving Decisions for Newborns*

---

می‌خوای برات این README رو همون‌جوری Markdown آماده کنم (یعنی فایل `README.md` بسازم که مستقیم بندازی تو گیت و درست رندر بشه)، یا فقط متنش کافیه؟
