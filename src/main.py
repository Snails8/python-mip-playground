from typing import Dict
from fastapi import FastAPI, status
from src.usecase.usecase import usecase

app: FastAPI = FastAPI()

@app.post("/run", status_code=status.HTTP_200_OK)
async def main() -> Dict[str, str]:
  
  json = usecase()
  
  with open('src/solution.json', 'w') as f:
    f.write(json)
  return json