# Identifying Fraud at Enron Using Emails and Financial Data

#### Project 4 - Udacity Nanodegree
#### Yang Yang

## Project Overview
In 2000, Enron was one of the largest companies in the United States. By 2002,
it had collapsed into bankruptcy due to widespread corporate fraud. In the
resulting Federal investigation, a significant amount of typically confidential
information entered into the public record, including tens of thousands of
emails and detailed financial data for top executives. In this project, skills
gained from class "Machine Learning" is used to build a person of interest
identifier based on financial and email data made public as a result of the
Enron scandal.

## Question 1
>Summarize for us the goal of this project and how machine learning is useful
in trying to accomplish it. As part of your answer, give some background on
the dataset and how it can be used to answer the project question. Were there
any outliers in the data when you got it, and how did you handle those?

### Goal of the project
The goal of this project is to build a prediction model to identify person
-of-interest (POI) based on financial and email data made public as a result of the
Enron scandal. A person is considered as a POI if he or she was indicted,
reached a settlement or plea deal with the government, or testified in
exchange for prosecution immunity.

The dataset contains financial and email data of 146 persons, out of which 18
are real POIs. Each person's record includes 14 financial features and 6 email
features.

| Feature                     | Number of Data Available     |
| --------------------------: | :--------------------------: |
| bonus                       | 82                           |
| deferral\_payments          | 39                           |
| deferred\_income            | 49                           |
| director\_fees              | 17                           |
| exercised\_stock\_options   | 102                          |
| expenses                    | 95                           |
| loan\_advances              | 4                            |
| long\_term\_incentive       | 66                           |
| restricted\_stock           | 110                          |
| restricted\_stock\_deferred | 18                           |
| salary                      | 95                           |
| total\_payments             | 125                          |
| total\_stock\_value         | 126                          |
| other                       | 93                           |
| email\_address              | 111                          |
| from\_messages              | 86                           |
| from\_poi\_to\_this\_person | 86                           |
| from\_this\_person\_to\_poi | 86                           |
| shared\_receipt\_with\_poi  | 86                           |
| to\_messages                | 86                           |


### Outliers
After exploring the dataset using python, 2 candidates were identified as
outliers and removed from the data set in further analysis:

* TOTAL:  this is likely a spreadsheet artifact.
* LOCKHART EUGENE E: No feature of this person is available.

Based on the "domain knowledge", email\_address should not be helpful in the
analysis. It will be removed from the analysis as well, which left us 144 data
points with 19 features.


## Question 2
>What features did you end up using in your POI identifier, and what
selection process did you use to pick them? Did you have to do any scaling?
Why or why not? As part of the assignment, you should attempt to engineer
your own feature that does not come ready-made in the dataset -- explain what
feature you tried to make, and the rationale behind it. (You do not
necessarily have to use it in the final analysis, only engineer and test it.)
In your feature selection step, if you used an algorithm like a decision tree,
please also give the feature importances of the features that you use, and
if you used an automated feature selection function like SelectKBest, please
report the feature scores and reasons for your choice of parameter values.

There are a lot of missing values in the final dataset. For loan\_advances,
only 4 data points are available, which is less than 5% of the data. Besides,
some of the POIs have this feature, while the rest do not. So there is no
good reason why this feature has so little data So this feature is removed in
final analysis. email\_address is not used and also removed from the dataset.

Since the amount of data is small and there are a lot of features available,
principle component analysis (PCA) is used for dimensionality reduction. Some
of the features are highly correlated. For example, the correlation coefficient
between total\_stock\_value and exercised\_stock\_options is 0.96; between
total\_payments and other is 0.83. PCA should be helpful to remove this
collinearity between different features.

The original feature data are on vastly different scales and vary
significantly by several orders of magnitude. Because PCA, logistic
regression and support vector machines have better performance with features
on a similar scale, all features are scaled to values between 0 and 1 using
_MinMaxScaler_.

#### Feature Engineering

All missing values are replaced with the median of the corresponding feature.

director\_fees and restricted\_stock\_deferred also have many missing values.
But the values of these two features are missing for all POIs.
Maybe POIs tend not have values on these features. To account for this,
two features director\_fees\_cat and restricted\_stock\_deferred\_cat are
added into the dataset with 0 means data not available and 1 means data
exists in the dataset. These features were used in the final model; but they
only improve the model quality slightly.


## Question 3
>What algorithm did you end up using? What other one(s) did you try? How did
model performance differ between algorithms?

Logistic regression turns out to the method with best performance. Besides, I
have also tried several other methods: Gaussian Naive Bayes, Support Vector
Machine Classifier, and K-means clustering.

## Question 4
>What does it mean to tune the parameters of an algorithm, and what can
happen if you don’t do this well?  How did you tune the parameters of your
particular algorithm? (Some algorithms do not have parameters that you need
to tune -- if this is the case for the one you picked, identify and briefly
explain how you would have done it for the model that was not your final
choice or a different model that does utilize parameter tuning, e.g. a
decision tree classifier).  [relevant rubric item: “tune the algorithm”]

Parameters of an algorithm affects its performance. If these parameters are not
tuned properly, the default value will be used and the resulting model is
probably not an optimized one, which means its precision, recall or other
performance metrics will not be as good as it could be.

In this work, grid search was used to tune major parameters of the
corresponding algorithm. Grid search is done on 100 cross-validation splits.
The average score obtained for testing over the testing data in each split is
then calculated to get the model with the highest average score. Since the goal
is to achieve better than 0.3 precision and recall, "f1" was used as the
scoring function in the grid search.

## Question 5
>What is validation, and what’s a classic mistake you can make if you do it
wrong? How did you validate your analysis? 

Validation helps you understand the performance of the model outside the
specific dataset. Typically, the dataset is split into training and testing
dataset. The model is trained on the training data and then verified over the
testing dataset. A classic mistake is overfitting. The model is able to have
very accurate prediction within the training data; but its performance over the
testing data is very poor.

The dataset for this project is very small. Therefore no data is reversed only
for testing. Instead, stratified shuffle split is used to evaluate the model
performance. 1000 randomized train-test splits are created; precision, recall
and f1-score are the average values from these 1000 cases.

## Question 6
>Give at least 2 evaluation metrics and your average performance for each of
them.  Explain an interpretation of your metrics that says something human
understandable about your algorithm’s performance.

Accuracy is not a good choice of evaluation metrics for this project because
the number of two classes are not balanced. If the model predicts non-POIs for
all the cases, the accuracy is still as high as 0.875. Precision, recall and F1
score will be used for evaluation here.

* __Precision__: TruePositive / (TruePositive + FalsePositive). A high
  precision means whenever a POI gets flagged, we have a high confidence that
it is very likely to be a real POI and not a false alarm.
* __Recal__: TruePositive / (TruePositive + FalseNegative). A high recall means
  the model is very unlikely to miss a real POI.
* __F1 score__: TruePositive * 2 / (TruePositive * 2 + FalseNegative +
  FalsePositive). This is the best of both worlds. High f1 score means that
both false positive and false negative rates are low, which means that POIs can
be identified reliably and accurately. If the model finds a POI then the
person is almost certainly a POI; if the identifier does not flag someone,
then they are almost certainly not a POI.

| Algorithm                 | Precision   | Recall      | F1 Score    |
| ------------------------: | :---------: | :---------: | :---------: |
| Logistic Regression       | 0.365       | 0.775       | 0.496       |
| Gaussian Naive Bayes      | 0.36        | 0.344       | 0.352       |
| Support Vector Classifier | 0.353       | 0.689       | 0.467       |
| K-means Clustering        | 0.108       | 0.233       | 0.174       |


# Files
* poi\_id.py: POI identifier
* poi\_utils.py: pipelines and parameter grids used for grid search to find the
  optimal model parameters
* tester.py: Udacity-provided file; used for validation and output relevant
  model information for submission
* README.md: markdown file to generate this report
* index.html: report generated from the markdown file
