from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import solution.factory
from model.data_handler import DataHandler

app = FastAPI()

@app.get('/solutions/{name}')
def get_scenario(name: str, scenario: Optional[str]=None):
  sol = solution.factory.one_solution_scenarios(name)
  if sol:
    constructor = sol[0]
    obj = constructor(scenario=scenario)
    return {name: to_json(obj)}
  else:
    return {}

def to_json(scenario):
    json_data = dict()
    instance_vars = vars(scenario).keys()
    for iv in instance_vars:
        try:
            obj = getattr(scenario, iv)
            if issubclass(type(obj), DataHandler):
                json_data[iv] = obj.to_json()
        except BaseException as e:
            json_data[iv] = None
    return {scenario.scenario: json_data}
