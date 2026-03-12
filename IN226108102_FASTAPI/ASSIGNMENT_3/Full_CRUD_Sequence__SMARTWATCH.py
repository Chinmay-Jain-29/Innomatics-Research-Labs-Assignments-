from fastapi import FastAPI , Query ,Request ,Response ,status
from pydantic import BaseModel , Field

app = FastAPI()

Watch_data = [
    {"id": 1,"name": "Apple Watch Series 9",   "price": 41999,  "category": "Electronics", "in_stock": True},
    {"id": 2,"name": "Apple Watch Series 9",   "price": 41999,  "category": "Electronics", "in_stock": True},
    {"id": 3,"name": "Samsung Galaxy Watch 6", "price": 29999,  "category": "Electronics", "in_stock": False},
    {"id": 4,"name": "Noise ColorFit Pro 4",   "price": 3499,   "category": "Electronics", "in_stock": True}
]

class AddProducts(BaseModel):
    name : str = Field(...,min_length=2,max_length=100)
    price : int = Field(...,gt=500)
    category :str = Field(..., min_length=2)
    in_stock :bool = True


def check_duplicate_product(addproduct:AddProducts, response:Response):
    for p in Watch_data:
        if p['name'].lower() ==addproduct.name.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return{'Message':"Data is already exist in dataset"}
    new_id = max(p['id'] for p in Watch_data )+1
    new_data = {
        "id": new_id,
        "name": addproduct.name,
        "price": addproduct.price,
        "category": addproduct.category,
        "in_stock": addproduct.in_stock
    }
    
    Watch_data.append(new_data)
    return new_data


@app.get('/products/getallproducts')
def get_all_products():
    return Watch_data


@app.post('/products')
def add_products(addproduct:AddProducts, response:Response):
    return check_duplicate_product(addproduct, response)


@app.get('/products/{product_id}')
def get_product_by_id(product_id:int):
   return find_product(product_id)


def find_product(product_id):
    for p in Watch_data:
        if p['id'] == product_id:
            return p
    return None
        

def update_products(product_id:int,
                    response:Response,
                     price:int|None,
                     in_stock:bool|None ):
    
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': "Product not exist in database"}
    if price is not None :
        product['price']=price
    if in_stock is not None:
        product['in_stock']=in_stock

    return product

@app.put('/products/update/{product_id}')
def update_product( product_id: int,
                    response: Response,
                    price: int = Query(None),
                    in_stock: bool = Query(None)
                    ):
    
    return update_products(product_id, response, price, in_stock)
    
@app.delete('/products/delete/{product_id}')
def delete_product(product_id:int  ,response:Response):
    prod = find_product(product_id)
    if not prod:
        response.status_code = status.HTTP_404_NOT_FOUND
        return'Product not found'
    
    Watch_data.remove(prod)
    return {f"product deleted {prod}"}