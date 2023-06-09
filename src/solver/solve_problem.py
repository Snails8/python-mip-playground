import pandas as pd
from mip import Model, xsum, BINARY, OptimizationStatus
from typing import Dict, List


def solve_problem(df: pd.DataFrame, days:int, daily_budget: float, nutrients: Dict[str, float]) -> str:
  m = Model()
  MEAL_PER_DAY = 3
  
  # 各食品が各日、各食事に対応するかどうかを示す二値変数を作成: x[d][meal][i] = 1 のとき、日dの食事mealに食品iが含まれる
  x = [] 
  for d in range(days):
    daily_menu = []
    for meal in range(MEAL_PER_DAY):
      meal_menu = []
      for i in df.index:
        decision_var = m.add_var(var_type=BINARY)
        meal_menu.append(decision_var)
      daily_menu.append(meal_menu)
    x.append(daily_menu)
  # x = [[[m.add_var(var_type=BINARY) for i in range(len(df))] for j in range(MEAL_PER_DAY)] for k in range(days)]

  # 各日、各食事の価格制約
  for d in range(days):
    m += xsum(df.iloc[j]['price_a'] * x[d][i][j] for i in range(3) for j in range(len(df))) <= daily_budget


  # 各日の栄養素制約
  for d in range(days):
    for i in range(3):
      for n in nutrients:
        m += xsum(df.iloc[j][n] * x[d][i][j] for j in range(len(df))) >= nutrients[n] * 0.9
        m += xsum(df.iloc[j][n] * x[d][i][j] for j in range(len(df))) <= nutrients[n] * 1.1

  # Set objective function
  m.objective = xsum(df.iloc[j]['price_a'] * x[d][i][j] for j in range(len(df)) for d in range(days) for i in range(3))

  # 最適化問題を解く
  m.optimize()

  if m.status == OptimizationStatus.OPTIMAL:
    
    # 解を取り出す
    solution = [[[df.iloc[j]['code'] if x[d][i][j].x >= 0.99 else '' for j in range(len(df))] for i in range(3)] for d in range(days)]
  else:
    print('The problem does not have an optimal solution.')
    solution = None
  
  return solution
