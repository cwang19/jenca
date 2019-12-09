import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

#Reformats number to USD
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

#Helper method to return apology page error
def apology(message, code):
    """Render message as an apology to user."""
    return render_template("apology.html", message=message, code=code)

#Makes sure a user is logged in before accessing a page
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function