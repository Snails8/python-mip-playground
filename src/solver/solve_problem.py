import pandas as pd
from mip import Model, xsum, BINARY, OptimizationStatus
from typing import Dict, List


def solve_problem(df: pd.DataFrame, days:int, daily_budget: float, nutrients: Dict[str, float]) -> str:
  m = Model()
  MEAL_PER_DAY = 3
  MIN_MENU_PER_MEAL = 3

  
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

  # １日3食は用意する
  for d in range(days):
    for i in range(MIN_MENU_PER_MEAL):
      m += xsum(x[d][i][j] for j in range(len(df))) >= MIN_MENU_PER_MEAL
  
  # 制約：各日、各食事の価格が一日の予算以下であること
  for d in range(days):
    m += xsum(df.iloc[j]['price_a'] * x[d][i][j] for i in range(MEAL_PER_DAY) for j in range(len(df))) <= daily_budget
  
  # 各食において主菜は必ず一個以上
  for d in range(days):
    for i in range(MEAL_PER_DAY):
      m += xsum(x[d][i][j] for j in df[df['cat_M'] == "主菜"].index) == 1


  # 制約：各日、各食事の各栄養素が目標範囲（目標値の90%から110%）内に収まること
  # for d in range(days):
  #   for i in range(3):
  #     for n in nutrients:
  #       m += xsum(df.iloc[j][n] * x[d][i][j] for j in range(len(df))) >= nutrients[n] * 0.9
  #       m += xsum(df.iloc[j][n] * x[d][i][j] for j in range(len(df))) <= nutrients[n] * 1.1

  # 目的関数は全ての日、全ての食事の価格の合計を最小化すること
  m.objective = xsum(df.iloc[j]['price_a'] * x[d][i][j] for j in range(len(df)) for d in range(days) for i in range(3))

  # 最適化問題を解く
  m.optimize()

  meal_times = ["breakfast", "lunch", "dinner"]
  solution = []
  if m.status == OptimizationStatus.OPTIMAL:
    print('--------found solution!--------')
    # solution = [[[df.iloc[j]['code'] if x[d][i][j].x >= 0.99 else '' for j in range(len(df))] for i in range(3)] for d in range(days)]

    # 各日についてループ
    for d in range(days):
        daily_menu = {"day": d + 1, "meals": []}
        for i in range(3):
            meal_menu = {"time": meal_times[i], "items": []}
            for j in range(len(df)):
                if x[d][i][j].x >= 0.99: #変数が二値であることを期待するが、数値計算の誤差により、1の代わりに0.999999などの値を出すことがある
                    meal_menu["items"].append({
                        "code": df.iloc[j]['code'],
                        "name": df.iloc[j]['name'],
                        "cat_M": df.iloc[j]['cat_M'],
                        
                    })
            daily_menu["meals"].append(meal_menu)
        solution.append(daily_menu)
  
  else:
    print('-------- The problem does not have an optimal solution -------')
    solution = None
  
  return solution
