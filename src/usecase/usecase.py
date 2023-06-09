import pandas as pd
import json
from src.solver.solve_problem import solve_problem
import numpy as np

def usecase():
  
  df = pd.read_csv('data/target.csv')
  days = 7
  daily_budget = 500*3
  nutrients = {
    'protein': 40*3, 
    'carb': 100*3,
    'fat': 40*3,
  }
  
  
  solution = solve_problem(df, days, daily_budget, nutrients,)

  # Return the solution in JSON format
  return json.dumps(solution, cls=MyEncoder, indent=2, ensure_ascii=False)

# カスタムエンコーダー
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return super(MyEncoder, self).default(obj)