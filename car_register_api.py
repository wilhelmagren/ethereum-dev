"""
Super simple webpage for listing all cars that exist in a local db.

File created: 2025-01-30
Last updated: 2025-02-12
"""

import sqlite3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return "Welcome to the car register webpage, such a nice design, right?..." 


@app.get("/cars", response_class=HTMLResponse)
async def read_cars():

    sql = sqlite3.connect("cars.db")
    cursor = sql.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()

    html_content = """
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
    <h1>Car register</h1><ul>
    """

    for car in cars:
        html_content += f"""
        <li>
            <span><strong>Id:</strong> {car[0]}</span>
            <span>Owner:   {car[1]}</span>
            <span>Previous owner:  {car[2]}</span>
            <span>Price:   {car[3]} SEK</span>
        </li>
        """
    html_content += "</ul></body></html>"

    return html_content

