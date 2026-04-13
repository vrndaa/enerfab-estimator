from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class EstimateRequest(BaseModel):
    material: str
    height: int
    width: int
    weld_type : str = "standard"

def get_db():
    conn = sqlite3.connect("enerfab.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home() : 
    return {"message": "Enerfab Estimation API is running!"}

#estimation endpoint
@app.post ("/api/estimate")
def get_estimate(request: EstimateRequest):
    #Step 1 : find similar projects
    similar = []
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, material, height, width, cost
        FROM projects
        WHERE material  = ?
        AND height BETWEEN ? AND ?
        """,
        (request.material, request.height - 3, request.height +3)
    )

    similar = cursor.fetchall()
    conn.close()

    if len(similar) == 0:
        return {
            "success": False,
            "error": "No similar projects found",
            "suggestion": "Try stainless_steel or carbon_steel"
        }

    costs = [row["cost"] for row in similar]
    avg_cost = sum(costs) / len(costs)

    #step 4 return structured response 
    return {
        "success": True,
        "estimated_cost": round(avg_cost, 2), 
        "based_on": len(similar),
        "matched projects": [p["id"] for p in similar],
        "confidence": "high" if len(similar) >= 3 else "medium" if len(similar) >= 1 else "low"
    }
