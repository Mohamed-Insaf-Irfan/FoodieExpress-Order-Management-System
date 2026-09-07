# 🍔 FoodieExpress Order Management System

A desktop-based food order management system developed using Python, Tkinter, and SQLite3.

## 👨‍🎓 Student

**Mohamed Irfan Mohamed Insaf**

## 🛠️ Technologies Used

- Python
- Tkinter
- SQLite3
- Visual Studio Code

## ✨ Features

- Customer details management
- Food and quantity selection
- Membership options: Regular, Premium, and VIP
- Automatic bill calculation
- Delivery fee calculation
- Membership discounts
- Free delivery for orders above Rs. 5,000
- Save orders to SQLite database
- View saved order history
- Clear form and logout functions

## ▶️ How to Run

1. Install Python on your computer.
2. Open this repository folder in Visual Studio Code.
3. Run `foodieexpress.py` using Visual Studio Code or the terminal.
4. The FoodieExpress GUI will open.
5. Enter the customer and order details.
6. Click **Calculate Bill** to calculate the order.
7. Click **Save Order** to store the order in SQLite.
8. Click **View Orders** to view saved order history.

## 🗄️ Database

The application uses SQLite3 and stores its data in `foodie.db`. The Python application creates the required `customers` and `orders` tables automatically if they do not already exist.

## 📁 Project Structure

```text
FoodieExpress-Order-Management-System/
├── foodieexpress.py
├── foodie.db
├── README.md
├── requirements.txt
└── .gitignore
```

## 📌 Notes

Tkinter and SQLite3 are part of Python's standard library, so no external Python packages are required.