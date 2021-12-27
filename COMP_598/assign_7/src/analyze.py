import pandas   as pd
import requests
import argparse
import json
import sys

#-i is the coded_file
#-s is the  subreddit
parser = argparse.ArgumentParser()
parser.add_argument('-i','--coded_file',help='coded file')
parser.add_argument('-o','--output_file', nargs='?', help='output file')
args = parser.parse_args()

def main():
    coded_file = args.coded_file
    try:
        output_file = args.output_file
    except:
        pass
    
    count_flags(coded_file)

    count_json = count_flags(coded_file)
    if output_file is not None:
        write_to_file(output_file,count_json)
    else:
        output_to_stdout(count_json)

def count_flags(coded_file):
    total_counts = {}
    total_counts.update({"course-related":0,"food-related":0,"residence-related":0,"other":0})
    d = {'c':0,'f':0,'o':0,'r':0}
    ser = pd.Series(d)
    with open(coded_file,'r+') as f:
        df = pd.read_csv(f,sep='\t')
        df = df.dropna()
        codes = df['coding'].value_counts().sort_index()
        
        total = pd.concat([ser,codes],axis=1).drop(columns=0,axis=1).fillna(0)
        total_counts['course-related'] = int(total.values[0][0])
        total_counts['food-related'] = int(total.values[1][0])
        total_counts['residence-related'] = int(total.values[2][0])
        total_counts['other'] = int(total.values[3][0])
    return total_counts

def write_to_file(output_file,count_json):
    with open('../'+output_file,'w') as f:
        json.dump(count_json, f,indent=4)

def output_to_stdout(count_json):
    sys.stdout.write(json.dumps(count_json,indent=4))


if __name__ == '__main__':
    main()