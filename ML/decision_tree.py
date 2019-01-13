from sklearn.tree import DecisionTreeClassifier

def decision_tree(train_data, train_targets, test_data, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, min_impurity_decrease=0.0):
	dt = DecisionTreeClassifier(min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, min_impurity_decrease=min_impurity_decrease)
	dt.fit(train_data, train_targets)

	return dt.predict(test_data)