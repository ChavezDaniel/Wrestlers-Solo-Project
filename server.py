from flask import render_template, session, redirect, request
from flask_app import app
from flask_app.controllers import wrestlers




if __name__ == "__main__":
    app.run(debug=True)