# 🍽️ Restaurant Reservation System
A simple web-based restaurant reservation system built with Python Flask for the backend and MySQL for data storage. It allows users to create, view, edit, and delete reservation records through a user-friendly interface.

## 📖 Table of Contents

- [Introduction](##introduction)
- [Features](##features)
- [Installation](##installation)
- [Usage](##usage)
- [Database Configuration](##database-configuration)
- [Tech Stack](##tech-stack)
- [Project Structure](##project-structure)

## 📘 Introduction

This project is a basic reservation management system for restaurants. It uses **Flask** to handle backend routing and logic, connects to a **MySQL database**, and optionally includes a frontend powered by HTML/CSS/JS with **npm** for dependency management.

---

## 🚀 Features

- 🔍 View all reservations  
- ➕ Create new reservations  
- ✏️ Edit existing reservations  
- ❌ Delete/cancel reservations

---

## 🧪 Usage
▶️ Start Flask Backend
```text
python app.py
```
▶️ Start Frontend Development Server
```text
npm start
```
Once both servers are running, open your browser and go to:
```text
http://localhost:3000
```

---

## 🧾 Database Configuration
1. Create MySQL Database
Use MySQL Workbench or your preferred tool to create a database named (for example) reservation_db.

Example table schema:
```text
CREATE DATABASE reservation_db;

USE reservation_db;

CREATE TABLE reservations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  people INT NOT NULL
);
```
2. Update MySQL Credentials in Code
Open app.py and update the database connection section with your own credentials:
```text
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",
    database="reservation_db"
)
```
Make sure your MySQL server is running before launching the app.

---

## 🧰 Tech Stack
Backend: Python 3 + Flask

Database: MySQL 

Frontend: HTML, CSS

Tools: npm, Node.js

---

## 📁 Project Structure

```text
restaurant-reservation/
│
├── app.py                   # Main Flask application
├── templates/               # HTML templates
├── static/                  # CSS/JS static files
├── requirements.txt         # Python dependencies
├── package.json             # npm dependencies
├── schema.sql               # Optional: SQL schema file
└── README.md                # Project documentation
```




