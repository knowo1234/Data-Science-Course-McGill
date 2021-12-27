import pandas as pd
import argparse 
import json
import numpy as np


#-o 
#-d 
parser = argparse.ArgumentParser()
parser.add_argument('-c','--pony_counts',help='pony counts')
parser.add_argument('-n','--num_words', nargs='?', help='num words')
args = parser.parse_args()

ponies = {
    "Twilight Sparkle": {    },
    "Applejack": {    },
    "Rarity": {    },
    "Pinkie Pie": {    },
    "Rainbow Dash": {    },
    "Fluttershy": {    },
}
def idf(w, pony_counts):
    num_ponies, ponies_used_w = 0,0
    for pony in pony_counts:
        num_ponies += 1
        if w in pony_counts[pony]:
            ponies_used_w += 1
    return np.log(num_ponies/ponies_used_w)
    
def tf(w,pony,pony_counts):
    return pony_counts[pony][w]

def tfidf(w,pony,pony_counts):
    return tf(w,pony,pony_counts)*idf(w,pony_counts)

def main():
    pony_file = args.pony_counts
    num_words = int(args.num_words)

    #load pony file
    with open(pony_file,'r') as f:
        pony_counts = json.load(f)
    
    ponies = count_dict(pony_counts,num_words)
    #TFIDF
    
    print(json.dumps(ponies,indent=1))

def count_dict(pony_counts,num_words):
    for pony in list(ponies.keys()):
        TF_IDF = [(w,tfidf(w,pony,pony_counts)) for w, count in pony_counts[pony].items()]
        TF_IDF.sort(key=lambda tup: tup[1], reverse=True)
        sorted_tfidf = TF_IDF[:num_words]
        ponies[pony] = [w[0] for w in sorted_tfidf]
    return ponies


if __name__ == '__main__':
    main()