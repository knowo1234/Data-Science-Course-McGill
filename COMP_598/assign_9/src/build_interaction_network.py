import pandas as pd
import numpy as np
import argparse
import json
#-i
#-o
parser = argparse.ArgumentParser()
parser.add_argument('-i','--script',help='script')
parser.add_argument('-o','--output_file', help='outputfile')
args = parser.parse_args()

script = args.script
output = args.output_file

#we have to compute the interactions 
#remove all pony that are not valid
#we can compute the 101 most common ponys
#throw away all dictionary entries that are not in the 101 list

def main():
    script_df = open_and_load(script) #works
    
    #lowercase all pony names
    script_df.pony = script_df.pony.apply(lambda x: x.lower())
    #remove unneccesary columns
    script_df = script_df[['title','pony']]

    #compute the interactions between all ponies
    interactions = count_interactions(script_df)

    #create a list of null ponies NULL is 0 VALID is 1
    null_ponies = validate_ponies(script_df,0)
    valid_ponies = validate_ponies(script_df,1)

    #remove all null ponies
    remove_null_ponies(interactions,null_ponies,valid_ponies)

    #remove interactions that have count 0
    remove_0_values(interactions)

    #sort and limit dict lengths to 101
    top_101 = get_top_101(script_df,null_ponies)

    #remove all ponies that are now in the top 101
    keep_top_101(interactions,top_101)

    #remove pony talkin to itself
    remove_selftalk(interactions)

    #output the final dict to a json
    with open(output,'w') as f:
        json.dump(interactions,f,indent=4)


def remove_selftalk(interactions):
    try:
        for pony in interactions:
            del interactions[pony][pony]
    except:     
        pass

def keep_top_101(interactions,top_101):
    for pony in interactions:
        for k in list(interactions[pony]):
            if k not in top_101:
                del interactions[pony][k]
    for pony in list(interactions):
        if pony not in top_101:
            del interactions[pony]

def get_top_101(script_df,null_ponies):
    pony_df = pd.DataFrame(script_df.pony)
    pony_list = list(pony_df.pony)
    for x in pony_list:
        if x in null_ponies:
            pony_df = pony_df.drop(pony_df.index[pony_df['pony']==x],inplace=False)
    pony_df['number'] = 1
    top_101 = list(pony_df.groupby('pony').count().sort_values('number',ascending=False).head(101).index)
    return top_101

def remove_0_values(interactions):
    for pony in interactions:
        for k,v in list(interactions[pony].items()):
            if v == 0:
                del interactions[pony][k]
            
def remove_null_ponies(interactions,null_ponies,valid_ponies):
    #remove all null ponies from outer dict
    for pony in null_ponies:
        interactions.pop(pony)
    #remove all null ponies from inner dict
    for Vpony in valid_ponies:
        for pony in null_ponies:
            interactions[Vpony].pop(pony)

def validate_ponies(script_df,flag):
    all_unique_pony = script_df.pony.unique()
    valid_ponies = []
    for pony in all_unique_pony:
        split_pony = pony.split()
        if flag:
            if not('in' in split_pony or 'and' in split_pony or 'all' in split_pony or 'sans' in split_pony or 'except' in split_pony or 'rest' in split_pony or 'but' in split_pony or 'others' in split_pony or 'ponies' in split_pony):
                valid_ponies.append(' '.join(split_pony))
        if not flag:
            if ('in' in split_pony or 'and' in split_pony or 'all' in split_pony or 'sans' in split_pony or 'except' in split_pony or 'rest' in split_pony or 'but' in split_pony or 'others' in split_pony or 'ponies' in split_pony):
                valid_ponies.append(' '.join(split_pony))
    return valid_ponies

def count_interactions(script_df):
    interactions = {}
    internal = {}
    #populate dictionary with pony names
    for names in script_df.pony.unique():
        interactions.update({names:{}})
    #populate the outer ponies with inner pony dict
    for names in script_df.pony.unique():
        internal.update({names:0})
    #populate dictionary with pony names
    for names in script_df.pony.unique():
        interactions[names].update(internal)
    
    #create initial values
    title = script_df.iloc[[0]].title.values[0]
    pony = script_df.iloc[[0]].pony.values[0]

    #loop over the dialogs and populate the dictionary
    for i in range(1,len(script_df)-1):
        #if we are in the same episode
        if title is script_df.iloc[[i]].title.values[0]:#acess title on line i
            
            #check if the current pony and previous pony are differnt
            if pony is not script_df.iloc[[i]].pony.values[0]: #access pony on line i
                interactions[pony][script_df.iloc[[i]].pony.values[0]] = interactions[pony][script_df.iloc[[i]].pony.values[0]] +1
                interactions[script_df.iloc[[i]].pony.values[0]][pony] = interactions[script_df.iloc[[i]].pony.values[0]][pony] +1
        title = script_df.iloc[[i]].title.values[0]
        pony = script_df.iloc[[i]].pony.values[0]
    return interactions
   
def open_and_load(file): #opens the script csv and loads it into a dataframe
    with open(file,'r'):
        df = pd.read_csv(file)
        return df

if __name__ == '__main__':
    main()