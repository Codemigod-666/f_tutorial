from math import e
from fastapi import FastAPI, Query, responses
from typing import Annotated
from db.database import get_supabase_client
from models import Product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = get_supabase_client()
if client is not None:
    print("Supabase database connection successful")
else:
    print("Supabase database connection FAILED")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return "Hello World!!"


# products = [
#     Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
#     Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
#     Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
#     Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
# ]

# to get all products
@app.get("/products/")
def get_all_products():
    response = client.table("Products").select("*").execute()
    return response.data


# GET - particular product 
# @app.get("/products/{product_id}")
# def get_product_by_id(product_id: int):
#     for product in products:
#         if product.id == product_id:
#             return product
#     return {"error": "Product not found"}


# # POST - CREATE PRODUCT: 
@app.post("/products/")
def create_product(product: Product):
    client = get_supabase_client()

    try:
        response = client.table("Products").insert(product.dict()).execute()
        return {
            "message": "Product created successfully",
            "product": response.data
        }
    except Exception as e:
        return {"error": str(e)}


# # PUT - update prodcuts 
@app.put("/products/{product_id}")
def update_products(product_id: int, product: Product):
    client = get_supabase_client()

    try: 
        response = {
            client.table("Products")
            .update(product.dict())
            .eq("id", product_id)
            .execute()
        }

        return {
            "message": "Peoduct updated successfully",
            "product": response.data
        }
    except Exception as e: 
        return {"error": str(e)}


# # DELETE - delete product 
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    client = get_supabase_client()

    try:
        response = (
            client.table("Products")
            .delete()
            .eq("id", product_id)
            .execute()
        )
        return {
            "message": "Product deleted successfully",
            "product": response.data
        }
    except Exception as e:
        return {"error": str(e)}


