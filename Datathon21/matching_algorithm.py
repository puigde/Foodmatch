test_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/test_reviews.json'
train_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/train_reviews.json'
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
test_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/test_reviews.json'
train_url = 'https://raw.githubusercontent.com/data-students/datathon2021/main/Reviews_Challenge/train_reviews.json'
import requests
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast
import torch
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments

model = torch.load('./trained model def_',map_location ='cpu')
model_name= "distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
classifier= pipeline("sentiment-analysis", model= model, tokenizer= tokenizer)

def is_positive(statement):
    '''Returns true if a statements if positive, negative otherwise'''
    if len(statement)>512:
        statement = statement[:500]
    result = classifier(statement)
    if result[0]['label']== 'POSITIVE': return True
    return False


def get_restaurant_titles(url1, url2):
    '''Returns a dictionary containing the restaurant title and descriptions out of the urls.'''
    d = {}
    condition = True
    raw_data = requests.get(url1).json()
    raw_data += requests.get(url2).json()
    for restaurant in raw_data:
        d[restaurant['title']] = []
        for review in restaurant['reviews_data']:
            descr = review['snippet']
            d[restaurant['title']] += [descr]
    return d

def matching(string_input):
    '''Generates a dictionary with how many times each word appears in the
    positive reviews, and returns a list with the top 5'''
    
    input_list = string_input.split(",")
    
    # Generating the dictionary
    points = {}
    restaurants = get_restaurant_titles(train_url, test_url)
    for restaurant in restaurants:
        restaurant_points = 0
        for review in restaurants[restaurant]:
            for word in input_list:
                if review.find(word) != -1 and is_positive(review): restaurant_points += 1
        points[restaurant] = restaurant_points
        
    sorted_points = {k: v for k, v in sorted(points.items(), key=lambda item: item[1])}
    top5 = {}
    
    # Getting the top 5
    for r in reversed(sorted_points):
        top5[r] = sorted_points[r]
        if len(top5) == 5: break
            
    top5_list = []
  
    for key in top5:
        top5_list += [key]
    return top5_list


