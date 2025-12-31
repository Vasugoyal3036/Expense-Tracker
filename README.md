# 💰 ExpenseFlow - Personal Expense Tracker

A beautiful, modern personal expense tracking application built with Flask.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **User Authentication** - Secure registration and login system
- **Expense Management** - Add, edit, and delete expenses
- **Smart Categories** - Organize expenses into intuitive categories
- **Visual Analytics** - Beautiful charts for spending insights
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Modern UI** - Glassmorphism design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
project/
├── app.py              # Main Flask application
├── helpers.py          # Database and utility functions
├── README.md           # Project documentation
├── templates/
│   ├── layout.html     # Base template
│   ├── index.html      # Dashboard page
│   ├── login.html      # Login page
│   └── register.html   # Registration page
└── static/
    └── styles.css      # Stylesheet
```

## 🎨 Features Overview

### Dashboard
- View total, monthly, and weekly expenses
- Interactive bar chart for monthly trends
- Doughnut chart for category breakdown
- Full transaction history with search

### Expense Categories
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Travel
- Other

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **Icons:** Font Awesome
- **Fonts:** Inter (Google Fonts)

## 📝 License

This project is open source and available under the MIT License.

---

Built with ❤️ using Flask
