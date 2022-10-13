from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal
import models

app = FastAPI()

class Product(BaseModel):
    id:int
    name:str
    category:str
    price:float


    class Config:
        orm_mode=True

db=SessionLocal()


@app.get('/products',response_model=List[Product],status_code=200)
def get_all_products():
    products=db.query(models.Product).all()

    return products

@app.get('/product/{product_id}',response_model=Product,status_code=status.HTTP_200_OK)
def get_a_product(product_id:int):
    product=db.query(models.Product).filter(models.Product.id==product_id).first()

    return product

@app.post('/products',response_model=Product,status_code=status.HTTP_201_CREATED)
def create_a_product(product:Product):
    db_product = db.query(models.Product).filter(models.Product.name == product.name).first()

    if db_product is not None:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product=models.Product(
        name=product.name,
        price=product.price,
        category=product.category
    )

    db.add(new_product)
    db.commit()

    return new_product

@app.put('/product/{product_id}', response_model=Product, status_code=status.HTTP_200_OK)
def update_a_product(product_id:int,product:Product):
    product_to_update=db.query(models.Product).filter(models.Product.id==product_id).first()
    product_to_update.name=product.name
    product_to_update.price=product.price
    product_to_update.category=product.category

    db.commit()

    return product_to_update

@app.delete('/product/{product_id}')
def delete_product(product_id:int):
    product_to_delete=db.query(models.Product).filter(models.Product.id==product_id).first()

    if product_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

    db.delete(product_to_delete)
    db.commit()

    return product_to_delete

