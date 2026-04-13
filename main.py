from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#histoical data

history = [
    {"id": "PV-2024", "material": "stainless_steel", "height": 10, "width": 4, "cost": 185000},
    {"id": "PV-3011", "material": "stainless_steel", "height": 11, "width": 4, "cost": 198000},
    {"id": "PV-4455", "material": "stainless_steel", "height": 9, "width": 5, "cost": 242000},
    {"id": "RV-108", "material": "carbon_steel", "height": 14, "width": 6, "cost": 245000},
    {"id": "RV-512", "material": "carbon_steel", "height": 15, "width": 7, "cost": 380000},
    {"id": "RV-610", "material": "carbon_steel", "height": 13, "width": 5, "cost": 210000},
    {"id": "TK-441", "material": "stainless_steel", "height": 8, "width": 3, "cost": 92000},
    {"id": "HX-220", "material": "stainless_steel", "height": 12, "width": 5, "cost": 310000},
]

# this defines what the request body looks like 

class EstimateRequest(BaseModel):
    material: str
    height: int
    width: int
    weld_type : str = "standard"

#home endpoint

@app.get("/")
def home() : 
    return {"message": "Enerfab Estimation API is running!"}

#estimation endpoint
@app.post ("/api/estimate")
def get_estimate(request: EstimateRequest):
    #Step 1 : find similar projects
    similar = []
    for project in history:
        same_material = project["material"] == request.material
        close_height = abs(project["height"] - request.height) <= 3
        if same_material and close_height:
            similar.append(project)

    #step 2 : if no matches, return
    if len(similar) == 0:
        return {
            "success" : False,
            "error" : "No similar objects found",
            "suggestions" : "try stainless_steel or carbon_steel"
        }

    #step 3 calculate estimate
    total_cost = sum([p["cost"] for p in similar])
    average_cost = total_cost / len(similar)

    #step 4 return structured response 
    return {
        "success" : True,
        "estimated_cost" : round(average_cost, 2), 
        "based_on" : len(similar),
        "matched projects": [p["id"] for p in similar],
        "confidence" : "high" if len(similar) >= 3 else "medium" if len(similar) >= 1 else "low"
    }
