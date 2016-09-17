# Make Effective Data Visualization

## Summary

This data visualization shows the percentage of survived and perished passengers of the titanic disaster. My main interest in this visualization is to show how `gender` and `class` influenced survival chances. This visualization explores the differences in classes within gender and also explores the differences in Gender within class too. In the same bar, one can observe percentages of survived and perished passengers.

In the chart, you can observe the following things.
- 1st class has more survived passengers than other two classes.
- In 1st Class and 2nd Class more than 90% female survived, while 50% female survived in 3rd Class (click female button)
- There are more survived female passengers than male passengers.
- In 1st Class more than 90% female passengers survived whereas less than 40% male passengers survived. (click class 1 button)

## Design

My objective is to show how many survived and how many perished in the same visual. Both Pclass and Sex are categorical variables. So stacked bar chart is the correct choice for me. To summarize, using stacked bar chart we could show categories of data and in each bar we could show the difference between surviving and perished passengers at the same time.

I used D3.js to create two button groups. One button group is for visualizing within gender. Other button group is for visualizing within class. In this way, we can clearly see the difference both in gender and class. For example, when you click `male` button, you can see the probability of survival chances of male in each class.

I used dimple.js to create charts because it not only easy but also has greater flexibility to add new functionalities without digging deep into library. On hovering over the bar, you can see a tooltip that shows survived/perished, belongs to which class/gender and the percentage of people survived/perished.

I used bootstrap classes for buttons and button groups.

### Changes from feedback:
 - I changed y axis from raw counts to proportions.
 - Added a new button group that shows how male and female rates compare within classes.
 - Added more text to summarize the findings.
 - Changed button group position from pixels to percentages.
 - In tooltip, showing rates in percentages instead of showing raw counts.
 - Increased the font sizes and changed the axis titles.

## Feedback

### Feedback #1:

This visualization is off to a great start! I like how the subject of explanation (influence of gender and class on survival) is stated up front. This is very helpful for the audience. The interactive buttons are also a very effective feature. It does seem like there is a relationship between class and survival. To augment the explanatory nature of this visualization, please consider the following:

It looks like the y axis is raw counts. This is somewhat difficult to interpret without knowing the underlying distribution of the class or gender populations. Use of proportions would be more straight forward.
The visualization covers the effect of class and the effect of gender within class. It would also be useful to see how male and female survival rates compare to each other in the absence of a class split. That is, male vs. female survival rates. Consider also showing how male and female survival rates compare within classes.

I hope this is useful!

### Feedback #2:

Hi Brahma,

Your visualization is very well done!

It clearly shows the disparity between the survival rates for different classes. The most remarkable feature is the proportion of females who survived and difference between classes.

Even though this is a visualization project, adding some text to summarize your findings (so that the viewer can see if their interpretation corresponds to yours) is important.

One minor technical issue: You have specified most of your visualization's element's positions in percentages (or vh/vw), yet the button is specified in pixels (which means that it will be in a different position, relative to the other elements, depending on screen size). You could also set that in percentages:

            div.btn-group-vertical {
                position: absolute;
                top: 30%;
                left: 70%;
            }
Nice work!

### Feedback #3:

Hi Brahma,

Your visualization looks Top notch. Its interactive and very well explains the no. of people survived according to class | sex. The moment I hover on any bin of histogram it shows a line for the values, it really looks awesome.

But I feel two minor issues are there, so I would like to suggest those:
1. On hovering over a bin, if it will give count & survival rate(probability) then we will be able to get details about survival rate too.
2. The x-label & y-label font size looks little bit small to me & change x-label to "Passenger Class"

Amazing work @bradd123

## Resources

- https://discussions.udacity.com/t/need-feedback-for-project-6-titanic-data/187861
- http://dimplejs.org/
- https://github.com/PMSI-AlignAlytics/dimple/wiki
- https://discussions.udacity.com/t/updating-data-in-chart-with-dimple/162873
- https://discussions.udacity.com/t/p6-final-project-final-bits/178085
