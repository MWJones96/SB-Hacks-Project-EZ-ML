from sklearn.ensemble import RandomForestClassifier

def random_forest(train_data, train_targets, test_data, min_samples_split, min_samples_leaf, min_weight_fraction_leaf, min_impurity_decrease):
	rf = RandomForestClassifier(min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, min_impurity_decrease=min_impurity_decrease)
	rf.fit(train_data, train_targets)

	return rf.predict(test_data)