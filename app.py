from flask import Flask, render_template, flash
from form import NamerForm, UserForm

from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Rest of your code remains the same


# Create the Flask instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# secret key
app.config['SECRET_KEY'] = "Key"

# Initialize database
db = SQLAlchemy(app)

# Add database
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Creating a model


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %s>' % self.name


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User Added successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted successfully")
    return render_template('name.html', name=name, form=form)


# create custom error page
# invalid Url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Function to create tables


def create_tables():
    with app.app_context():
        db.create_all()


# Run the function to create tables
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
