# Estimation Tool

A REST API that estimates fabrication project costs based on historical data. Built as a project.

## What it does

When a project manager send vessel specification wrt material, dimensiosn, etc -- the API returns a cost estimate

## How it works 

- client sends a post request with vessel specs
- the API queries a SQLite database of historical products
- find projects with similar specifications
- it then calculates the average cost of those matches
- returns estimate w confidence level & matched project ID

## Stack
- Pyhton
- FastAPI
- SQLite (BigQuery in production)
- Git

## How to run
'''bash
python3 -m venv
pip install fastapi uvicorn
python setup_db.py
uvicorn main:app --reload

Then open http://localhost:8000/docs to test.

## What I would add in production

- Replace SQLite with BigQuery for large-scale data
- Add a Vertex AI model instead of simple averaging
- Add weld type and width to the matching criteria
- Deploy on Google Cloud Run
- Add authentication for API access
