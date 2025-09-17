from math import e
from fastapi import Depends, FastAPI, HTTPException, Query, responses
from sqlalchemy.orm import Session
# from typing import Annotated
from db.database import get_db, engine
# from db.database import get_supabase_client
from models import Product
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas

app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# if client is not None:
#     print("Supabase database connection successful")
# else:
#     print("Supabase database connection FAILED")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://f-tutorial.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return "Hello World!!"

# ✅ Get all products 
@app.get("/products/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# ✅ Create product
@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ✅ Get product by ID
@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



# ✅ Update product
@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


# ✅ Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}