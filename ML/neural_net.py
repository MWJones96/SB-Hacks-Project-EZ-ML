from sklearn.neural_network import MLPClassifier

def neural_network(train_data, train_targets, test_data, hidden_layer_sizes, alpha, learning_rate_init, power, max_iter, shuffle, tol, validation_fraction, beta_1, beta_2, epsilon, n_iter_no_change):
	mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, alpha=alpha, learning_rate_init=learning_rate_init, power=power, max_iter=max_iter, shuffle=shuffle, tol=tol, validation_fraction=validation_fraction, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, n_iter_no_change=n_iter_no_change)
	mlp.fit(train_data, train_targets)

	return mlp.predict(test_data)