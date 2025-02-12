"""
Super simple webpage for listing all cars that exist in a local db.

File created: 2025-01-30
Last updated: 2025-02-12
"""

import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

CARS_DB = "./cars_db.json"


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return "Welcome to the car register webpage, such a nice design, right?..." 


@app.get("/cars", response_class=HTMLResponse)
async def read_cars():
    with open(CARS_DB, "rb") as f:
        cars = json.loads(f.read())

    html_content = """
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
    <h1>Car register</h1><ul>
    """

    for car_id, car in cars.items():
        html_content += f"""
        <li>
            <span><strong>Id:</strong> {car_id}</span>
            <span>Owner:   {car['owner']}</span>
            <span>Price:   {car['price']} SEK</span>
            <span>Previous owner:  {car['previous_owner']}</span>
        </li>
        """
    html_content += "</ul></body></html>"

    return html_content

