from fastapi import FastAPI

app = FastAPI(title="Health Calculator API")

@app.get("/api/v1/bmi")
def calculate_bmi(weight_kg: float, height_m: float):
    if height_m <= 0:
        return {"error": "Chiều cao phải lớn hơn 0"}
    
    bmi = weight_kg / (height_m ** 2)
    category = ""
    if bmi < 18.5:
        category = "Gầy"
    elif bmi < 24.9:
        category = "Bình thường"
    else:
        category = "Thừa cân"
        
    return {
        "weight": weight_kg,
        "height": height_m,
        "bmi": round(bmi, 2),
        "category": category
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)