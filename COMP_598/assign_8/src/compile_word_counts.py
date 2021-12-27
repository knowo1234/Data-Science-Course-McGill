import pandas as pd
import argparse
import json
from collections import Counter
import regex as re

#-o 
#-d 
parser = argparse.ArgumentParser()
parser.add_argument('-o','--word_counts_json',help='word_counts_json')
parser.add_argument('-d','--clean_dialog', nargs='?', help='clean_dialog.csv')
args = parser.parse_args()

#dictionary containing all the ponies and their respective dictioanries whihc will conatin the work count
ponies = {
    "Twilight Sparkle": {    },
    "Applejack": {    },
    "Rarity": {    },
    "Pinkie Pie": {    },
    "Rainbow Dash": {    },
    "Fluttershy": {    },
}
pony_arr = []
for keys in ponies.keys():
    pony_arr.append(keys)

#dictionary containing all the ponies and their respective dictioanries whihc will conatin the work count

with open('../data/stopwords.txt','r') as f:
        stopwords = f.read().splitlines()

output_file = args.word_counts_json
input_file = args.clean_dialog

def main():
    #load in csv and trim it to contain only the data we need
    d = load_clean(input_file)
    
    ponies = count_them(d)
    with open(output_file, 'w') as f:
        json.dump(ponies, f,indent=4)
    


def count_them(d):
    for pony in ponies:
        clean_words_per_pony = []
        all_dialog = list(d[d['pony']==pony]['dialog'].values)
        ponies[pony] = ' '.join(all_dialog)
        act = ponies[pony].split()
        punct_rem = []
        for word in act:
            punct_rem.append(lower_nostop(word))
        
        clean_act = [lower_nostop(word) for word in punct_rem if (word.isalpha()) and (not word in stopwords)]
        
        for word in clean_act:
            clean_words_per_pony.append(lower_nostop(word))
        counter = Counter(clean_words_per_pony)
        
        filtered_word_counts = {x: count for x, count in dict(counter).items() if count >= 5}
        ponies[pony]=filtered_word_counts  
    return ponies

def lower_nostop(word):
    # lowercase word
    word = word.lower()
    # remove punctuation
    word = re.sub(r"[()\[\],-.?!:;#&]+", " ", word)
    return word

def tokenize(speech_act):
    return [lower_nostop(word) for word in speech_act.split(" ") if (not word in stopwords) and (word.isalpha())]

def load_clean(input_file):
    
    df = pd.read_csv(input_file)
    df = df[['pony','dialog']]
    df = df.loc[df['pony'].isin(pony_arr)]
    return df


if __name__ == '__main__':
    main()