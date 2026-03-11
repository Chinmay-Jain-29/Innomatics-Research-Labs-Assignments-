# USE OF POST METHOD
# USE OF PYDANTIC METHOD(validation of data) 
# USE OF HELPER FUNCTION IN EXISTING PREV CODE    

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
 
app = FastAPI()
 
# ══ PYDANTIC MODEL ════════════════════════════════════════════════
class OrderRequest(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    quantity:         int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)
    contact_number:   int= Field(...,max_length =10)
 
# ══ DATA ══════════════════════════════════════════════════════════
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook',       'price':  99, 'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True},
]
 
orders= []
order_counter = 1
 
# ══ HELPER FUNCTIONS ══════════════════════════════════════════════
 
def find_product(product_id: int):
    """Search products list by ID. Returns product dict or None."""
    for p in products:
        if p['id'] == product_id:
            return p
    return None
 
def calculate_total(product: dict, quantity: int) -> int:
    """Multiply price by quantity and return total."""
    return product['price'] * quantity
 
def filter_products_logic(category=None, min_price=None,
                          max_price=None, in_stock=None):
    """Apply filters and return matching products."""
    result = products
    if category  is not None:
        result = [p for p in result if p['category'] == category]
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock  is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return result
 
# ══ ENDPOINTS ═════════════════════════════════════════════════════
# ROUTE ORDER RULE:
#   Fixed routes  (/filter, /compare)  must come BEFORE
#   Variable route (/products/{product_id})
# ═════════════════════════════════════════════════════════════════
 
# ── Day 1 ─────────────────────────────────────────────────────────
 
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}
 
# ── Day 2: Query Parameters ────────────────────────────────────────
 
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    min_price: int  = Query(None, description='Minimum price'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only'),
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}
 
# ── Day 3: Compare (fixed route — must stay BEFORE /{product_id}) ─
 
@app.get('/products/compare')
def compare_products(
    product_1: int = Query(..., description='First product ID'),
    product_2: int = Query(..., description='Second product ID'),
):
    p1 = find_product(product_1)
    p2 = find_product(product_2)
    if not p1:
        return {'error': f'Product {product_1} not found'}
    if not p2:
        return {'error': f'Product {product_2} not found'}
    cheaper = p1 if p1['price'] < p2['price'] else p2
    return {
        'product_1':    p1,
        'product_2':    p2,
        'better_value': cheaper['name'],
        'price_diff':   abs(p1['price'] - p2['price']),
    }
 
# ── Day 1: Path Parameter (variable — always AFTER all fixed routes)
 
@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}
    return {'product': product}
 
# ── Day 2: POST + Pydantic ─────────────────────────────────────────
 
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
        'order_id':         order_counter,
        'customer_name':    order_data.customer_name,
        'product':          product['name'],
        'quantity':         order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price':      total,
        'status':           'confirmed',
    }
    orders.append(order)
    order_counter = order_counter + 1
    return {'message': 'Order placed successfully', 'order': order}
 
@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}
 
    return {'message':'Order placed successfully','order':order}
 
