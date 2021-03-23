# TO DO- Normalization

import demoji
import pandas as pd
import re
from collections import Counter

# Preprocess raw dataset and
# save processed comments in  a new file


class Preprocess:
    # dataset_name -> raw dataset location
    # new_dataset_name -> processed dataset location
    def __init__(self, dataset_name, new_dataset_name):
        self.df = pd.read_csv(dataset_name)
        self.new_ds_name = new_dataset_name
        #self.PUNCT_TO_REMOVE = string.punctuation
        # df.head()

    # Cleaning - Lowercase all characters
    def lower_case(self):
        self.df["text_lower"] = self.df["Comments"].str.lower()
        self.df["Comments"] = self.df["text_lower"]

    def remove_emogies(self):
        no_emoji = []
        for comment in self.df['Comments']:
            no_emoji.append(demoji.replace(comment, " "))

        self.df['Comments'] = no_emoji

    # Normalization --TO DO

    def correct_spelling(text):
        pass

    # do after normalisation to cater for words such as "pil..." and "f..."
    # Cleaning - remove punctuations
    def remove_punctuations(self):
        self.df['remove_punct'] = self.df['Comments'].str.replace(
            '[^\w\s]', ' ')
        self.df["Comments"] = self.df["remove_punct"]

    # Cleaning - remove urls

    def remove_urls(self):
        no_url = []
        regex_str = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        url_pattern = re.compile(regex_str)

        for comment in self.df['Comments']:
            no_url.append(url_pattern.sub(r'', comment))

        self.df['Comments'] = no_url

    # Remove unique words such as names
    def remove_rareWords():
        pass

    #  top 30 frequent words as stop words after examination
    # + add some from my own knowledge
    def remove_stopwords(self):

        #Get to 20 common words
        # cnt = Counter()
        # for text in self.df["text_stop"].values:
        #     for word in text.split():
        #         cnt[word] += 1
        
        # common_words = cnt.most_common(30)
        # stop_words = []
        # for cw in common_words:
        #     stop_words.append(cw[0])


        stop_words = ['la', 'to', 'ki', 'pe', 'p', 'sa', 'li', 'pou', 'ou', 'pa', 'mo', 'ti', 'ena', 'et', 'ek', 'so', 'ene', 'nou', 'tou', 'pu', 'fer', 'la', 'la', 'to', 'to', 'ki', 'ki', 'p', 'p', 'sa', 'sa', 'li', 'li', 'pou', 'pou', 'ou', 'ou', 'pa', 'pa', 'mo', 'mo', 'pas', 'pas', 'ti', 'ti', 'ena', 'ena', 'zotte', 'zotte', 'fer', 'fer', 'faire', 'faire', 'dire', 'dire', 'zot', 'zot', 'et', 'et', 'so', 'so', 'le', 'le', 'en', 'en', 'pe', 'pe', 'pu', 'pu', '1', '1', 'les', 'les', 'r', 'r', 'si', 'si', 'tou', 'tou', 'dir', 'dir']
        

    def tokenize(text):
        pass

    def combine_whitespace(self):
        combine_space = []

        for comment in self.df['Comments']:
            no_space = ' '.join(comment.split())
            combine_space.append(no_space)

        self.df['Comments'] = combine_space

    # Cleaning - Remove null values from dataset
    def remove_null(self):
        self.df = self.df.dropna()

    def preprocess(self):
        # Call all the preprocessing functions
        self.lower_case()
        self.remove_emogies()
        self.remove_urls()
        self.remove_punctuations()
        self.combine_whitespace()
        self.remove_null()

        # Drop all the other added columns
        self.df.drop(["text_lower"], axis=1, inplace=True)
        self.df.drop(["remove_punct"], axis=1, inplace=True)

        # Write the preprocess dataset to a new file
        self.df.to_csv(self.new_ds_name, index=False, header=True)


def main():
    pr = Preprocess("SmallDatasets/smallDataset.csv",
                    "SmallDatasets/processSmallDataset.csv")
    pr.preprocess()


if __name__ == "__main__":
    main()
