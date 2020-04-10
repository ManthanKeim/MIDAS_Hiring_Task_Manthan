# Reddit Flair Predictor

[Project Hosted on : Heroku (CSS not enabled due to memory issue )](link)

[Machine Learning Model: Google Drive link can be downloaded and used ](link)


### Technologies Used:
* Frontend - HTML/CSS
* Backend - Flask
* Database - Direct CSV import from pandas library
* APIs - Reddit API, PRAW Model 

### Overall Approach towards the problem

1. Data Acquisition - I collected the data from the subreddit r/India, using the reddit API and praw model. I collected almost 200 post from each flair incline (AskIndia,Non-Political,[R]eddiquette, Scheduled, Photography, Science/Technology, Politics, Business/Finance, Policy/Economy, Sports, Food, AMA). I collected approximately 2200 subreddit posts collectively and represented them using graphs, wordcloud etc. ( attached below).

2. Flair Detection - Since I'm not so fluent in Machine Learning part, but I'm able to make the model using different algorithms including Naive Bayes, SVM, logistic regression, random forest, MLP classifier. I got the best accuracy from random forest and using this as the testing and training. Then I've split the data into 70% training and 30% testing and getting the Random forest accuracy 78% using the combination of URL, comments and title of the subreddit post. (refrences attached ) 

3. Web Application : Using Flask library as backend and HTML/CSS as frontend, all the screenshots are attached below. Unfortunately I am not able to push the CSS file to heroku library due to memory shortage ( working on this ) but the application working is totally fine.

4. Reported the result using graphs and visualizations.

### Libraries/Dependencies

* beautifulsoup
* Flask
* scikit
* sklearn
* nltk
* etc. ( listed in requirements.txt)

### Refrences

* https://praw.readthedocs.io/en/latest/
* https://www.reddit.com/dev/api/
* https://www.datacamp.com/community/tutorials/wordcloud-python
* https://seaborn.pydata.org
