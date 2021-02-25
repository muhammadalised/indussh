from flask import render_template, redirect, url_for, Blueprint, request, session, jsonify
from indussh.models import Product, Customer, User, Order, OrderItem
from indussh.products.forms import BillingForm
from indussh import db, bcrypt

products = Blueprint('products', __name__)

@products.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.added_on.desc()).paginate(page=page, per_page=9)
    return render_template('shop.html', products=products)

@products.route('/shop/product/<string:article_no>')
def shop_single(article_no):
    product = Product.query.filter_by(article_no=article_no).first()
    return render_template('shop-single.html', product=product, recommendations=[])

@products.route('/shop/<string:category>')
def shop_by_category(category):
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category).order_by(Product.added_on.desc()).paginate(page=page, per_page=9)
    return render_template('shop-by-category.html', products=products, category=category)

@products.route('/shop/addtocart', methods=['POST'])
def add_to_cart():
    article_no = request.form['article_no']
    size_selected = request.form['size']
    quantity = int(request.form['quantity'])
    
    if 'discount_price' in session:
        disc_price = session['discount_price']
    else:
        disc_price = 0

    if size_selected and quantity and size_selected != 'nosize' and quantity > 0:
        # Cart Session Starts here
        if 'cart' in session:
            # if product is not in the cart then add it
            if not any(article_no in p for p in session['cart']):
                session['cart'].update({article_no: [quantity, size_selected, disc_price]})
                return jsonify({'success': 'Product added to cart!'})
            # if the product is already in the cart, update the quantity
            elif any(article_no in p for p in session['cart']):
                session['cart'][str(article_no)][0] += quantity
                return jsonify({'success': 'Product already in the cart so quantity updated!'})
        else:
            # start the cart if already not created and add the product in it.
            session['cart'] = { article_no: [quantity, size_selected, disc_price] }
            return jsonify({'success': 'Product added to cart!'})
   
    return jsonify({'error': 'Please select size and quantity'})

@products.route('/shop/cart')
def cart():
    cart_prods = []
    if 'cart' in session:
        cart_prods = list(session['cart'].keys())
        products = Product.query.filter(Product.article_no.in_(cart_prods)).all()
        total = int(calculate_total_amount(products))
        return render_template('cart.html', products=products, total=total)
    return render_template('cart.html')

def calculate_total_amount(products):
    cart_products = session['cart']
    total_amount = 0
    for product in products:
        if product.article_no in cart_products:
            article_no = product.article_no
            quantity = cart_products[article_no][0]
            # app.logger.info(p)
            if cart_products[article_no][2] != 0:
                price = cart_products[article_no][2]
            else:
                price  = product.price
                
            total_amount += (int(quantity) * int(price))
    
    return total_amount
    # session.pop('discount_price', None)

@products.route('/shop/removecartitem/<string:article_no>')
def remove_from_cart(article_no):
    if article_no in session['cart']:
        session['cart'].pop(article_no)
        if len(session['cart'].items()) <= 0:
            session.clear()
        return redirect(url_for('products.cart'))


@products.route('/shop/checkout', methods=['GET', 'POST'])
def checkout():
     if 'cart' in session:
        cart_prods = list(session['cart'].keys())
        products = Product.query.filter(Product.article_no.in_(cart_prods)).all()
        total = int(calculate_total_amount(products))

        form = BillingForm()

        if form.validate_on_submit():
            # If create account is checked
            if request.form.get('c_create_account'):
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(email=form.email.data,
                            password=hashed_password
                            )
                db.session.add(user)
                db.session.commit()

                customer = Customer(name=form.name.data,
                                    address=form.address.data,
                                    city=form.city.data,
                                    postcode=form.postcode.data,
                                    email=form.email.data,
                                    phone_number=form.phone_number.data,
                                    user_id=user.id
                                    )
                db.session.add(customer)
            else:
                customer = Customer(name=form.name.data,
                                    address=form.address.data,
                                    city=form.city.data,
                                    postcode=form.postcode.data,
                                    email=form.email.data,
                                    phone_number=form.phone_number.data
                                    )
                db.session.add(customer)
            db.session.commit()

            # Create an order
            order = Order(amount=total, customer_id=customer.id, notes=form.notes.data)
            db.session.add(order)

            # Add the items in order items
            for article_no in cart_prods:
                product = Product.query.filter_by(article_no=article_no).first()
                order_item = OrderItem(quantity=session['cart'][str(article_no)][0], 
                                        discounted_price=session['cart'][str(article_no)][2],
                                        product_id=product.id,
                                        order_id=order.id
                                        )
                db.session.add(order_item)
            
            db.session.commit()
            session.clear()
            return redirect(url_for('products.thanks'))
            
        return render_template('checkout.html', products=products, total=total, form=form)


@products.route('/shop/completed')
def thanks():
    return render_template('thankyou.html')

@products.route('/shop/search-results', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)
    
    if request.method == 'POST':
        search_query = request.form.get('search-query')
        session['search-query'] = search_query
    elif 'search-query' in session:
        search_query = session['search-query']

    products = Product.query.filter(Product.name.like('%' + search_query + '%')).paginate(page=page, per_page=9)
    results_count = Product.query.filter(Product.name.like('%' + search_query + '%')).count()
    
    return render_template('search-results.html', search_query=search_query, products=products, results_count=results_count)