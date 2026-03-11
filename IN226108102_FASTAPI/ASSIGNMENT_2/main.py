# USE OF POST METHOD
# USE OF PYDANTIC METHOD(validation of data) 
# USE OF HELPER FUNCTION IN EXISTING PREV CODE    

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List
 
app = FastAPI()
 
# ══ PYDANTIC MODEL ════════════════════════════════════════════════
class OrderRequest(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    quantity:         int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)
    contact_number:   int= Field(...,max_length =10,min_length=10)

class CustomerFeedback(BaseModel):
    customer_name:  str = Field(...,min_length=2 , max_length=100)
    product_id: int= Field(..., gt=0)
    rating : int= Field(..., gt=0,lt=6)
    comment: str = Field(None,max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

class OrderRequest(BaseModel):
    product_id: int
    quantity: int

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

def get_feedback(cust_feedback:CustomerFeedback):
    cust_feedback: CustomerFeedback
    product= find_product(cust_feedback.product_id)
    if not product:
        return "PRODUCT NOT FOUND"
    feedback = {
            'customer_name': cust_feedback.customer_name ,
            'product_id': cust_feedback.product_id,
            'rating':cust_feedback.rating,
            'comment': cust_feedback.comment
    }
    feedbacks.append(feedback)
    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback,
        "total_feedback": len(feedbacks)}


def products_summary():
    total_products = len(products)

    in_stock_count = len([p for p in products if p['in_stock'] == True])
    out_of_stock_count = len([p for p in products if p['in_stock'] == False])

    most_expensive = max(products, key=lambda x: x['price'])
    cheapest = min(products, key=lambda x: x['price'])

    categories = list(set([p['category'] for p in products]))
    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

def find_product_price(product_id: int ):
    """Search products list by ID. Returns product dict or None."""
    for p in products:
        if p['id'] == product_id:
            return {"Product name ": p['name'] , "product price": p['price']}
    return "PRODUCT NOT FOUND"
 
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

# Task 3  Q4-----------------
@app.get('/products/summary')
def product_summary():
    return products_summary()
   


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


# task 3: Q2-------------------------------------
@app.get('/products/{product_id}/price')
def get_product_price(product_id: int):
    
    detail = find_product_price(product_id)

    return detail

#task : 3 Q3------------------------------------
feedbacks=[]

@app.post('/feedback')
def take_feedback(cust_feedback: CustomerFeedback):
   return get_feedback(cust_feedback)

#task:3 Q3--------------------------------------
@app.get('/product/feedback')
def get_product_feedback():
    return {'FEEDBACKS':feedbacks, 'Total feedbacks':len(feedbacks)}


# Q5 -------- Bulk Order Endpoint --------

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        # product not found
        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })

        # product out of stock
        elif not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })

        # valid order
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }


@app.post("/orderssss")
def place_order(data: OrderRequest):

    order = {
        "order_id": len(orders) + 1,
        "product_id": data.product_id,
        "quantity": data.quantity,
        "status": "pending"
    }

    orders.append(order)

    return {
        "message": "Order placed",
        "order": order
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"

            return {
                "message": "Order confirmed",
                "order": order
            }

    return {"error": "Order not found"}
