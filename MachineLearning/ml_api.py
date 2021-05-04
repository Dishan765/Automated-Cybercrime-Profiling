from flask import Flask, request, jsonify
from SpellChecker.spell import spell_checker
import pickle
import os
import demoji
import re


def lowercase(data):
    data = data.lower()
    return data


def remove_emogies(data):
    data = demoji.replace(data, " ")
    return data


def remove_urls(data):
    regex_str = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    url_pattern = re.compile(regex_str)

    data = url_pattern.sub(r'', data)
    return data


def remove_punctuations(data):
    #data = data.replace('[^\w\s]', ' ')
    data = re.sub(r'[^\w\s]',' ',data)
    return data


def combine_whitespace(data):
    data = ' '.join(data.split())
    return data

def correct_spelling(data):
    sp = spell_checker('SpellChecker/KreolDictionary.txt')
    data = sp.correct_sent(data)
    return data


def remove_stopwords(data):
    stop_words = ['la', 'le', 'mo', 'pa', 'so', 'ti', 'de', 'fer', 'si',
            'ou', 'pe', 'ek', 'enn', 'sa', 'zot', 'dan', 'pou', 'a', 'b', 'li']
    data = " ".join([word for word in str(data).split() if word not in stop_words])
    return data

def remove_special_char(data):
    # define the pattern to keep
    pat = r'[^a-zA-z.,!?/:;\"\'\s]' 
    data =  re.sub(pat, '', data)
    return data


def preprocess(data):
    data = lowercase(data)
    data = remove_emogies(data)
    data = remove_urls(data)
    data = remove_punctuations(data)
    data = correct_spelling(data)
    data = remove_stopwords(data)
    data = remove_special_char(data)
    data = combine_whitespace(data)
    return data


# Path where model is located (LRclassifier.py)
# os.chdir('MachineLearning/Models')
file_name = 'Models/LRclassifier.pkl'
# Load Model
with open(file_name, 'rb') as training_model:
    model = pickle.load(training_model)

app = Flask(__name__)

@app.route('/ml_api', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    data = preprocess(data['sentence'])
    predict_request = [data]
    # request = np.array(predict_request)
    print(predict_request)
    prediction = model.predict(predict_request)
    # pred = prediction[0]
    print(prediction)
    return jsonify(int(prediction))


if __name__ == '__main__':
    print(preprocess("DATA      😉 😌 😍 🥰 😘 data www.google.com :) .@ 12 3333 .  🙃 😗  to ek kk pln flm   twa toi kaka kkliki mo pa so "))
    # from werkzeug.serving import run_simple
    #app.run(port=9000, debug=True)
