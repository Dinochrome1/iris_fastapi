from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils import load_model, predict_flower, QueryOut, QueryIn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("hello")
    load_model()
    yield
    print('bye')


app = FastAPI(lifespan=lifespan,
              title='iris_fastapi_demo v.2305041317')


@app.get('/')
async def root():
    return {"message": "iris_fastapi_demo"}


@app.post("/predict_flower", response_model=QueryOut, status_code=200)
def predict_flower_(query_data: QueryIn):
    output = {'flower_class': predict_flower(query_data)}
    return output
