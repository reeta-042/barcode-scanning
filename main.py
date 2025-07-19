import os
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Barcode Lookup API",
    description="An intelligent product verification system that checks barcodes against a MongoDB database and flags potentially fake items.",
    version="1.0.0"
)
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],            
)

# MongoDB connection
uri = os.environ.get("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["barcodeDB"]
collection = db["barcodes"]

@app.get("/")
def read_root():
    return {"message": "Barcode lookup API is running 🔍"}

@app.get("/product/{barcode}")
def get_product(barcode: str):
    result = collection.find_one({"barcode": barcode})
    if result:
        return {
            "barcode": result["barcode"],
            "productName": result["productName"],
            "status": result["status"],
            "reason": result["reason"]
        }
    else:
        return {
            "message": "Product might be fake",
            "reason": "product not available on the system"
        }
