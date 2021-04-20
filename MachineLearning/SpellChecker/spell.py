# Check spelling of a word


class spell_checker():
    # Dictionary file
    def __init__(self, file_name):
        self.writer = open(file_name)
        # correct_word: variations
        self.word_dict = {'la': [], 'le': [], 'mo': [], 'pa': ['pas'], 'so': [], 'ti': ['chi'], 'de': ['2', 'd'], 'fer': ['faire', 'fr'], 'si': [], 'ou': [], 'pe': ['p'],
                          'ek': ['et', 'e'], 'enn': ['ene', '1', 'en', 'n', 'un'], 'sa': [], 'zot': ['zotte'], 'dan': ['dans'], 'pou': ['pour'], 'a': [], 'b': ['be'], 'li': [],
                          'dimoune': [], 'tou': ['tout'], 'c': [], 'twa': ['toi'], 'finn': ['in', 'fine'], 'byin': ['bien'], 'ki': ['qui'], 'mai': ['mais'], 'nou': ['nu'],
                          'gagne': ['ggne'], 'nous': ['nou'], 'vasin': ['vaccin'], 'mwa': ['moi'], 'vinn': ['vine'], 'bann': ['banne', 'ban'], 'covid-19': ['covid', 'corona'],
                          'premier ministre': ['pm'], 'to': ['t'], 'avek': ['avec'], 'mem': ['meme'], 'ar': ['r', 'are'], 'moris': ['maurice'], 'alle': [], 'gran': ['grand'],
                          'pri': ['prix', 'pris'], 'chatwa': [], 'mor': ['mort'], 'pays': [], 'kuma': ['couma'], 'pren': ['pren'], 'legime': ['legume'],
                          'kaka': ['kk', 'kkliki', 'kakaliki', 'kl'], 'liki': ['l', 'lkm', 'likitorma', 'boussou', 'busu', 'bousou'], 'gogot': ['ggt', 'g'], 'pilon': ['pln', 'peelon'],
                          'fesse': ['fes', 'f', 'fess', 'fss'], 'bour': ['boure', 'pez', 'viol'], 'falour': ['flm', 'falourmama', 'falomama'], 'graine': ['grain'],'bouss':['bouse','bousse','bous']}

    # Read dictionary file
    # Return: array of words
    def read_dic(self):
        kreol_words = self.writer.readlines()
        # Remove newline
        kreol_words = [kreol_word.replace('\n', '')
                       for kreol_word in kreol_words]
        return kreol_words

    # Is the word in the dictionary file?
    # Return boolean
    def is_dict(self, word):
        if word in self.read_dic():
            return True
        return False

    # Check if word is in the variation part of word_dict
    # Return boolean
    def is_variation(self, word):
        if word in [item for sublist in self.word_dict.values() for item in sublist]:
            return True
        return False

    # Return the correct spelling of word
    def correction(self, word):
        # Given value (wrong word), find the key (correct word)
        for key, value in self.word_dict.items():
            if word in value:
                return key
        return word

    # Return the correct spelling of words in a sentnece
    def correct_sent(self, sent):
        correct_sent = ""
        for word in sent.split():
            # print(word)
            # if word not in dicitonary
            if not self.is_dict(word):
                # if word in variation list
                if self.is_variation(word):
                    # append corrected word to sentence
                    correct_sent = correct_sent + " " + self.correction(word)
                else:
                    correct_sent = correct_sent + " " + word
            else:
                correct_sent = correct_sent + " " + word
        return correct_sent.lstrip()


