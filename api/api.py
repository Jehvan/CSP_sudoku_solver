# API to fetch sudoku grids to be solved
import requests

def get_classic_sudoku():
    url = "https://sudoku-api.vercel.app/api/dosuku"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    grid = data["newboard"]["grids"][0]["value"]
    return grid
