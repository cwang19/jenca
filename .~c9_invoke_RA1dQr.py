import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from calendar import monthrange
from cs50 import SQL
from flask import Flask, Markup, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///jenca.db")


# Register Users
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure valid (i.e., >0) budget amount was submitted
        if not request.form.get("budget"):
            return apology("Must input budget", 403)
        elif float(request.form.get("budget")) <= 0:
            return apology("Budget must be greater than 0", 403)

        # Ensure unique username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        elif request.form.get("username") in db.execute("SELECT username FROM users;"):
            return apology("Username already taken", 403)

        # Ensures password must be at least 5 characters long with at least 1 special character and 1 number
        # Ensures password was submitted and password matches confirmation
        if not request.form.get("password"):
            return apology("Must provide password", 403)

        elif request.form.get("password").isalnum():  # if contains special characters
            return apology("Password must contain at least 1 special character", 403)

        elif len(request.form.get("password")) < 5:  # checks length of password
            return apology("Password must be at least 5 characters long", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Psswords must match", 403)  # checks if passwords match

        for char in request.form.get("password"):  # checks if password contains at least 1 number
            if char.isdigit():
                # if all conditions are met, register the new user by inputting the information into the "users" SQL database
                db.execute("INSERT INTO users (username, hash, budget) VALUES (?, ?, ?);", request.form.get(
                    "username"), generate_password_hash(request.form.get("password")), request.form.get("budget"))

                return render_template("login.html")

        # else, return apology if password does not contain a number
        return apology("Password must contain at least 1 number", 403)

    else:
        return render_template("register.html")


# copied from CS50 Finance: logs in user
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# creates the dashboard
@app.route("/")
@login_required
def index():

    # queries the "users" SQL table for the initial budget
    init_budget = (db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"]))[0]["budget"]

    # find first and last date of the current month
    # used https://www.mytecbits.com/internet/python/first-day-of-the-month
    current_date = datetime.today().date()
    first_day_of_month = current_date.replace(day=1)

    # used https://www.mytecbits.com/internet/python/get-last-day-of-month
    last_day_of_month = current_date.replace(day = monthrange(current_date.year, current_date.month)[1])

    # variable representing how much has been spent so far
    monthly_expenses = 0

    # for pie chart:
    labels = []
    values = []
    # selected colors for the pie chart: mint, purple, pink, yellow, orange, sky blue, lime, cornflower blue, light green
    colors = ["#aff8db", "#a79aff", "#f6a6ff", "#fff5ba", "#ffabab", "#85e3ff", "#bffcc6", "#e7ffac", "#afcbff"]

    # queries the "expenses" SQL database for a list of categories the user spent money in during the past month
    categories_list = db.execute("SELECT DISTINCT category FROM expenses WHERE user_id = ?;", session["user_id"])

    # will contain a list of dictionaries of what categories have been used, how much has been spent in each category, and the "recent" list
    category_expenses = []

    # will contain the five most recent transactions in each category
    recent = []
    for i in categories_list:

        category = i["category"]

        # checks if user is logging expense or adding money

        # if user is not adding money:
        if category != "Raise":

            # add the category to the pie chart
            labels.append(category)

            # query the SQL database for how much money has been spent in that category
            expense = db.execute("SELECT SUM(cost) FROM expenses WHERE user_id = ? AND category = ? AND date BETWEEN ? AND ?;", session["user_id"], category, first_day_of_month, last_day_of_month)

            # query the SQL database for the 5 most recent purchases in each category (dictionary with description, cost, date)
            recent = db.execute("SELECT description, cost, date FROM expenses WHERE user_id = ? AND category = ? AND date BETWEEN ? AND ? ORDER BY date DESC LIMIT 5;", session["user_id"], category, first_day_of_month, last_day_of_month)

            # calculates the total amount of money spent in each category as a percentage
            # adds how much money has been spent in a category to the monthly expenses
            # adds the value to the pie chart
            if not expense[0]["SUM(cost)"]:
                percentage = 0
                total = 0
                values.append(0)
            else:
                total = expense[0]["SUM(cost)"]
                monthly_expenses += total
                percentage = '{0:.2f}%'.format((total / init_budget * 100))
                values.append(float(expense[0]["SUM(cost)"]))

            # adds the category, total amount spent, and 5 most recent purchases (in the form of a list) to the "category_expenses" list
            category_expenses.append({"category": category, "total": usd(total), "recent": recent, "percentage": percentage})

        # if the category is a raise in monthly budget
        else:
            raises = db.execute("SELECT SUM(cost) FROM expenses WHERE user_id = ? AND category = ? AND date BETWEEN ? AND ?;", session["user_id"], category, first_day_of_month, last_day_of_month)[0]["SUM(cost)"]
            if not raises:
                pass

            # increase that month's budget by the amount of money inputted as a "raise"
            else:
                init_budget += raises

    amt_left = init_budget - monthly_expenses

    return render_template("index.html", set=zip(values, labels, colors), monthlybudget=usd(init_budget), left=usd(amt_left), spent=usd(monthly_expenses), category_expenses=category_expenses)


# Log new expense
@login_required
@app.route("/new_expense", methods=["GET", "POST"])
def newexpense():
    """Log New Expense"""
    if request.method == "POST":

        # checks that a category is selected from the dropdown
        if not request.form.get("category"):
            return apology("Must select category", 403)

        # checks that the cost of the product/transaction is inputted and greater than $0
        elif not request.form.get("cost"):
            return apology("Must input dollar amount of expense", 403)
        elif float(request.form.get("cost")) <= 0:
            return apology("Expenditure must cost more than $0", 403)

        # checks that a description and date are given
        elif not request.form.get("description"):
            return apology("Must include description of expense", 403)
        elif not request.form.get("date"):
            return apology("Must include date", 403)

        # run a SQL command to insert the new transaction (using data submitted in the form) into the "expenses" SQL database
        category = request.form.get("category")
        cost = float(request.form.get("cost"))
        description = request.form.get("description")
        date = request.form.get("date")
        user_id = session["user_id"]
        db.execute("INSERT INTO expenses (user_id, cost, description, category, date) VALUES (?, ?, ?, ?, ?);", user_id, cost, description, category, date)
        return redirect("/")
    else:
        return render_template("new_expense.html")


# change monthly budget
@login_required
@app.route("/changebudget", methods=["GET", "POST"])
def change_budget():
    """Change monthly budget"""

    # finds current budget (as listed in the "users" SQL database)
    original_budget = db.execute("SELECT budget FROM users WHERE id = ?;", session["user_id"])
    current = original_budget[0]["budget"]

    if request.method == "POST":
        # ensures that the users inputs a new budget value and a confirmation
        if not request.form.get("budget"):
            return apology("Must input new monthly budget category", 403)
        elif not request.form.get("confirmation"):
            return apology("Must confirm budget change", 403)

        # checks that the new budget is greater than $0
        elif float(request.form.get("budget")) <= 0:
            return apology("Budget must be greater than $0", 403)

        # checks if the new budget equals the confirmation value
        elif request.form.get("budget") != request.form.get("confirmation"):
            return apology("Changes to budget must match", 403)

        # runs a SQL command to update the budget corresponding to the current user
        db.execute("UPDATE users SET budget = ? WHERE id = ?;", float(request.form.get("budget")), session["user_id"])
        return render_template("changebudget.html", current=usd(float(request.form.get("budget"))))

    else:
        return render_template("changebudget.html", current=usd(current))


# monthly history page that filters based on category
@app.route("/month_history/<category>")
@login_required
def month_history(category):
    """Show monthly history of expenses"""

    # find first and last date of the current month
    # used https://www.mytecbits.com/internet/python/first-day-of-the-month
    current_date = datetime.today().date()
    first_day_of_month = current_date.replace(day=1)

    # used https://www.mytecbits.com/internet/python/get-last-day-of-month
    last_day_of_month = current_date.replace(day = monthrange(current_date.year, current_date.month)[1])

    if category is not "null":
        # query SQL database for all expenses in that category from the current month
        all_expenses = db.execute(
         "SELECT category, description, cost, date, notes FROM expenses WHERE user_id = ? AND category = ? AND date BETWEEN ? AND ? ORDER BY date DESC;", session["user_id"], category, first_day_of_month, last_day_of_month)

        # organizes results from SQL query into a list accessed by history.html
        # the dictionary for each transaction includes the category, description, cost, date, and notes
        history = []
        for i in range(len(all_expenses)):
            history.append({"category": all_expenses[i]["category"], "description": all_expenses[i]["description"],
                            "expense":"$" + '{:,.2f}'.format(all_expenses[i]["cost"]), "date": all_expenses[i]["date"], "notes": all_expenses[i]["notes"]})

        return render_template("month_history.html", history=history)


#monthly history page
@app.route("/history")
@login_required
def history():

    # find first and last date of the current month
    # used https://www.mytecbits.com/internet/python/first-day-of-the-month
    current_date = datetime.today().date()
    first_day_of_month = current_date.replace(day=1)

    # used https://www.mytecbits.com/internet/python/get-last-day-of-month
    last_day_of_month = current_date.replace(day = monthrange(current_date.year, current_date.month)[1])

    # queries SQL database for catgeory, descriptionn, cost, date, and notes for each expense logged in the current month
    expenses = db.execute(
         "SELECT category, description, cost, date, notes FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date DESC;", session["user_id"], first_day_of_month, last_day_of_month)

    # creates a "history" list where a dictionary of all expenses in the current month are added
    history = []
    for i in range(len(expenses)):
        history.append({"category": expenses[i]["category"], "description": expenses[i]["description"],
                        "expense":"$" + '{:,.2f}'.format(expenses[i]["cost"]), "date": expenses[i]["date"], "notes": expenses[i]["notes"]})

    return render_template("history.html", history=history)


#full transactional history page: all categories, all time
@app.route("/full_history")
@login_required
def full_history():
    """Show full history of expenses"""

    # SQL query for all expenses
    all_expenses = db.execute(
        "SELECT category, description, cost, date, notes FROM expenses WHERE user_id = ? ORDER BY date DESC;", session["user_id"])

    # organizes results from SQL query into a list accessed by history.html
    # collects category, description, cost, date, and notes associated with each expense
    history = []
    for i in range(len(all_expenses)):
        history.append({"category": all_expenses[i]["category"], "description": all_expenses[i]["description"],
                        "expense":"$" + '{:,.2f}'.format(all_expenses[i]["cost"]), "date": all_expenses[i]["date"], "notes": all_expenses[i]["notes"]})

    return render_template("full_history.html", history=history)


# Logs users out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")