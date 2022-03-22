from pandas.core.indexes import category
from indussh import db, create_app
from indussh.models import Product
import pandas as pd

app = create_app()

columns = [
        'article_no', 'name', 'description', 'type', 'category', 
        'price', 'minimum_price', 'image_file', 'size_sm', 'size_md',
        'size_l', 'size_xl'
        ]

df = pd.read_csv('Upload-Ready-WebProducts.csv')
df.columns = columns

with app.app_context():   
    for i in range(len(df)):
        product = Product(
            article_no=df.iloc[i]['article_no'],
            name=df.iloc[i]['name'],
            description=df.iloc[i]['description'],
            type=df.iloc[i]['type'],
            category=df.iloc[i]['category'],
            price=df.iloc[i]['price'],
            minimum_price=df.iloc[i]['minimum_price'],
            image_file=df.iloc[i]['image_file'],
            size_sm=df.iloc[i]['size_sm'],
            size_md=df.iloc[i]['size_md'],
            size_l=df.iloc[i]['size_l'],
            size_xl=df.iloc[i]['size_xl']
        )

        db.session.add(product)
    db.session.commit()

print("Products table seeding done!")