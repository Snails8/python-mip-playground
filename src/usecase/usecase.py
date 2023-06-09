import pandas as pd
import json
from src.solver.solve_problem import solve_problem

def usecase():
  
  df = pd.read_csv('data/target.csv')
  days = 7
  daily_budget = 330*3
  nutrients = {
    'protein': 20*3, 
    'carb': 80*3,
    'fat': 20*3,
  }
  
  
  solution = solve_problem(df, days, daily_budget, nutrients,)

  # Return the solution in JSON format
  return json.dumps(solution)
