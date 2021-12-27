import datetime
import json
import argparse
import pandas as pd
import re
import dateutil
from dateutil.parser import isoparse
from dateutil.tz import UTC


#-i is the input file
#-o is the output file
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input_file',help='Input file')
parser.add_argument('-o','--output_file',help='Output file')
args = parser.parse_args()

def main():
    file = open_and_load(args.input_file)
    file2 = title_check(file)
    file = change_title(file2)
    file2 = check_author(file)
    file = check_count_convert(file2)
    file2 = ISO_check_UTC_convert(file)
    file = check_tags(file2)
    write_to_file(file)


#open and load the File into a pyton array
#this also removes invalid JSON objects that are missing the last } 5
def open_and_load(input):
    raw_data = []
    f = open(input,'r+')
    for line in f:
        try:  
            json_line = json.loads(line)
            raw_data.append(json_line)

        except:
            continue
    f.close()
    return raw_data
#lets remove all lines that dont have a title or title_text 1
def title_check(raw_data):
    title_only = []
    for i in range(0,len(raw_data)):
        if ('title' in raw_data[i].keys() or 'title_text' in raw_data[i].keys()):
            title_only.append(raw_data[i])
    return title_only
#change all title_text to title 2
def change_title(title_only):
    for i in range(0,len(title_only)):
        
        if ('title_text' in title_only[i].keys()):
            print('')
            title_only[i]['title'] = title_only[i]['title_text']
            del title_only[i]['title_text']
    return title_only
#remove all objects where the author field is empty, null, or N/A 6
def check_author(title_only):
    data = []
    for i in range(0,len(title_only)):
        
        if (title_only[i]['author'] != 'N/A' and title_only[i]['author'] != None and title_only[i]['author'] != 'n/a'):
            data.append(title_only[i])
    return data
#check if str, int, float then convert to int 7, 8
def check_count_convert(data):
    swag = []
    for i in range(0,len(data)):
        if('total_count' not in data[i].keys()):
                swag.append(data[i])
                continue
        if(type(data[i]['total_count']) == int or type(data[i]['total_count']) == str or type(data[i]['total_count']) == float):
            
            try:
                data[i]['total_count'] = int(float(data[i]['total_count']))
                swag.append(data[i])
            except:
                continue
    return swag
#check if date is ISO standard 4
def ISO_check_UTC_convert(swag):
    data = []
    for i in range(0,len(swag)):
        try:
            dateutil.parser.isoparse(swag[i]['createdAt'])
            data.append(swag[i])
        except:
            continue
    #convert to UTC 3
    for i in range(0,len(data)):
        dt = isoparse(data[i]['createdAt'])
        data[i]['createdAt'] = str(dt.astimezone(UTC))
    return data
#9 tags
def check_tags(data):
    for i in range(0,len(data)):
        if('tags' not in data[i].keys()):
                continue

        all_tags = []
        for tag in data[i]['tags']:
            all_tags.extend((tag.split(' ')))
        data[i]['tags'] = all_tags
    return data
#write to output file 10
def write_to_file(data):
    with open(args.output_file,'w') as f:
        json.dump(data, f,indent=4)

if __name__ == '__main__':
    main()
