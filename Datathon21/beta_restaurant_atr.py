from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import requests
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
import re
import MGP
import json
import torch

# Urls where all the data is stored
test_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/test_reviews.json'
train_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/train_reviews.json'

def get_reviews_from_restaurant(restaurant_title, online=True, url=''):
    '''Returns the descriptions of the reviews from the restaurant indicated.
    Variable online (bool) indicates if infomration must be extracted from url.
    '''
    if online:
        raw_data = requests.get(url).json()
    else:
        f = open('test_reviews.json')
        raw_data = json.load(f)
    descriptions = []
    for restaurant in raw_data:
        if restaurant['title'] == restaurant_title:
            for review in restaurant['reviews_data']:
                descriptions += review['snippet'].split('.')
            break
    return descriptions

def separate_into_words(list, symbols_to_remove='.,?!-'):
    '''Separates sentences of a list into a list of words, all uppercase
    and without the symbols indicated.'''

    new_list = []
    for element in list:
        new_list += [re.sub(symbols_to_remove, '', element).upper().split(' ')]

    return new_list



def process_mgp(restaurant_name, positive):
    '''Clusters words from positive (or negative according the 'positive' bool variable)
    reviews of the indicated restaurant_name'''

    # Setting our model and tokenizer and creating our classifier
    model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
    MODEL = torch.load('./trained model def_', map_location = 'cpu')
    TOKENIZER = DistilBertTokenizerFast.from_pretrained(model_name)
    classifier = pipeline('sentiment-analysis', model = MODEL, tokenizer = TOKENIZER)


    restaurant_reviews = get_reviews_from_restaurant(restaurant_name, online=False, url=test_url)
    results = classifier(restaurant_reviews)

    # Classifying our reviews into positive or negative according to our classifier
    positive_list = []
    negative_list = []
    labels_and_reviews = []
    for i in range(len(restaurant_reviews)):
        if results[i]['label'] == 'POSITIVE':
          positive_list += [restaurant_reviews[i]]
        else:
          negative_list += [restaurant_reviews[i]]

    # Formatting the lists to work with our cluster generator
    full_separated_positive = separate_into_words(positive_list)
    full_separated_negative = separate_into_words(negative_list)

    # Clustering the list chosen
    if positive:
        MGP.test(full_separated_positive)
    else:
        MGP.test(full_separated_negative)
