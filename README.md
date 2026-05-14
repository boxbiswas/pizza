# PizzaTime — Django demo

PizzaTime is a minimal Django demo for browsing pizzas, adding them to a cart, and placing orders.

Features:
- User registration & login
- DB-driven pizza menu
- Shopping cart and orders

Tech: Python, Django, SQLite, Bootstrap 5

Quick start (Windows):
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt  # or `pip install django`
python manage.py migrate
python manage.py runserver
```

Optional: `python manage.py createsuperuser` to manage pizzas via admin.

Note: This is the first demo project using Django — created for learning and demonstration.
