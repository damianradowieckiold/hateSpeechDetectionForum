# Based on https://github.com/ybalcanci/Hate-Speech-Detector

from sklearn.externals import joblib

sgd = joblib.load(r"model\svm_model")

print(sgd.predict(["Hey"]))