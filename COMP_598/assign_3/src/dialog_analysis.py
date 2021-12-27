import json
import sys
import csv
import argparse
#argparse
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output_file')
parser.add_argument('data_file',type=str)
args = parser.parse_args()


#setting variables
data_file=args.data_file
output_file=args.output_file
total_pony_speach = 0
with open (data_file, "r") as f:
    reader = csv.reader(f)
    count = {'twilight sparkle':0,'applejack':0,'rarity':0,'pinkie pie':0,'rainbow dash':0,'fluttershy':0}
    for row in reader:
        total_pony_speach += 1
        for key in count:
            if key.lower()==row[2].lower():
                count[key] +=1


#for key in count:
#    total_pony_speach += count[key]


verbosity = {'twilight sparkle':0,'applejack':0,'rarity':0,'pinkie pie':0,'rainbow dash':0,'fluttershy':0}
for key in verbosity:
    verbosity[key]=round((count[key]/total_pony_speach),2)


output_json = {'count':count,'verbosity':verbosity}
with open ("../"+output_file,"w") as f:
    json.dump(output_json, f,indent=4)
