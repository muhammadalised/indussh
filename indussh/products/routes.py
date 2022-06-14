from flask import render_template, redirect, url_for, Blueprint, request, session, jsonify
from indussh.models import Product, Customer, Order, OrderItem
from indussh.products.forms import BillingForm
from indussh.products.recommender import Recommender
from indussh import db
import pandas as pd

products = Blueprint('products', __name__)

@products.route('/')
def shop():
    page = request.args.get('page', 1, type=int)
    categories = [c[0] for c in Product.query.with_entities(Product.category).distinct()]
    types={}
    for category in categories:
        types[category] = [t[0] for t in Product.query.filter_by(category=category).with_entities(Product.type).distinct()]
    
    products = Product.query.order_by(Product.added_on.desc()).paginate(page=page, per_page=9)

    return render_template('shop.html', products=products, categories=categories, types=types)

@products.route('/product/<string:article_no>')
def shop_single(article_no):
    # Get the product data
    product = Product.query.filter_by(article_no=article_no).first()
    # Get the recommendations for the product
    recommendations = get_product_recommendations(article_no=article_no)

    return render_template('shop-single.html', product=product, recommendations=recommendations)

def get_product_recommendations(article_no):
    # Get the sql query
    sql = db.session.query(Product).with_entities(Product.id, 
                                                    Product.article_no, 
                                                    Product.name, 
                                                    Product.description,
                                                    Product.type,
                                                    Product.category).statement
    # Read the data from database using pandas
    prods = pd.read_sql(sql, db.session.bind)

    # Extract and combine the features for the recommendation system
    prods['details'] = prods['name'] + ' ' + prods['category'] + ' ' + prods['type'] + ' ' + prods['description']
    # Drop the columns after extracting the features
    prods.drop(['name', 'category', 'type', 'description'], axis=1, inplace=True)
    # Initialize the recommender instance
    recommender = Recommender(prods)
    # Get recommendation results
    recommendation_results = recommender.recommend(article_no, 10)
    # Get Article no's of recommended products
    rec_prods_nos = [rec[1] for rec in recommendation_results]

    return Product.query.filter(Product.article_no.in_(rec_prods_nos)).all()

@products.route('/<string:category>')
def shop_by_category(category):
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category).order_by(Product.added_on.desc()).paginate(page=page, per_page=9)
    types=[]
    types = [t[0] for t in Product.query.filter_by(category=category).with_entities(Product.type).distinct()]
    return render_template('shop-by-category.html', products=products, category=category, types=types)

@products.route('/<string:category>/<string:type>')
def shop_by_type(category, type):
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category, type=type).order_by(Product.added_on.desc()).paginate(page=page, per_page=9)
    types=[]
    types = [t[0] for t in Product.query.filter_by(category=category).with_entities(Product.type).distinct()]
    return render_template('shop-by-type.html', products=products, type=type, category=category, types=types)

@products.route('/addtocart', methods=['POST'])
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

@products.route('/cart')
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

@products.route('/removecartitem/<string:article_no>')
def remove_from_cart(article_no):
    if article_no in session['cart']:
        session['cart'].pop(article_no)
        if len(session['cart'].items()) <= 0:
            session.clear()
        return redirect(url_for('products.cart'))


@products.route('/checkout', methods=['GET', 'POST'])
def checkout():
     if 'cart' in session:
        cart_prods = list(session['cart'].keys())
        products = Product.query.filter(Product.article_no.in_(cart_prods)).all()
        total = int(calculate_total_amount(products))

        form = BillingForm()

        if form.validate_on_submit():
            
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


@products.route('/completed')
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