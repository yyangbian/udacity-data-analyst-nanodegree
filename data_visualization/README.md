# Titanic Passenger Data
#### Udacity Data Analyst Nanodegree Project 6 (Data Visualization and D3.js)
#### Yang Yang

## Summary

This data visualization shows the passenger information between those
passengers who survived and those who died in the Titanic tragedy.
Passengers are divided into groups based on gender, passenger class, age group,
number of siblings/spouses abroad, number of children/parents abroad
or port or embarkation. The data can be viewed either as absolute number or as
normalized percentages.

## Design

The goal is to find out what type of people has more chance to survive in this
tragical event. Since most of the variabls are categorical, or can be converted
to categorical variables, bar chart is selected as the tool to convey the
information to readers. There are quite a few variables that may have an impact
on whether the passenger can survive or not. In order to let readers explore
the effect of different variables, an interactive feature is added to the
graph: different data will be plotted based on the variable selected by the
reader. Since the number people are not equally distributed
across the different categories, a normalization feature is added so that
readers can easily see the percentages of survived passenges within each
category.

## Feedbacks

Below is the feedback I received. The initial version of the visualization can
be found in the directory *"initial_version"*.

### Feedback 1
>Instead of having drop down menus for the choices, could you use buttons or
rollovers (it's just easier to click than to use a menu, and it would be nice
to be able to see all of the options immediately instead of having to click a
menu to see them).

### Feedback 2
>The data also has a variable "Fare". Logically, you may think that the people
>who paid more for the ticket were richer, possibly in 1st or 2nd class and
>thus had more chance or survival. You may try to create bins for the ticket
fare and include it in the plot as well.

### Feedback 3
>Some things that confused me: for port of embarkation, I don't know where
the locations are (where is Q and S ?), could you use the names? For passenger
class, it is also better to use '1st class', '2nd class' and '3rd class' on the
axis label instead of only '1', '2', and '3'.

# Resources
* [Titanic Passenger Data](https://www.kaggle.com/c/titanic/data)
* [Data Visualization and D3.js (Udacity)](https://www.udacity.com/course/viewer#!/c-ud507-nd)
* [Dimple documentation](https://github.com/PMSI-AlignAlytics/dimple/wiki)
* [Dimple examples](http://dimplejs.org/examples_index.html)

# Files and Data
* index.html: html page contains the visualization
* js/main.js: javascript file that creates the visualization
* initial_version: directory that contains the html, javascript and data files
for the initial version of the visualization.
* data/titanic.csv: original downloaded dataset from
[here](https://www.kaggle.com/c/titanic/data)
* data/titanic_modified.csv: modified data set to create the visualization
* titanic_data_analysis.ipynb: ipython notebook that is used to create
data/titanic_modified.csv


