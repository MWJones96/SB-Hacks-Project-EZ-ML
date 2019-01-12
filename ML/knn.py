from sklearn.neighbors import KNeighborsClassifier

def knn(train_data, train_targets, test_data, n_neighbors, leaf_size, p):
	knn = KNeighborsClassifier(n_neighbors=n_neighbors, leaf_size=leaf_size, p=p)
	knn.fit(train_data, train_targets)

	return knn.predict(test_data)