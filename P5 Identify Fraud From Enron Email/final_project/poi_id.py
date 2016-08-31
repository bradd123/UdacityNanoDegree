#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from tester import test_classifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import cross_validation
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.neighbors import KNeighborsClassifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                      'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                      'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                      'restricted_stock', 'director_fees']

email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages',
                  'from_this_person_to_poi', 'shared_receipt_with_poi']


features_list = ['poi'] + financial_features + email_features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)



### Task 3: Create new feature(s)

for k,v in data_dict.items():
	if v["from_poi_to_this_person"] != "NaN" and v["from_this_person_to_poi"] != "NaN":
		v["from_poi_rate"] = v["from_poi_to_this_person"]/float(v["to_messages"])
		v["to_poi_rate"] = v["from_this_person_to_poi"]/float(v["from_messages"])
	else:
		v["from_poi_rate"] = 0
		v["to_poi_rate"] = 0
	if all([v[f] == "NaN" for f in financial_features]):
		v["total_value"] = "NaN"
	else:
		v["total_value"] = sum([v[f] for f in financial_features if (v[f] != "NaN")])

features_list.append("from_poi_rate")
features_list.append("to_poi_rate")
features_list.append("total_value")


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

tree = DecisionTreeClassifier()

parameters = {'tree__criterion' : ['gini', 'entropy'],
			  'tree__splitter' : ['best', 'random'],
			  'tree__random_state' : [42],
			  'tree__max_depth':range(8,12)}

min_max_scaler = MinMaxScaler()

skb = SelectKBest(score_func = f_classif)

pca_dt = PCA()

pipeline = Pipeline(steps = [('select', skb), ('tree', tree)])

cv = StratifiedShuffleSplit(labels, 100, random_state = 42)

gs = GridSearchCV(pipeline, parameters, n_jobs= -1, cv=cv, scoring='f1')
gs.fit(features, labels)
clf = gs.best_estimator_

test_classifier(clf, data_dict, features_list, 100)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)