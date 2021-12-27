import pandas  
import requests
import argparse
import json

#-o is the output file
#-s is the  subreddit
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output_file',help='output file')
parser.add_argument('-s','--subreddit',help='enter a subreddit')
args = parser.parse_args()

def main():
    headers = reddit_auth()
    
    scrape_by_subreddit_into_file(args.subreddit,args.output_file,headers)

def reddit_auth():
    #AUTHENTICATION
    headers = {}
    CLIENT_ID = 'Fm91DhLSEMsxGwMA2m4RIQ'
    SECRET_KEY = 'XwKUdo-LCl63yS0Pp1y9tW0svMfU4A'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)
    with open('../auth/.env.example','r') as f:
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
    return headers

def scrape_by_subreddit_into_file(subreddit,output_file,headers):
    #titles_for_each_subreddit = {}
    titles_array=[]
    scrape_url = 'https://oauth.reddit.com/{}/new?limit=100'.format(subreddit)
    reddit_title = requests.get(scrape_url, 
                                headers=headers)
    
    titles_array.append(reddit_title.json())#['data']['children'][i])#['data']['title'])
    #titles_for_each_subreddit.update({'{}'.format(subreddits):titles_array})
    
    f = open('../'+output_file,'w+')
    for i in range(0,len(titles_array)):
        jsonstr = json.dumps(titles_array[i])
        f.write(jsonstr)
        f.write('\n')
    f.close()

if __name__ == '__main__':
    main()