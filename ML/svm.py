from sklearn.svm import SVC

def svm(train_data, train_targets, test_data, C, kernel, degree, coef0, shrinking, probability, tol, cache_size, max_iter):
	svm = SVC(C=C, kernel=kernel, degree=degree, coef0=coef0, shrinking=shrinking, probability=probability, tol=tol, cache_size=cache_size, max_iter=max_iter)
	svm.fit(train_data, train_targets)

	return svm.predict(test_data)