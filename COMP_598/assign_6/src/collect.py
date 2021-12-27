import pandas as pd
import requests, json
#import BeautifulSoup

def main():
    #AUTHENTICATION
    headers = {}
    CLIENT_ID = 'Fm91DhLSEMsxGwMA2m4RIQ'
    SECRET_KEY = 'XwKUdo-LCl63yS0Pp1y9tW0svMfU4A'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)
    with open('../.env.example','r') as f:
        pw = f.read()
    data = {
        'grant_type': 'password',
        'username': 'Comp598_hw6',
        'password': pw
    }
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
    #AUTHENTICATION

    #define array of subreddits to scrape
    by_subsribers = ['funny','AskReddit','gaming','aww','pics','Music','science','worldnews','videos','todayilearned']
    by_posts = ['AskReddit','memes','politics','nfl','nba','wallstreetbets','teenagers','PublicFreakout','leagueoflegends','unpopularopinion']

    
    scrape_by_subreddit_into_file(by_subsribers,'sample1.json',headers)
    scrape_by_subreddit_into_file(by_posts,'sample2.json',headers)

    #first we will do by subscribers
    #titles_by_subs = scrape_by_subreddit(by_subsribers)
    #second: scrape subreddits by posts
    #titles_by_posts = scrape_by_subreddit(by_posts)


#compute average title length for each dictionary
#this method writes the children from the reddit scrape to a file output_file
def scrape_by_subreddit_into_file(subreddit_list,output_file,headers):
    #titles_for_each_subreddit = {}
    titles_array=[]
    for subreddits in subreddit_list:
        scrape_url = 'https://oauth.reddit.com/r/{}/new?limit=100'.format(subreddits)
        reddit_titles = requests.get(scrape_url, 
                                    headers=headers)
        for i in range(0,100):
            titles_array.append(reddit_titles.json()['data']['children'][i])#['data']['title'])
        #titles_for_each_subreddit.update({'{}'.format(subreddits):titles_array})
    
    f = open('../'+output_file,'w+')
    for i in range(0,len(titles_array)):
        jsonstr = json.dumps(titles_array[i])
        f.write(jsonstr)
        f.write('\n')
    f.close()

#data.children.data.title
#this method gives me a dictionary of 100 titles from each subreddit in the list passed
def scrape_by_subreddit(subreddit_list):
    titles_by = {}
    for subreddits in subreddit_list:
        titles_array = []
        scrape_url = 'https://oauth.reddit.com/r/{}/new?limit=100'.format(subreddits)
        reddit_titles = requests.get(scrape_url, 
                                    headers=headers)
        for i in range(0,100):
            titles_array.append(reddit_titles.json()['data']['children'][i]['data']['title'])
        titles_by.update({'{}'.format(subreddits):titles_array})
        
    return titles_by

if __name__ == '__main__':
    main()
