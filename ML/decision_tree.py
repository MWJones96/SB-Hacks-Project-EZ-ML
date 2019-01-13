from sklearn.tree import DecisionTreeClassifier

def neural_network(train_data, train_targets, test_data, min_samples_split, min_samples_leaf, min_weight_fraction_leaf, min_impurity_decrease):
	dt = DecisionTreeClassifier(min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, min_impurity_decrease=min_impurity_decrease)
	dt.fit(train_data, train_targets)

	return dt.predict(test_data)