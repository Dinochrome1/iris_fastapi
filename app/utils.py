from pydantic import BaseModel, validator, root_validator
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

clf = GaussianNB()

classes = {
    0: "Iris Setosa",
    1: "Iris Versicolour",
    2: "Iris Virginica"
}


class QueryIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    def name_must_be_greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('must be greater than zero')
        return v


class QueryOut(BaseModel):
    flower_class: str


def load_model():
    X, y = datasets.load_iris(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Model trained with accuracy: {round(acc, 3)}")


def predict_flower(query_data):
    x = list(query_data.dict().values())
    prediction = clf.predict([x])[0]
    print(f"Model prediction: {classes[prediction]}")
    return classes[prediction]
