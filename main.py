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

    errors = []

    if request.height <= 0 or request.width <= 0:
        errors.append("Height and width must be positive numbers")

    if request.material not in ["stainless_steel", "carbon_steel"]:
        errors.append(f"unknown material type: {request.material}. Try stainless_steel or carbon_steel")

    if len(errors) > 0:
        return {
            "success": False,
            "errors": errors
        }

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, material, height, width, cost
            FROM projects
            WHERE material = ?
            AND height BETWEEN ? AND ?
            """,
            (request.material, request.height - 3, request.height + 3)
        )
        similar = cursor.fetchall()
        conn.close()

    except Exception as e:
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }

    if len(similar) == 0:
        return {
            "success": False,
            "error": "No similar projects found",
            "suggestion": "Try adjusting height or material"
        }

    costs = [row["cost"] for row in similar]
    avg_cost = sum(costs) / len(costs)

    return {
        "success": True,
        "estimated_cost": round(avg_cost, 2),
        "based_on": len(similar),
        "matched projects": [p["id"] for p in similar],
        "confidence": "high" if len(similar) >= 3 else "medium" if len(similar) >= 1 else "low"
    }