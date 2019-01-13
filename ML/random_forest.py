from sklearn.ensemble import RandomForestClassifier

def random_forest(train_data, train_targets, test_data, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, min_impurity_decrease=0.0):
	rf = RandomForestClassifier(min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, min_impurity_decrease=min_impurity_decrease)
	rf.fit(train_data, train_targets)

	return rf.predict(test_data)