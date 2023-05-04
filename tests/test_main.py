from fastapi.testclient import TestClient
from main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "iris_fastapi_demo"}


def test_pred_virginica():
    payload = {
        "sepal_length": 3,
        "sepal_width": 5,
        "petal_length": 3.2,
        "petal_width": 4.4
    }
    with TestClient(app) as client:
        response = client.post('/predict_flower', json=payload)
        assert response.status_code == 200
        assert response.json() == {'flower_class': "Iris Virginica"}


def test_name_must_be_greater_than_zero():
    payload = {
        "sepal_length": 1,
        "sepal_width": 0,
        "petal_length": 3.2,
        "petal_width": 4.4
    }
    with TestClient(app) as client:
        response = client.post('/predict_flower', json=payload)
        assert response.status_code == 422
        assert response.json() == {'detail': [{'loc': ['body',
                                                       'sepal_width'],
                                               'msg': 'must be greater than zero',
                                               'type': 'value_error'}]}


def test_name_must_be_greater_than_zero_2():
    payload = {
        "sepal_length": 1,
        "sepal_width": -2,
        "petal_length": -3.2,
        "petal_width": 4.4
    }
    with TestClient(app) as client:
        response = client.post('/predict_flower', json=payload)
        assert response.status_code == 422
        assert response.json() == {'detail': [{'loc': ['body',
                                                       'sepal_width'],
                                               'msg': 'must be greater than zero',
                                               'type': 'value_error'},
                                              {'loc': ['body',
                                                       'petal_length'],
                                               'msg': 'must be greater than zero',
                                               'type': 'value_error'}]}
