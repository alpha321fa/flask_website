from flask import Flask, render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Item, User
from shop.forms import LoginForm, RegistrationForm, CheckoutForm, SortForm
from flask_login import login_user, logout_user

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    form = SortForm()
    if form.sort_type.data == "price_high":
        items = Item.query.order_by(Item.price.desc())
    elif form.sort_type.data == "price_low":
        items = Item.query.order_by(Item.price.asc())
    elif form.sort_type.data == "eco_low":
        items = Item.query.order_by(Item.carbon.asc())
    return render_template('home.html', items=items, form=form)

@app.route("/item/<int:item_id>")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', item=item)

@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    if 'cart' not in session and not session["logged_in"]:
        flash("Please login to add items to basket.")
        return redirect(url_for('login'))
    item = Item.query.get_or_404(item_id)
    if item.name in session['cart']:
        session['cart'][item.name][0] += 1
        session['cart'][item.name][1] += item.price
    else:
        session['cart'][item.name] = [0,0,item.image]
        session['cart'][item.name][0] = 1
        session['cart'][item.name][1] = item.price
    flash("Item added to cart")
    return redirect(url_for('home'))

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if 'logged_in' not in session:
        session['logged_in'] = False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            session['cart'] = {}
            session['logged_in'] = True
            login_user(user)
            flash('You have successfully logged in.')
            return redirect(url_for('home'))
        else:
            return render_template('unsuccessful.html', title='Unsuccessful')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username_new.data, password=form.password_new.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/cart")
def cart():
    if 'cart' in session and session["logged_in"]:
        total_price = 0
        cart = session['cart']
        for item_name in cart:
            total_price += cart[item_name][1]
    else:
        cart = None
        total_price = 0
    return render_template('cart.html', title='Cart', cart=cart, total_price=total_price)

@app.route("/remove/<item_name>")
def remove(item_name):
    del session['cart'][item_name]
    flash('Item successfully removed from cart.')
    return redirect(url_for('cart'))

@app.route("/checkout", methods=['GET','POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        del session['cart']
        session['cart'] = {}
        return render_template('success.html', title='Success')
    return render_template('checkout.html', title='Checkout', form=form)

@app.route("/logout")
def logout():
    if session['logged_in']:
        session['logged_in'] = False
        del session['cart']
        logout_user()
        flash("Logout successful.")
    return redirect(url_for('home'))

