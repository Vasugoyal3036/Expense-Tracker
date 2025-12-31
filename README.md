# ExpenseFlow – Personal Expense Tracker

#### Video Demo: (https://youtu.be/q0P9vEvaBhY)

## Description

ExpenseFlow is a web-based personal expense tracking application built as my final project for CS50. The goal of this project is to help users manage their daily expenses in a simple, organized, and visually appealing way. This application allows users to register an account, log in securely, record expenses, categorize them, and view spending summaries. The project focuses on usability, clarity, and real-world practicality.

This project was inspired by the need for a lightweight tool that helps individuals understand their spending habits without relying on complex financial software. ExpenseFlow provides a clean interface where users can focus on tracking expenses and reviewing their financial activity over time.

The project is built using Python with the Flask web framework. HTML, CSS, and JavaScript are used for the frontend, while SQLite is used as the database to store user and transaction data. The application demonstrates key concepts learned throughout CS50, including web development, databases, authentication, and software design.

---

## Features

- **User Authentication**  
  Users can register for an account and securely log in using hashed passwords.

- **Expense Management**  
  Users can add expenses with descriptions, categories, and amounts.

- **Transaction History**  
  All expenses are stored in a database and displayed in an organized table.

- **Category Organization**  
  Expenses can be grouped into categories such as food, transportation, entertainment, and more.

- **Responsive Design**  
  The application works smoothly on both desktop and mobile devices.

- **Clean User Interface**  
  A modern layout with readable typography and simple navigation enhances usability.

---

## Project Structure

The project consists of the following main files and folders:

- **app.py**  
  This is the core of the application. It defines all Flask routes, handles user authentication, processes form submissions, interacts with the database, and renders templates.

- **helpers.py**  
  Contains helper functions such as login validation and formatting utilities that keep the main application logic clean and modular.

- **templates/**  
  This directory contains all HTML templates used by the application:
  - `layout.html`: Base layout used across all pages.
  - `index.html`: Main dashboard displaying expenses.
  - `login.html`: Login page for users.
  - `register.html`: Registration page for new users.
  - `history.html`: Displays a history of recorded transactions.

- **static/**  
  Contains static assets such as CSS files used for styling the website.

- **database (SQLite)**  
  Stores user credentials and expense data. SQLite was chosen for its simplicity and reliability.

---

## Design Decisions

Flask was selected as the framework due to its lightweight nature and flexibility. It allows for clear separation between backend logic and frontend presentation. SQLite was chosen as the database because it does not require a separate server and integrates seamlessly with Flask, making it ideal for a small-scale project.

The user interface was designed to be minimal and intuitive. Rather than overwhelming users with unnecessary options, the focus was placed on essential functionality. Clear navigation and readable layouts help ensure a smooth user experience.

Security was also considered during development. Passwords are hashed before being stored, and user sessions are managed securely to prevent unauthorized access.

---

## What I Learned

This project helped me gain a deeper understanding of full-stack development. I learned how to connect frontend components with backend logic, manage user authentication, and store persistent data using a database. I also improved my debugging skills and learned how to structure a larger project in an organized and maintainable way.

Additionally, this project strengthened my confidence in building applications from scratch and reinforced the importance of planning, testing, and documentation.

---

## Conclusion

ExpenseFlow represents the culmination of my learning throughout CS50. It combines multiple concepts such as programming logic, database management, web development, and user interaction into a single functional application. I am proud of the progress I have made through this project and the skills I have developed along the way.

Thank you for reviewing my project!
