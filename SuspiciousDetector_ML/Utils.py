#Get words that need to be included in the dictionary
import pandas as pd
from collections import Counter

 # Get top 30 common words
def commonWords(fileName):
    df = pd.read_csv(fileName)
    cnt = Counter()
    for text in df["Comments"].values:
        for word in text.split():
            cnt[word] += 1
    
    common_words = cnt.most_common(30)
    print(common_words)
    stop_words = []
    for cw in common_words:
        stop_words.append(cw[0])

    print(set(stop_words))


#correctWord:Variations
stop_dict = {'la':[], 'le':[],'mo':[],'pa':['pas'],'so':[],'ti':['chi'],'de':['2','d'],
                'fer':['faire','fr'], 'si':[],'ou':[],'pe':['p'], 'ek':['et'], 'enn':['ene','1','en','n','un'],
                'sa':[],'zot':['zotte'],'dan':['dans'],'pou':['pu'],'a':[],'b':['be'],'li':[]}

#Find the top 30/50 misspelled words
def misspell(fileName):
    word_variation_count = {}

    df = pd.read_csv(fileName)
    with open("SpellChecker/KreolDictionary.txt") as fr:
        kreol_words = fr.readlines()

    # Replace newline with empty string
    kreol_words = [kreol_word.replace('\n','') for kreol_word in kreol_words]

    cnt = Counter()
    for comment in df['Comments'].values:
        for word in comment.split():
            # Check if word is a key in dictionary
            if not(word in stop_dict):
                # Check if word is a value in dictionary
                if not(word in [item for sublist in stop_dict.values() for item in sublist]):
                    if not(word in kreol_words):
                        cnt[word]+=1

    print(cnt.most_common(50))
    first_cnt_elements = [cnt_tuple[0] for cnt_tuple in cnt.most_common(50)]
    print(first_cnt_elements)

# commonWords("/Datasets/processDataset.csv")
# misspell("/Datasets/processDataset.csv")

word_variations = {'dimoune':[],'tou':[], 'c':[], 'twa':['toi'], 'finn':['in','fine'], 'bien':[], 
'ki':['qui'], 'mai':['mais'], 'nou':['nu'], 'gagne':['ggne'], 'tou':['tout'], 'pou':['pour'], 
'nous':['nou'], 'vaccin':['vasin'], 'moi':['mwa'], 'vinn':['vine'], 'bann':['bane','banne'], 
'covid-19':['covid','corona'], 'premier ministre':['pm'], 'avek':['avec'], 'mem':['meme'], 'ar':['ar','are']
,'moris':['maurice'], 'alle':[], 'gran':['grand'], 'pri':['prix','pris'], 'chatwa':[], 
'mor':['mort'],'peyi':['payi'], 'kuma':['couma'],'pren':['pren'], 'legime':['legume'], 
'bann':['banne','ban'], 'kaka':['kk'], 'l':['liki'],'gogot':['ggt','g'],
'pilon':['p']}

print(stop_dict.keys())
word_variations = z = {**stop_dict, **word_variations}
print("*********************************")
print(word_variations)