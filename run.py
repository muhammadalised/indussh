from indussh import create_app, db
from indussh.models import User, Customer, Product, Order, OrderItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Customer=Customer, Product=Product, Order=Order, OrderItem=OrderItem)