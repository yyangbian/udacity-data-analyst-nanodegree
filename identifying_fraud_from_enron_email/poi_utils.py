"""
File: poi_utils.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description: provide multiple helper functions for this course project
"""
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans

pipeline_logistic = Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                                    ('pca', PCA()),
                                    ('clf', LogisticRegression(max_iter=400,
                                        random_state=42))])

params_logistic = {'pca__n_components' : [0.3, 0.5, 0.8, 1, 2, 3, 4, 6],
                   'pca__whiten'       : [True, False],
                   'clf__C'            : np.logspace(-6, 6, 2),
                   'clf__tol'          : [1e-4, 1e-20],
                   'clf__class_weight' : [{True : 14, False : 1},
                                          {True : 10, False : 1},
                                          {True : 6,  False : 1},
                                          {True : 1,  False : 1},
                                          {True : 1,  False : 2},
                                          'auto',],}

pipeline_nb = Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                              ('pca', PCA()),
                              ('clf', GaussianNB())])

params_nb = {'pca__n_components' : [1, 2, 3, 4, 6],
             'pca__whiten'       : [True, False],
            }

pipeline_svc = Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                               ('pca', PCA()),
                               ('clf', SVC())])

params_svc = {'clf__kernel': ['linear', 'rbf'],
              'clf__C': [1e-16, 1e-6, 1e-2, 1e-1, 1, 10, 100],
              'clf__class_weight': [{True: 14, False: 1},
                                    {True: 10, False: 1},
                                    {True: 6,  False: 1},
                                    'auto',],
              'pca__n_components': [0.3, 0.5, 0.8, 1, 2, 3, 4, 6],
              'pca__whiten': [True, False]}


pipeline_kmeans = Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                                  ('pca', PCA()),
                                  ('clf', KMeans(n_clusters=2,
                                                 n_init = 50,
                                                 random_state=42))])

params_kmeans = {'pca__n_components': [1, 2, 3, 4, 6],
                 'pca__whiten': [True, False],}

