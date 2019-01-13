from sklearn.svm import SVC

def svm(train_data, train_targets, test_data, C=1.0, kernel='rbf', degree=3, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, max_iter=-1):
	svm = SVC(C=C, kernel=kernel, degree=degree, coef0=coef0, shrinking=shrinking, probability=probability, tol=tol, cache_size=cache_size, max_iter=max_iter)
	svm.fit(train_data, train_targets)

	return svm.predict(test_data)