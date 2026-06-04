# 📚 Smart Library Management System

<div align="center">

# 📖 Library Management System

### A Professional Python OOP + SQLite Based Library Management Solution

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![OOP](https://img.shields.io/badge/OOP-Object%20Oriented-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</div>

---

## 🚀 Overview

The **Smart Library Management System** is a Python-based application designed to manage library operations efficiently using **Object-Oriented Programming (OOP)** and **SQLite Database**.

The system enables administrators to manage books, users, issue-return transactions, and fine calculations while ensuring data persistence and modular code architecture.

This project demonstrates real-world implementation of:

- Object-Oriented Programming
- Database Management using SQLite
- SQL Queries
- Exception Handling
- Modular Software Design
- File Handling & Reporting

---

# ✨ Features

## 📖 Book Management

- Add New Books
- Remove Books
- Update Book Details
- Search Books
- View Available Books

---

## 👤 User Management

- Register New Users
- View User Information
- Manage User Records

---

## 🔄 Transaction Management

- Issue Books
- Return Books
- View Transaction History
- Track Borrowed Books

---

## 💰 Fine Calculation

- First 7 Days Free
- ₹5 Fine Per Day After Due Date
- Automatic Fine Generation

---

## 📊 Reporting & Analytics

- Total Books
- Available Books
- Issued Books
- Active Users
- Transaction Reports

---

# 🏗️ System Architecture

```text
                    Smart Library Management System

                                   Library
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
          Admin                     Book                  Transaction
             │                        │                        │
             └────────────── User Management ────────────────┘
                                      │
                                 SQLite Database
                                 
