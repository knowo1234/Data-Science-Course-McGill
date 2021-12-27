import pandas as pd
import requests, json
#import BeautifulSoup
import sys

#capture the input file
input_file = sys.argv[1]

def main():
    
    subs_dict = subreddit_dictionary(input_file)
    open_and_compute(sys.argv[1],subs_dict)

def open_and_compute(input_file,subreddit_dict):
    #create a dictionary that will hold the avg length of titles per subreddit
    avg_title_len = {}
    for subreddits in subreddit_dict:
        avg_title_len.update({'{}'.format(subreddits):0})
    f = open(input_file,'r+')
    denominator = 0
    for line in f:
        denominator = denominator +1
        file = json.loads(line)
        avg_title_len[file['data']['subreddit']] = len(file['data']['title']) + avg_title_len[file['data']['subreddit']]
    f.close()
    denominator = denominator/len(avg_title_len.keys())
    for subreddit in avg_title_len.keys():
        avg_title_len[subreddit] = round(avg_title_len[subreddit]/denominator,2)
    print(avg_title_len)

def subreddit_dictionary(input_file):
    avg_title_len = {}
    f = open(input_file,'r+')
    for line in f:
        file = json.loads(line)
        avg_title_len.update({file['data']['subreddit']:0})
    return avg_title_len
if __name__ == '__main__':
    main()