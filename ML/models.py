import  decision_tree as dt
import knn as knn
import neural_net as nn
import random_forest as rf
import svm as svm

def run_model(model, **kwargs):
    if model == "dt":
        return dt.neural_network(**kwargs)
    elif model == "knn":
        return knn.knn(**kwargs)
    elif model == "nn":
        return nn.neural_network(**kwargs)
    elif model == "rf":
        return rf.random_forest(**kwargs)
    elif model == "svm":
        return svm.svm(**kwargs)
    else:
        return None