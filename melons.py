from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list=melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    # print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    # """TODO: Display the contents of the shopping cart. The shopping cart is a
    # list held in the session that contains all the melons to be added. Check
    # accompanying screenshots for details."""
    

    if not 'cart' in session:
        flash('Your cart is empty!')
        return render_template("cart.html")

    cart_list = []

    # session['cart'] == {1: 17, 2: 10}  # melon #1 is 17, #2 is has 10
    # cart_list == [(melon obj, 17), (melon obj, 10)]
    for melon_id, qty in session['cart'].items():
        melon = model.get_melon_by_id(melon_id)
        melon_tuple = (melon, qty)
        cart_list.append(melon_tuple)


    print cart_list

    final_price = total_price(cart_list)

    return render_template("cart.html", cart_list = cart_list, final_price= final_price)

@app.route("/add_to_cart/<string:melon_id>")
def add_to_cart(melon_id):
    # import pdb; pdb.set_trace()

    # """TODO: Finish shopping cart functionality using session variables to hold
    # cart list.

    # Intended behavior: when a melon is added to a cart, redirect them to the
    # shopping cart page, while displaying the message
    # "Successfully added to cart" """

    if not 'cart' in session:
        session['cart'] = {}
        session['cart'][melon_id]=1
        print "Here!"
    else:
        if session['cart'].get(melon_id) == None:
            flash('melon added!')
            session['cart'][melon_id] = 1
        else:
            session['cart'][melon_id] += 1
            flash('melon added!')

    cart_list = []

    for key in session['cart']:
        melon = model.get_melon_by_id(key)
        melon_tuple = (melon, session['cart'][key])
        cart_list.append(melon_tuple)

    print cart_list

    final_price = total_price(cart_list)

    return render_template("cart.html", cart_list = cart_list, final_price = final_price)


def total_price(cart_list):

    total_price = 0

    for melon, quantity in cart_list:
        price = quantity*melon.price
        total_price = total_price + price

    return total_price

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form"""
    email = request.form.get("email")
    password = request.form.get("password")

    cust = model.get_customer_by_email(email)
 
    if cust == None:
        flash('Login Unsuccessful')
        return render_template("login.html")
    else: 
        session["cust"] = cust.givenname

    # cust = model.Customer(email, password)
    # print cust.email, cust.password

    # if not 'login' in session:
    #     session['login'] = {}
    # if email not in session['login']:
    #     session['login'][email]=password
    #     print "yes!"
    #     print session['login']
    
    return render_template("index.html")


@app.route("/checkout")
def checkout():
    # """TODO Implement a payment system. For now, just return them to the main
    # melon listing page."""
    # flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    # return redirect("/melons")
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
