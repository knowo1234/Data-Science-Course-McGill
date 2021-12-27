import pandas as pd
import json
import requests
import argparse
import sys
import csv
import random
#-o is the output file
#-s is the  subreddit



if sys.argv[1] == '-o':
    try:
        output_file = sys.argv[2]
        json_file = sys.argv[3]
        num_posts_to_output = sys.argv[4]
    except:
        sys.stderr.write('ERROR -- you forgot some arguments: json_input num_posts_to_output')

def main():
    file = openfile(json_file) #open the file -- return: file pointer
    check = compare_posts_file(num_posts_to_output,file) #check if the file has lte, gt lines than the posts wanted -- return:boolean
    write_annotated_file(file,output_file,check,num_posts_to_output)
    
def write_annotated_file(file,out,check,num): #jsonfile, outputfile
    if check:
        with open('../'+out,'w+') as f:
            tsv_writer = csv.writer(f,delimiter='\t')
            tsv_writer.writerow(['Name','title','coding'])
            for i in range(0,int(num)):
                try:
                    tsv_writer.writerow([file[0]['data']['children'][i]['data']['author_fullname'],file[0]['data']['children'][i]['data']['title'],None])
                except:
                    continue
    if not check:
        with open('../'+out,'w+') as f:
            tsv_writer = csv.writer(f,delimiter='\t')
            tsv_writer.writerow(['Name','title','coding'])
            for i in range(0,len(file[0]['data']['children'])):
                r = random.randint(0,int(num))
                try:
                    tsv_writer.writerow([file[0]['data']['children'][r]['data']['author_fullname'],file[0]['data']['children'][r]['data']['title'],None])
                except:
                    continue
    return out

def openfile(json_file):
    data = []
    with open(json_file,'r+') as f:
        for line in f:
            jsonstr = json.loads(line)
            data.append(jsonstr)
    return data

def compare_posts_file(num,file):
    if len(file[0]['data']['children']) <= int(num):
        return False
    return True

if __name__ == '__main__':
    main()

