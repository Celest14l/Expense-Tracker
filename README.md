# 💸 Multi-Bank Expense Tracker

A simple, elegant, and powerful personal expense tracker built using **Flask**, **SQLite**, and **Chart.js**. It supports **multiple bank accounts (SBI & BOB)**, real-time balance tracking, category-based breakdown, monthly charts, and more!

---

## 🚀 Features

- 🔄 Track expenses across multiple banks (SBI and BOB)
- 🏦 Set and update bank-wise total balances
- 📝 Add, view, and delete expenses
- 📊 Monthly category-wise expense pie chart
- ⬆️⬇️ Sort expenses by amount (ascending or descending)
- 🔍 Filter expenses by bank
- 🌈 Clean UI with Tailwind CSS styling

---

## 📂 Project Structure

expense-tracker/ │ ├── app.py # Flask backend logic ├── templates/ │ └── index.html # Main HTML page with embedded Tailwind CSS & Chart.js ├── static/ │ └── ... (optional for styling or JS files) ├── expenses.db # SQLite database (auto-generated) └── README.md # You are here!

yaml
Copy
Edit

---


📦 Database Schema
expenses table:

id (INT, Primary Key)

amount (REAL)

category (TEXT)

description (TEXT)

date (TEXT)

bank (TEXT)

balances table:

bank (TEXT, Primary Key)

balance (REAL)

📈 Future Enhancements
Export data to Excel/CSV

Add user login/authentication

Monthly summary and trend analysis

Responsive mobile design

🛠️ Built With
Python

Flask

SQLite

Tailwind CSS

Chart.js

