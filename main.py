import os
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_utility import call_llm_model  # 🔗 Import LLM logic from separate module

app = FastAPI(
    title="Barcode Lookup API",
    description="An intelligent product verification system that checks barcodes against a MongoDB database and flags potentially fake items.",
    version="1.0.0"
)

# 🔐 CORS setup
origins = [
    "http://localhost:3000",
    "https://veritrue.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 MongoDB connection
uri = os.environ.get("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["barcodeDB"]
collection = db["barcodes"]

# 🏠 Root route
@app.get("/")
def read_root():
    return {"message": "Barcode lookup API is running 🔍"}

# 🔍 Barcode product lookup with LLM enrichment
class ProductRequest(BaseModel):
‎    barcode: str
‎    language: str
‎@app.post("/product/")
‎def get_product(data: ProductRequest):
‎    barcode = data.barcode
‎    language = data.language
    result = collection.find_one({"barcode": barcode})
‎    if result:
‎        metadata = {
‎            "product_name": result.get("productName", ""),
‎            "brand": result.get("brand", ""),
‎            "category": result.get("category", ""),
‎            "use": result.get("use", ""),
‎            "pack_size": result.get("packSize", ""),
‎            "features": result.get("features", ""),
‎            "language": language 
‎        }
‎
‎        explanation = call_llm_model(metadata)
‎
‎        return {
‎            "barcode": result["barcode"],
‎            "productName": result["productName"],
‎            "status": result["status"],
‎            "reason": result["reason"],
‎            "What_Vero_has_to_say": explanation if explanation else "Vero has no comment"
‎        }
‎    else:
‎        return {
‎            "message": "Product might be fake",
‎            "reason": "Product not available on the system"
‎        }
