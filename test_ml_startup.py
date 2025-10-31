#!/usr/bin/env python3
"""
Test ML service startup
"""

print("🔍 Testing ML service startup...")

try:
    print("1. Testing FastAPI import...")
    from fastapi import FastAPI, HTTPException
    print("✅ FastAPI imported successfully")
    
    print("2. Testing Pydantic import...")
    from pydantic import BaseModel
    print("✅ Pydantic imported successfully")
    
    print("3. Testing Uvicorn import...")
    import uvicorn
    print("✅ Uvicorn imported successfully")
    
    print("4. Creating FastAPI app...")
    app = FastAPI()
    print("✅ FastAPI app created successfully")
    
    print("5. Testing simple endpoint...")
    @app.get("/")
    async def root():
        return {"message": "Test API"}
    
    print("✅ Endpoint created successfully")
    
    print("6. Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
