
from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field
app = FastAPI()



# ══ DATA ══════════════════════════════════════════════════════════

products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},

    {'id': 2, 'name': 'Notebook',       'price':  99, 'category': 'Stationery',  'in_stock': True},

    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True},

]

@app.get('/products/search')
def search_products(
    keyword: str = Query (..., description = "ENNTER WORD TO SEARCH")
):
    results =[
        p for p in products
        if keyword.lower() in p['name'].lower()
    ]

    if not results :
        return {'message ': f'no products found for :{keyword}', 'results': []}
    
    return {
        'keyword' : keyword,
        'total_found' : len(results),
        'results': results,
    }

@app.get('/products/sort')
def sort_products(
    sort_by: str =Query(..., description = "price or name"),
    order : str= Query(..., description="ASC or DESC")
):
    if sort_by not in ['price' , 'name']:
        return {'error ': "sort must be 'price' or 'name' "}
    if order not in ['asc','desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    
    if (order == 'desc'):
        sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=True)
    else:
        sorted_products = sorted(products, key=lambda p: p[sort_by])

    return {
        
    'sort_by':  sort_by,

    'order':    order,

    'products': sorted_products,
    }

@app.get('/products/page')
def get_products_paged(
    page: int=Query(1, ge=1 ,description ='page number'),
    limit : int = Query (2, ge =1 , le =20, description = 'item per page'),
):
    start  = (page - 1) * limit
    end = start + limit 
    paged = products[start:end]

    return {
        
        'page':        page,

        'limit':       limit,

        'total':       len(products),

        'total_pages': -(-len(products) // limit),   # ceiling division

        'products':    paged,

    }
class OrderRequest(BaseModel):

    customer_name:    str = Field(..., min_length=2, max_length=100)

    product_id:       int = Field(..., gt=0)

    quantity:         int = Field(..., gt=0, le=100)

    delivery_address: str = Field(..., min_length=10)


orders=[]

def calculate_total(product: dict, quantity: int) -> int:

    return product['price'] * quantity


def find_product(product_id: int):

    for p in products:

        if p['id'] == product_id:

            return p

    return None
order_counter = 1   # ✅ add this globally

@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter

    product = find_product(order_data.product_id)

    if not product:
        return {'error': 'Product not found'}

    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}

    total = calculate_total(product, order_data.quantity)

    order = {
        'order_id': order_counter,
        'customer_name': order_data.customer_name,
        'product': product['name'],
        'quantity': order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price': total,
        'status': 'confirmed',
    }

    orders.append(order)

    order_counter += 1

    return {'message': 'Order placed successfully', 'order': order}

@app.get('/orders/search')
def search_orders(
    keyword: str = Query (..., description = "ENNTER WORD TO SEARCH")
):
    results =[
        p for p in orders
        if keyword.lower() in p['customer_name'].lower()
    ]

    if not results :
        return {'message ': f'no products found for :{keyword}', 'results': []}
    
    return {
        'keyword' : keyword,
        'total_found' : len(results),
        'orders':results,
    }