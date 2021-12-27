import requests
import pandas as pd
import json
import argparse
import os
from bs4 import BeautifulSoup
import requests
import urllib


#-c is the config file
#-o is the output file
parser = argparse.ArgumentParser()
parser.add_argument('-c','--config_file',help='Contains single JSON dictionary')
parser.add_argument('-o','--output_file',help='Output file')
args = parser.parse_args()

raw_url = 'https://www.whosdatedwho.com/dating/'

def main():
    jsonstr = open_and_load(args.config_file)
    directory = jsonstr['cache_dir']
    output_dict = {}
    for people in jsonstr['target_people']:
        person_cache = check_cache(directory,people) #checks if the dir exists, if not makes one, then checks the dir if the names are chached there, if not scraeps
        if person_cache:
            download_webpage(directory,people)
            find_relationships(directory,people,output_dict)
        if not person_cache:
            find_relationships(directory,people,output_dict)
    with open(args.output_file,'w+') as o:
        json.dump(output_dict,o,indent=1)
              
def find_relationships(dir,person,relation_dict):
    relations = []
    with open('../'+dir+'/'+person,'r') as f:
        file = f.read()
        soup = BeautifulSoup(file,'html.parser')
        relation_dict.update({person:None})
        step1 = soup.find('div',id='ff-dating-history-list')
        try:
            for points in step1.find_all('h4','ff-title'):
                relations.append(points.string)
            relation_dict[person]=relations
        except:
            relation_dict[person]=relations
     
def open_and_load(input_file):
    with open(input_file,'r') as f:
        return json.load(f)

def check_cache(dir,person):
    if not os.path.isdir('../'+dir):
        os.mkdir('../'+dir)
    if not os.path.isfile('../'+dir+'/'+person):
        return True

def download_webpage(dir,person):
    full_url = raw_url+person
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content,'html.parser')
    open('../'+dir+'/'+person,'w').write(str(soup))

if __name__ == '__main__':
    main()
