# Create a list of Kreol words from online dictionary found at:
# https://www.lalitmauritius.org/en/dictionary.html?letter=a

from bs4 import BeautifulSoup
from selenium import webdriver
import string
import time
import re
import string

class KreolDic():

    # constructor
    def __init__(self):
        self.driver = webdriver.Firefox()
        # the last variable is the initial letter of words in dictionary
        # added in function scrap_words
        self.URL = "https://www.lalitmauritius.org/en/dictionary.html?letter="

    # destructor
    def __del__(self):
        self.driver.quit()

    def scrap_words(self):
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        word_list = []

        for alpha in alphabet_list:
            # Opens link to dictionary URL for each alphabet
            self.driver.get(self.URL + alpha)
            time.sleep(10)
            # and get HTML content
            #page = self.driver.execute_script('return document.body.innerHTML')
            page = self.driver.page_source

            # Create a BeautifulSoup object
            soup = BeautifulSoup(page, 'lxml')
            # Get whole <ul> tag with id 'dictionarylist'
            # Contains a list of <li> with words
            section_ul = soup.find('ul', id='dictionarylist')
            # Find all <li>s
            section_li = section_ul.findAll('li')

            for li in section_li:
                # For each <li> get main word (class = 'main')
                word = li.find('span', {'class': 'main'}).text
                #Remove words (aks,...) in brakets
                word = re.sub(r"\([^()]*\)", '', word)
                # Remove trailing whitespaces
                word = word.strip()
                word_list.append(word)

                # For each <li> class = 'variations'
                word = li.find('span', {'class': 'variations'})
                if word:
                    word = word.text
                    #Reomve word 'Variation(s)'before term of inteterst
                    word = word.replace('Variation(s): ','')
                    #split multiple words by comma
                    word = word.split(',')

                    for w in word:
                        # Remove trailing whitespaces
                        modified_word = w.strip()
                        word_list.append(modified_word)

        return word_list
    
    #Write a list to a file
    def write_file(self,words,file_name):
        with open(file_name, 'a') as fw:
            for word in words:
                fw.write(f"{word}\n")

def main():
    kc = KreolDic()
    words_list = kc.scrap_words()
    kc.write_file(words_list,"KreolDictionary.txt")

    del kc


if __name__ == "__main__":
    main()
