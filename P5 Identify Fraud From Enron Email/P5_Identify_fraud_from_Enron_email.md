## Enron Submission Free-Response Questions and Answers

### 1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?

The goal of this project is to build a person of interest identifier based on the features of financial and email data of Enron dataset. Enron was one of the largest companies in 2000. It had collapsed into bankruptcy due to widespread corporate fraud. The persons of interest are the people, who were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity. This is considered as supervised classification problem in which we use features to train a model and use this model to predict outcome label. In this case, it is whether someone is person of interest or not.

The dataset consists of financial and email data of about 150 Enron employees. The dataset consists of 146 records with 14 financial features, 6 email features and 1 labeled target feature (POI). In these 146 records, 18 records are persons of interest. With the financial information like salary, bonuses and stock values and email information like from/to messages, from_poi_to_this_person and from_this_person_to_poi we can build a model to predict whether someone is poi or not. The dataset is very small, so we need to be conservative about removing values. After inspecting the pdf file, I found two invalid values in the records. I removed `TOTAL` and `THE TRAVEL AGENCY IN THE PARK` from the dataset. I also removed `LOCKHART EUGENE E` as it does not contain any information.

In the dataset, some records have many missing values. But we need to be conservative about those because our dataset is pretty small, if we remove those records we can't build good predictive model. Our dataset is not only small but also imbalance. There are only 18 POI records. So If we predict every record as nonPOI, we will have 87% accuracy. So accuracy is not a good metric. Here precision and recall are good metrics. In this cases, we should use StratifiedShuffleShift as validation method because it  makes sure the ratio of POI and nonPOI is the same during training and testing.

### 2. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.

I have used `SelectKBest` to select the best features. I did not use any scaling because After using scaling I got low precision and recall. So I build the model without using any scaling. After reading the whole discussion about features, I got to know that having total values of all financial features is useful. I am right in this case, It is one of the most important feature for the model. So I created a new feature called `total_value` that contains sum of all financial values. In email data, from_this_person_to_poi and from_poi_to_this_person are useful features. In it's absolute form these are not that good, but ratios of these values will be good features. So I created two new features called `from_poi_rate` and `to_poi_rate`. In these to_poi_rate is one of the most important features. Following are the ten most important features.

(feature, score, p-value)
- ('bonus', '30.729', '0.000')
- ('salary', '15.859', '0.000')
- ('to_poi_rate', '15.838', '0.000')
- ('total_value', '10.803', '0.001')
- ('shared_receipt_with_poi', '10.723', '0.001')
- ('total_stock_value', '10.634', '0.002')
- ('exercised_stock_options', '9.680', '0.002')
- ('total_payments', '8.959', '0.003')
- ('deferred_income', '8.792', '0.004')
- ('restricted_stock', '8.058', '0.006')

p-value indicates how probable a given outcome or a more extreme outcome is under the null hypothesis. In general high scores and low p-values are better.

### 3. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?
I ended up using Decision Tree Classifier. DTC gave me good results in combination with SelectKBest and GridSearchCV. I have tried other algorithms also like SVC, kNN and NaiveBayes etc. But those are not giving good performance. precision and recall of SVC, kNN are around 0.27 and 0. 29 even after turing the parameters. So I tried Decision Tree Classifier which gave good performance compared to others. The F1 score of Decision Tree Classifier is 0.416.

### 4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).

Most of the classifiers has some parameters. Parameter tuning is selecting the parameters that leads to optimal model. This model will give us optimal score. If we are not tuning the parameters, then the model uses default values and this will result in poor model then poor results.  So it is always better to tune the parameters. I used GridSearchCV to find the best parameters. First I stored the range of parameters in a dictionary and then used this in GridSearchCV function with pipeline.

### 5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?

validation is testing the performance of the model so that we can ensure it will generalize well for unknown data. The classic mistake that we might make is overfitting. Overfitting occurs when we have too many parameters but very few observations. A model that has been overfit has poor predictive performance, as it overreacts to minor fluctuations in the training data. Overfitting model will try to memorize training data than learning to generalize to new data. In order to estimate how well model our has been trained on, we store some part of training data that we can use for validation.

So we should always be careful while doing validation. We have a pretty small data and that too we have very small number of POIs that makes it worse for validation. That's why I have used `StratifiedShuffleShift` . It will create indices for the test and train subsets of data. It performs random splits and training and testing splits each have class distribution that reflect overall data.

### 6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human understandable about your algorithm’s performance.

The two most important metrics that I have chosen are `precision` and `recall`. Since the data is small and imbalance, `accuracy` is not a good metric.

Note: Here positive prediction means recognizing that the employee is POI.

**precision**: It refers to the ratio of correct positive predictions made out of all positive predictions that our model made. The precision score is 0.41379.

**recall**: It refers to the correct positive predictions made out of the total that were indeed positive. To explain clearly, we are looking at actual POIs and calculating what proportion of them were recognized correctly. The recall score is 0.42000.

## References
- http://stackoverflow.com/questions/33091376/python-what-is-exactly-sklearn-pipeline-pipeline
- http://abshinn.github.io/python/sklearn/2014/06/08/grid-searching-in-all-the-right-places/
- http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html
- http://scikit-learn.org/stable/modules/tree.html
- Udacity Discussions
