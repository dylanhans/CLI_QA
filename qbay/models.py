from flask import Flask, sessions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TIMESTAMP
from email_validator import validate_email, EmailNotValidError
import re
from datetime import datetime
from sqlalchemy import exc
from sqlalchemy.sql.elements import Null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    """
    A class to represent someone who can buy or sell on the platform.
    .........
    Atributes
    ---------
    id : Integer
        A unique ID to identify the user in the database and app
    username : String
        A unique string display name for the user
    password : String
        A string password to allow the user to login
    email : String
        A string containing the user's email
    balance : Integer
        The user's current monetary balance in cents
    """
    email = db.Column(db.String(120), unique=True,
                      primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    balance = db.Column(db.Integer, unique=False, nullable=False)
    shipping_addr = db.Column(db.String(120), unique=False, nullable=False)
    postal_code = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Reviews(db.Model):
    """
    A class to represent the reviews on the platform.
    --------
    Attributes
    --------
    id : Integer
        A unique integer containing the review ID for the database
    content: String
        A string to represents the contents of the review
    subject: String
        A string to represent the title of the review
    poster: String
        A string to represent the user who posted the review
    timestamp: TIMESTAMP
        Time that the review was posted
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    poster = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(TIMESTAMP)

    def __repr__(self):
        return f"<Review {self.subject}>"


class Transactions(db.Model):

    """
    A class to represent the transactions on the platform.
    .........
    Atributes
    ---------
    id : Integer
        A unique integer containing the transaction ID for the database
    price : Integer
        An integer to represent the cost of the product being sold
    buyer : String
        A unique string display name for the buyer
    seller : String
        A unique string display name for the seller
    product_id : Integer
        An integer containing the product's unique id
    status : String
        The current status of the order (processed, shipped, etc.)
    timestamp : TIMESTAMP
        The time that the transaction occurred
    """
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, unique=False, nullable=False)
    buyer = db.Column(db.String(80), unique=False, nullable=False)
    seller = db.Column(db.String(80), unique=False, nullable=False)
    product_id = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.String(50), unique=False, nullable=False)
    timestamp = db.Column(TIMESTAMP)

    def __repr__(self):
        return f"<Transaction {self.ID}>"


class Product(db.Model):
    """
    A class to represent the products on the platform.
    --------
    Attributes
    --------
    id: Integer
        A unique integer containing the product ID for the database
    price: Integer
        A Integer to represent the cost of the product
    title: String
        A string to represent the name of the product
    desc: String
        A string to represent the product's description
    last_modified_date: Time stamp
        A timestamp to represent the last time a product was updated
    owner_email: String
        A string to represent the owners email
    """
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(2000), unique=False, nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    owner_email = db.Column(db.String(80), unique=False, nullable=False)
    last_modified_date = db.Column(TIMESTAMP)

    def __repr__(self):
        return f"<Product {self.id}>"


db.create_all()  # Create all tables


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''

    specialChar = ['!', '@', '#', '$', '%', '&', '*', '?']
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # R1-1: Both the email and password cannot be empty
    if not email or not password:  # Both should be strings, falsy when empty
        return False

    # R1-2/R1-7: Emails are unique / if the email is used, operation fails
    existing_users = User.query.filter_by(email=email).all()
    if len(existing_users) > 0:
        return False

    # R1-3: The email has to follow addr-spec defined in RFC 5322
    if (re.fullmatch(email_regex, email)) is None:
        return False

    # R1-4: Password has to meet the required complexity
    if (len(password) < 6 or password.lower() == password or password.upper()
            == password or password.isalpha() or
            not any(i in specialChar for i in password) or
            not any(i.isdigit() for i in password)):
        return False

    # R1-5: User name rules
    if not name or not re.match(r"^[ \w]+$", name) or name.strip() != name:
        return False

    # R1-6: User name size
    if len(name) <= 2 or len(name) > 20:
        return False

    # create a new user
    newuser = User(username=name, email=email, password=password)

    # R1-8: Shipping address is empty at the time of registration.
    newuser.shipping_addr = ""
    # R1-9: Postal code is empty at the time of registration.
    newuser.postal_code = ""
    # R1-10: Balance should be initialized as 100 at the time of registration.
    newuser.balance = 100

    # add it to the current database session
    db.session.add(newuser)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    specialChar = ['!', '@', '#', '$', '%', '&', '*', '?']

    # R1-1: email is not empty
    if email == '':
        return False

    # R1-3: email follows addr-spec define in RFC 5322
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return False

    # R1-1: password is not empty
    if password == '':
        return False

    # R1-4: password is at least 6 letters
    if len(str(password)) < 6:
        return False

    # R1-4: password has a number
    if not any(i.isdigit() for i in password):
        return False

    # R1-4: password has an uppercase letter
    if not any(i.isupper() for i in password):
        return False

    # R1-4: password has a lowercase letter
    if not any(i.islower() for i in password):
        return False

    # R1-4: password has a special character
    if not any(i in specialChar for i in password):
        return False

    # look in the database and return the user
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]


def user_update(current_username, **kwargs):
    '''
    Check update information
    Parameters:
        username (string): username
        shipping_address (string): user's address
        postal_code (string): user's postal
    Make use of regex.
    '''
    current_user = User.query.filter_by(username=current_username).first()

    # R3-1 Only specified tables can be updated.
    if not (all(k in kwargs for k in
            ("new_username", "new_shipping_address", "new_postal_code"))
            and len(kwargs) == 3):
        return False
        print("Incorrect Table")

    # R3-2 Shipping address should be alphanumeric-only,
    # and no special characters
    if (any(not c.isalnum() and not c.isspace()
            for c in kwargs['new_shipping_address'])
            or not(kwargs['new_shipping_address'])):
        print("Shipping address incorrect")
        return False

    # R3-3 Ensure it's a valid Canadian Postal Code
    regex = '[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9]'
    postal_pattern = re.match(regex, kwargs['new_postal_code'])
    if not(postal_pattern is not None and len(kwargs['new_postal_code']) == 7):
        print("Postal code incorrect")
        return False

    # R3-4 - Username Requirement
    if (not kwargs['new_username'] or
        not re.match(r"^[ \w]+$", kwargs['new_username'])
            or kwargs['new_username'].strip() != kwargs['new_username']):
        print("Username requirement failure.")
        return False

    if len(kwargs['new_username']) <= 2 or len(kwargs['new_username']) > 20:
        print("Length of username failure")
        return False

    if current_user is None:    # No such user exists
        print("User doesn't exist")
        return False

    current_user.username = kwargs['new_username']

    current_user.shipping_addr = kwargs['new_shipping_address']

    current_user.postal_code = kwargs['new_postal_code']

    try:
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        return e


def create_product(title, description, price, date, owner_email):
    '''
    Create a new product for listing
      Parameters:
        title (string):          product title
        description (string):    product description
        price (int):             product price
        date (int):              product last modified date
        owner_email(string):     product contact email
    '''
    if not date:
        date = datetime.today()
    # R4-1: The title of the product has to be alphanumeric-only, and space
    # allowed only if it is not as prefix and suffix.
    if not title or not re.match(r"^[ \w]+$", title) or title.strip() != title:
        return False

    # R4-2: The title of the product is no longer than 80 characters.
    # (Requirement of not empty is covered above by "if not title")
    if len(title) > 80:
        return False

    # R4-3: The description of the product can be arbitrary characters
    # with a minimum length of 20 characters and a maximum of 2000 characters.
    if len(description) < 20 or len(description) > 2000:
        return False

    # R4-4: Description has to be longer than the product's title.
    if len(title) >= len(description):
        return False

    # R4-5: Price has to be of range [10, 10000].
    if price <= 10 or price >= 10000:  # inclusive
        return False

    # R4-6: last_modified_date must be after 2021-01-02 and before 2025-01-02.
    if type(date) is str:
        year, month, day = map(int, date.split('-'))
        date = datetime(year, month, day)
    minDate = datetime(2021, 1, 2)  # assigns parameters to compare to date
    maxDate = datetime(2025, 1, 2)
    if date < minDate or date > maxDate:
        return False

    # R4-7: owner_email cannot be empty. The owner of the corresponding
    # product must exist in the database.
    if (owner_email == ''
            or len(User.query.filter_by(email=owner_email).all()) == 0):
        return False

    # R4-8: A user cannot create products that have the same title
    # duplicatieTitleExists return True if there is a product with the same
    # title, otherwise it returns False.
    duplicateTitleExists = db.session.query(
        Product).filter_by(title=title).first() is not None

    # check if duplicate title exists in the database
    if (duplicateTitleExists):
        return False

    # Create newProduct object to add to database
    newProduct = Product(
        title=title,
        desc=description,
        price=price,
        last_modified_date=date,
        owner_email=owner_email)

    # add it to the current database session
    db.session.add(newProduct)
    # actually save the product object

    try:
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        return e


def update_product(_id, **kwargs):
    '''
     Update a product in the database:
     Parameters:
        _id: id of the product you want to update
        newPrice: the new price of the product
        newTitle: the new title of the product
        newDesc: the new description of the product
    '''

    currentProduct = Product.query.filter_by(
        id=_id).first()  # find product in database from id

    # R5-1: One can update all attributes of the product, except owner_email
    # and last_modified_date.
    if not (all(k in kwargs for k in ("newPrice", "newTitle", "newDesc"))
            and len(kwargs) == 3):
        return False

    # R5-2: Price can be only increased but cannot be decreased :)
    if (kwargs["newPrice"] < currentProduct.price):
        return False

    # R5-4: When updating an attribute, one has to make sure that it follows
    # the same requirements as above.

    # R4-1: The title of the product has to be alphanumeric-only, and space
    # allowed only if it is not as prefix and suffix.
    if (not re.match(r"^[ \w]+$", kwargs["newTitle"])
            or kwargs["newTitle"].strip() != kwargs["newTitle"]):
        return False

    # R4-2: The title of the product is no longer than 80 characters and not
    # empty.
    if len(kwargs["newTitle"]) > 80 or not kwargs["newTitle"]:
        return False

    # R4-3: The description of the product can be arbitrary characters
    # with a minimum length of 20 characters and a maximum of 2000 characters.
    if len(kwargs["newDesc"]) < 20 or len(kwargs["newDesc"]) > 2000:
        return False

    # R4-4: Description has to be longer than the product's title.
    if len(kwargs["newTitle"]) >= len(kwargs["newDesc"]):
        return False

    # R4-5: Price has to be of range [10, 10000].
    if kwargs["newPrice"] <= 10 or kwargs["newPrice"] >= 10000:  # inclusive
        return False

    # R4-8: A user cannot create products that have the same title
    if (db.session.query(Product).filter_by(title=kwargs["newTitle"]).first()
            is not None and currentProduct.title != kwargs["newTitle"]):
        return False

    currentProduct.price = kwargs["newPrice"]
    currentProduct.title = kwargs["newTitle"]
    currentProduct.desc = kwargs["newDesc"]

    # R5-3: last_modified_date should be updated when the update operation is
    # successful.
    currentProduct.last_modified_date = datetime.today()

    try:
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        return e


def purchase_product(productTitle, email):
    '''
    this function is the backend for making orders on products.
    to make a purchase:
        1. productTitle: title of the product
        2. email: user email address
    '''

    # get product that wants to be purchased
    product = Product.query.filter_by(title=productTitle).first()
    user = User.query.filter_by(email=email).first()

    # owner of the product can't purchase his own product
    if (user.email == product.owner_email):
        return "Cannot make an order on your own products"

    # A user cannot place an order that costs more than his/her balance.
    if (user.balance < product.price):
        return "You don't have enough balance to purchase this item"

    # create transaction
    newTransaction = Transactions(price=product.price,
                                  buyer=user.email,
                                  seller=product.owner_email,
                                  product_id=product.id)

    newTransaction.status = ""  # initialized as an empty string

    # add it to the current database session
    db.session.add(newTransaction)
    # actually save the transaction object
    db.session.commit()

    return True
