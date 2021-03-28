# Preprocess raw dataset and
# save processed comments in  a new file
# TO DO- Normalization
from SpellChecker.spell import spell_checker
import demoji
import pandas as pd
import re


class Preprocess:
    # dataset_name -> raw dataset location
    # new_dataset_name -> processed dataset location
    def __init__(self, dataset_name, new_dataset_name):
        self.df = pd.read_csv(dataset_name)
        self.new_ds_name = new_dataset_name

    # Cleaning - Lowercase all characters
    def lower_case(self):
        self.df["processed_comments"] = self.df["Comments"].str.lower()

    def remove_emogies(self):
        no_emoji = []
        for comment in self.df["processed_comments"]:
            no_emoji.append(demoji.replace(comment, " "))

        self.df["processed_comments"] = no_emoji

    # do after normalisation to cater for words such as "pil..." and "f..."
    # Cleaning - remove punctuations
    def remove_punctuations(self):
        self.df["processed_comments"] = self.df["processed_comments"].str.replace('[^\w\s]', ' ')

    # Cleaning - remove urls
    def remove_urls(self):
        no_url = []
        regex_str = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        url_pattern = re.compile(regex_str)

        for comment in self.df["processed_comments"]:
            no_url.append(url_pattern.sub(r'', comment))

        self.df["processed_comments"] = no_url

    # Normalization --TO DO
    def correct_spelling(self):
        sp = spell_checker('SpellChecker/KreolDictionary.txt')
        correct_comments = [] # List of correct spelling for each comment
        # Read each comment in from df (for loop with index)
        for comment in self.df["processed_comments"]:
            correct_comments.append(sp.correct_sent(comment))
            
        self.df["processed_comments"] = correct_comments

    #  top 20 frequent words as stop words after examination
    def remove_stopwords(self,comment):
        stop_words = ['la', 'le', 'mo', 'pa', 'so', 'ti', 'de', 'fer', 'si',
            'ou', 'pe', 'ek', 'enn', 'sa', 'zot', 'dan', 'pou', 'a', 'b', 'li']
        # Remove stop word
        return " ".join([word for word in str(comment).split() if word not in stop_words])

    # Passing function remove_stopwords()
    # Saving the processed comments into the dataframe
    def removeStopwordSave(self):
        self.df["processed_comments"] = self.df["processed_comments"].apply(lambda text: self.remove_stopwords(text))

    def combine_whitespace(self):
        combine_space = []

        for comment in self.df["processed_comments"]:
            no_space = ' '.join(comment.split())
            combine_space.append(no_space)

        self.df["processed_comments"] = combine_space

    # Cleaning - Remove null values from dataset
    def remove_null(self):
        self.df = self.df.drop(self.df[self.df["processed_comments"] == ''].index)
        self.df.dropna()
        
    # Remove unique words such as names
    def remove_rareWords():
        pass

    def tokenize(text):
        pass

    def preprocess(self):
        # Call all the preprocessing functions
        self.lower_case()
        self.remove_emogies()
        self.remove_urls()
        self.remove_punctuations()
        self.combine_whitespace()
        self.correct_spelling()
        self.removeStopwordSave()
        self.remove_null()

        # Write the preprocess dataset to a new file
        self.df.to_csv(self.new_ds_name, index=False, header=True)

        # Returned the processed comments along with its labels as a dataframe
        return self.df


def main():
    pr = Preprocess("SmallDatasets/smallDataset.csv","SmallDatasets/processSmallDataset.csv")
    # pr = Preprocess("Datasets/Dataset.csv","Datasets/processDataset.csv")
    print(type(pr.preprocess()))
    

if __name__ == "__main__":
    main()
