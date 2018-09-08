import pickle
import os


path = os.path.realpath(os.path.dirname(__file__))
model = pickle.load(open(os.path.join(path, "objects", "scorer.pkl"), "rb"))


def scorer(data):
    try:
        # ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        sepal_length, sepal_width = float(data['sepal_length']), float(data['sepal_width'])
        petal_length, petal_width = float(data['petal_length']), float(data['petal_width'])
        data_p = [[sepal_length, sepal_width, petal_length, petal_width]]
        pred = model.predict(data_p)[0]
        ppred = round(max(model.predict_proba(data_p)[0]), 4)
        return {'probability': ppred, 'class': pred, 'message': 'success'}
    except:
        return {'probability': None, 'class': None, 'message': 'there was an error'}


