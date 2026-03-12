from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
   {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook',       'price':  99, 'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False}
]



@app.put('/products/discount')
def apply_discount(
    category: str = Query(..., description="Product category"),
    discount_percent: int = Query(..., ge=1, le=99)
):

    updated_products = []

    for p in products:
        if p['category'].lower() == category.lower():

            new_price = int(p['price'] * (1 - discount_percent / 100))
            p['price'] = new_price

            updated_products.append({
                "name": p['name'],
                "new_price": new_price
            })

    if len(updated_products) == 0:
        return {"message": f"No products found in category '{category}'"}

    return {
        "updated_count": len(updated_products),
        "updated_products": updated_products
    }



@app.get('/products/audit')
def product_audit():
    total_products = len(products)
    in_stock_count =[]
    out_of_stock_names= []
    for p in products:
        if p['in_stock']==True:
            in_stock_count.append(p)
        else:
            out_of_stock_names.append(p['name'])
    total_stock_value = sum(p['price'] for p in in_stock_count)*10
    most_expensive = max(products , key = lambda x: x['price'])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_count),
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": most_expensive['name'],'price':most_expensive['price']
    }
    








class NewProducts(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price : int = Field(..., gt=0)
    category : str = Field(..., min_length=2)
    in_stock : bool = True

   

@app.post('/products')
def add_products(newproduct: NewProducts,response:Response):
    
   
    existing_name = [p['name'].lower() for p in products]
    if newproduct.name.lower() in existing_name:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Product already exists'}
    
    next_id = max(p['id'] for p in products)+1

    product ={
        'id': next_id,
        'name':newproduct.name,
        'price':newproduct.price,
        'category':newproduct.category,
        'in_stock': newproduct.in_stock,
    }
    products.append(product)
    response.status_code= status.HTTP_201_CREATED
    return{'message': 'product added', 'product': product}
    


def find_product(product_id):
    for p in products:
        if p['id']==product_id:
            return p
    return None


@app.put("/productsss/{product_id}/update")
def update_product(
    product_id:int,
    response: Response,
    in_stock:bool = Query(None, description='update stock status'),
    price:int= Query(None, description = 'Update price'),

):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error:',"PRODUCT NOT FOUND"}
    if in_stock is not None:
        product['in_stock']=in_stock

    if price is not None:
        product['price']=price

    #return {in_stock,price}
    return {"message": 'product Updated', 'product':product}

@app.delete("/products/{product_id}")
def delete_product(response:Response, product_id:int):
    product = find_product(product_id)
    if not product:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{'Error': 'Product not found'}
    products.remove(product)
    return{'Message': f"product '{product['name']}' deleted"}
        
