#!/usr/bin/python

import sys
import pickle
import numpy as np
import pandas as pd
# sys.path.append("../tools/")
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit

# from feature_format import featureFormat, targetFeatureSplit
from poi_utils import params_logistic, pipeline_logistic
from poi_utils import params_nb, pipeline_nb
from poi_utils import params_svc, pipeline_svc
from poi_utils import params_kmeans, pipeline_kmeans
from tester import test_classifier, dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "rb") )

### Task 2: Remove outliers
outlier_keys = ['TOTAL', 'LOCKHART EUGENE E']
for key in outlier_keys:
    data_dict.pop(key)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
df = pd.DataFrame(data_dict).transpose()
df = df.replace('NaN', np.nan)

# remove feature loan_advance and email_address
# loan_advance: less then 5% has data on this feature; besides, some POI has
#               this value and others do not. So there is no good reason why
#               this feature has so little data.
# email_address: will not help improve model quality
df = df.drop(['loan_advances', 'email_address'], axis=1)

# fill missing values with median of the corresponding column
df_median_filled = df.fillna(df.median())

# director_fees and restricted_stock_deferred_cat has many missing values.
# but all the POIs, this value is not available. Maybe these features for POIs
# are 0. So two features are added into the dataset with 0 means data not 
# available and 1 means data exists in the dataset
df_median_filled['director_fees_cat'] =\
        [0 if np.isnan(i) else 1 for i in df['director_fees']]

df_median_filled['restricted_stock_deferred_cat'] =\
        [0 if np.isnan(i) else 1 for i in df['restricted_stock_deferred']]

### Extract features and labels from dataset for local testing
#data = featureFormat(my_dataset, features_list, sort_keys = True)
#labels, features = targetFeatureSplit(data)
labels = df_median_filled['poi'].as_matrix()
features = df_median_filled.drop('poi', axis=1)
features_list = ['poi'] + list(features.columns.values)
features = features.as_matrix()

# transform back to dictionary type for tester use
my_dataset = dict(df_median_filled.transpose())
my_dataset = {k: dict(v) for k, v in my_dataset.items()}

print(my_dataset)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

sss = StratifiedShuffleSplit(labels, n_iter=100, test_size=0.1)

scoring = 'f1'
gs = GridSearchCV(pipeline_logistic, param_grid=params_logistic,
        scoring=scoring, cv=sss, verbose=0, n_jobs=-1)
gs.fit(features, labels)

n_pca_components = gs.best_estimator_.named_steps['pca'].n_components_
explained_variance_ratio =\
        gs.best_estimator_.named_steps['pca'].explained_variance_ratio_

print("Cross-validated {0} score: {1}".format(scoring, gs.best_score_))
print("Reduced to {0} PCA components".format(n_pca_components))
print("Explained variance ratio: {0}".format(str(explained_variance_ratio)))
print("Params: ", gs.best_params_)

clf = gs.best_estimator_

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)
