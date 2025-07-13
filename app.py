from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI(
    title="Barcode Lookup API",
    description="An intelligent product verification system that checks barcodes against a MongoDB database and flags potentially fake items.",
    version="1.0.0"
)

# MongoDB connection
uri = "mongodb+srv://francismbah008:<your_password>@enugu-hackathon.lkcsush.mongodb.net/?retryWrites=true&w=majority&appName=enugu-hackathon"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["barcodeDB"]
collection = db["barcodes"]

@app.get("/")
def read_root():
    return {"message": "Barcode lookup API is running 🔍"}

@app.get("/product/{barcode}")
def get_product(barcode: str):
    result = collection.find_one({"code": barcode})
    if result:
        return {
            "code": result["code"],
            "productName": result["productName"],
            "status": result["status"],
            "reason": result["reason"]
        }
    else:
        return {
            "message": "Product might be fake",
            "reason": "product not available on the system"
        }
