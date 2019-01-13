from sklearn.neural_network import MLPClassifier

def neural_network(train_data, train_targets, test_data, hidden_layer_sizes=(100,), alpha=0.0001, learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, tol=0.0001, momentum=0.9, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10):
	mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, alpha=alpha, learning_rate_init=learning_rate_init, power_t=power_t, max_iter=max_iter, shuffle=shuffle, tol=tol, momentum=0.9, validation_fraction=validation_fraction, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, n_iter_no_change=n_iter_no_change)
	mlp.fit(train_data, train_targets)

	return mlp.predict(test_data)