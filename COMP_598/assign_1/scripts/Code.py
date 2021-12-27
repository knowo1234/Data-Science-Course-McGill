import pandas as pd

#save filename to a variable called filename
filename=r'C:/Users/xsnow/Desktop/School/Semester 7/Comp 598/comp598-2021/hw1/submission_template/data/IRAhandle_tweets_1.csv'

tweets = pd.read_csv(filename) #read the file into the code
tweets = tweets.head(10000) #look at the first 10000 tweets
tweets = tweets[~tweets.content.str.contains("\?")] #get all the tweets containing ? out
tweets = tweets[tweets.language == 'English'] #keep all the tweets with englihs as their Language
tweets.to_csv(r'C:/Users/xsnow/Desktop/School/Semester 7/Comp 598/comp598-2021/hw1/submission_template/dataset.tsv') #export cleaned tweets to new csv
