# A/B Testing : Free Trial Screener

## Experiment Overview

In the experiment, Udacity tested a change where if the student clicked "start free trial", they were asked how much time they had available to devote to the course. If the student indicated 5 or more hours per week, they would be taken through the checkout process as usual. If they indicated fewer than 5 hours per week, a message would appear indicating that Udacity courses usually require a greater time commitment for successful completion, and suggesting that the student might like to access the course materials for free. At this point, the student would have the option to continue enrolling in the free trial, or access the course materials for free instead.

The hypothesis was that this might set clearer expectations for students upfront, thus reducing the number of frustrated students who left the free trial because they didn't have enough time—without significantly reducing the number of students to continue past the free trial and eventually complete the course. If this hypothesis held true, Udacity could improve the overall student experience and improve coaches' capacity to support students who are likely to complete the course.

## Experiment Design

The unit of diversion is a cookie, although if the student enrolls in the free trial, they are tracked by user-id from that point forward. The same user-id cannot enroll in the free trial twice. For users that do not enroll, their user-id is not tracked in the experiment, even if they were signed in when they visited the course overview page.

### Metric Choice

**Invariant Metrics:** number of cookies, number of clicks, click through probability

**Evaluation Metrics:** gross conversion, retention, net conversion

**Invariant Metrics**

Invariant metrics are the metrics that would be same in both control and experiment groups. Our invariant metrics follow from dividing our population on our units of diversion. After we divide subjects into experimental and control groups, we want to verify that the division has been performed correctly before assessing the potential effects of our experimental manipulations. Invariant metrics are those metrics that we record to check equivalences between groups, and which will not have direct implications on the efficacy of the experiment. Typically, this will come from checking that counts or rates are equivalent between groups.

**Number of Cookies:** The number of unique cookies to view the course overview page. It is a good invariant metric because unit of diversion should be same in both control and experiment groups.

**Number of Clicks:** Number of cookies to click the "start free trail" button (which happens before the free trail screener is trigger). Because free trail screener shows up after clicking the start free trail button, we can expect that number of clicks would be same in both control and experiment groups.

**Click-through-probability:** Number of unique cookies to click the "Start free trail" button divided by number of unique cookies to view the course overview page.

**Evaluation Metrics:**

Evaluation metrics are the metrics that would vary between control and experiment groups. By comparing differences between the control and experiment groups, we can measure the effectiveness of the free trail screener.

The main goal here is minimizing the student frustration and utilizing coaching resources effectively. Cancelling early may be one good indicator of low satisfaction. If more people, who couldn't spend enough time daily on courses, enrolled in courses, then the coaching resources would be utilized inefficiently. So to consider a launch, the following must be observed.

- Retention (students who stay after free trial should not be decreased)

- Gross Conversion and Net Conversion (less students enrolling in the free trial but students who stay after free trial should not be decreased)

**Gross Conversion:** Number of user-ids to complete checkout and enroll in the free trail divided by number of unique cookies to click the "Start free trail" button. The practical minimum difference is 0.01.

**Retention:** Number of user-ids to remain enrolled past the 14-day boundary(and thus make at least one payment) divided by number of user-ids to complete checkout. The practical minimum difference is 0.01.

**Net Conversion:** Number of user-ids to remain enrolled past the 14-day boundary(and thus make at least one payment) divided by the number of unique cookies to click the "Start free trail" button. The practical minimum difference is 0.0075.

Number of user-ids could be used as Evaluation metric. But it is not the best metric to choose as it is not normalized. It is better to use gross conversion, which will give more information than number of user-ids.

### Calculating Standard Deviation

**Analytical Estimate of Standard Deviation**

Evaluation Metric | Standard Deviation
:---------------: | :----------------:
Gross Conversion  |     0.0202
Retention         |     0.0549
Net Conversion    |     0.0156

For Gross Conversion and Net Conversion, the unit of diversion is equal to unit of analysis. So the analytical estimate of standard deviation tends to be empirical estimate of standard deviation. After calculating pageviews, duration and exposure, if we decide to keep retention, we have to calculate empirical variability of retention.

### Sizing

**Number of Samples vs. Power**

I am not using Bonferroni correction. Bonferroni correction is too conservative for these metrics. I want all my metrics to be significant. The pageviews were calculated using an alpha value of 0.05 and beta value of 0.2

**Gross Conversion**

- Baseline Conversion : 20.625%
- Minimum Detectable Effect : 1%
- alpha : 5%
- 1 - beta : 80%
- sample size : 25,835 enrollments/group
- total sample size : 25835 * 2 = 51,670 enrollments
- total pageviews : 645,857

**Retention**

- Baseline Conversion : 53%
- Minimum Detectable Effect : 1%
- alpha : 5%
- 1 - beta : 80%
- sample size : 39,155
- total sample size : 78,230 enrollments
- total pageviews : 4,741,212

**Net Conversion**

- Baseline Conversion : 10.9313%
- Minimum Detectable Effect : 0.75%
- alpha : 5%
- 1-beta : 80%
- sample size : 27,413
- total sample size : 54,826
- total pageviews : 685,325

Total PageViews required : 4,741,212

### Duration vs. Exposure

In all of these three evaluation metrics retention has most number of pageviews. If we divert our 100% traffic and 400,000 pageviews per day, then it will take approx. 119 days. Thats appro. 4 months. This is not feasible. After removing the retention, the required pageviews will be 685,325. If we divert 100% traffic, it will take approx. 18 days.

Since we are not dealing with any sensitive data and have no potential risks, we could divert 100% traffic to the experiment. But I would not advice diverting all traffic. Because there is always a chance that data collected over a short period of time is influenced by specific events. This is why collecting data over a longer period of time helps get a sense of the differences between week days/weekends, different weeks, or even months. We also should keep in mind how many other experiments are running, to decide the fraction of traffic. If we divert 50% traffic, it would take approx. 35 days. The only potential problem that we would have is drop in enrollments. Since we are not expecting a big drop in enrollments, because of our new feature and the duration is 35 days, we can take this risk. So considering all above points, I would choose to divert 50% traffic, which will take 35 days to complete the experiment.

## Experiment analysis

### Sanity Checks

Metric                    |Expected Value|Observed Value|CI Lower Bound|CI Upper Bound|Result
:------------------------:|:------------:|:------------:|:------------:|:------------:|:-----
 Number of Cookies        | 0.5000       | 0.5006       | 0.4988       | 0.5012       | Pass
 Number of Clicks         | 0.5000       | 0.5005       | 0.4959       | 0.5042       | Pass
 Click-through-probability| 0.0821       | 0.0822       | 0.0812       | 0.0830       | Pass

### Result Analysis

95% Confidence interval for the difference between the experiment and control group for evaluation metrics.

Metric                    |    dmin |Observed Difference|CI Lower Bound|CI Upper Bound|Result
:------------------------:|:-------:|:------------:|:------------:|:------------:|:-----
Gross Conversion          | 0.01    | -0.0205      | -0.0291      | -0.0120|Statistically and Practically Significant
Net Conversion            | 0.0075  | -0.0048      | -0.0116      | 0.0019 | Neither Statistically nor Practically Significant

### Sign Tests

Metrc      | p-value  | Statistically Significant (alpha = 0.05)
:---------:|:--------:|:---------------------------------------:
Gross Conversion|0.0026|Yes
Net Conversion|0.6776|No

### Summary

The experiment was conducted to see whether asking how many hours users could spend and thereby suggesting them to enroll, will increase student experience and coaches' capacity to support students who are likely to complete the course, without significantly reducing the number of students who continue past the free trail. The invariant metrics are Number of cookies, Number of clicks and Click-through-probability. Gross Conversion and Net Conversion are evaluation metrics. The null hypothesis is that there is no difference between control and experiment group. The practical significance was set for each metric. To launch the experiment, all evaluation metrics should be both practically and statistically significant. I did not use Bonferroni Correction because we want all our metrics to be statistically significant. Normally we use Bonferroni Correction to control false positives when using multiple metrics in which any of the metrics matches hypothesis. Sanity Checks revealed equal distribution of cookies into the control and experimental groups at 95% Confidence Interval. Gross Conversion was both statistically and practically significant, while Net Conversion was neither statistically nor practically significant.

### Recommendation

To make a recommendation whether to launch or not, first we need to check our evaluation metrics. The results of these two metrics will give us the clue. If both these metrics resulted as we expected, then we could launch otherwise we should discuss other alternatives. Let's check each metric individually.

Gross Conversion is the ratio of number of users enrolling the free trial and the number of users clicking the start free trail button. We are expecting fewer number of people enrolling in the course as a result of the free trail screener. Gross conversion is both statistically and practically significant, that means we are successful in decreasing the number of people who enroll for free trial.

Net Conversion is the ratio of the number of users who remain enrolled past the 14 day trail period and the number of users who click the start free trial button. So we are expecting the number of people who stayed after 14 day period not to decrease. Net conversion is neither statistically nor practically significant. The confidence interval of Net conversion includes the negative of practical significance boundary. So the number of people who stay after trial period, could possibly go down by an amount that matters to business. With 95% confidence, the net conversion can be as low as -0.0116 and as high as 0.0019. We cannot say for certain whether it will decrease or increase. It is not worth taking this risk.

So considering above points, I would recommend not to launch the experiment, rather it would be better to pursue other experiments.

### Follow-Up Experiment

After clicking the start free trial button, in addition to asking number of hours they could spend per week, it is also better to list prerequisite courses. If they are not comfortable with prerequisites, we advice them to take prerequisite courses and refresh the necessary knowledge. I also think that 14 day trail period is too short to adopt. It would take some time to adopt to new learning routine and changing old routines. I advice increasing 14 day trail period to 30 days. Now students would have enough time to adopt to the new learning routine. Usually beginners find it tough to start, once they are comfortable with the process, it is more likely that they will stay longer. This 30 day trail period is very crucial. It we have a beginner friendly project, that students could complete with in 30 days, they would feel accomplished and this will increase students paying for the course.

**Setup:** After clicking the "Start free trail" button, the free trail screener shows up. In that screener, in addition to time, we will also list the prerequisite courses. Free trail duration changed to 30 days. We have a beginner friendly project as a starting one.

**Null Hypothesis:** There is no significant difference in all metrics between control and experiment groups.

**Unit of Diversion:** Cookie

**Invariant Metrics:** Number of cookies, Click-through-probability

**Evaluation Metrics:** Gross Conversion, Retention, Net Conversion

If statistically and practically positive change in Retention and Net Conversion and negative change in Gross Conversion, then we can launch the experiment.
