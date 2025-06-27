from datetime import datetime
from fastapi import HTTPException


def validate_date(date_str: str) -> datetime.date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Fecha inválida. Utiliza el formato YYYY-MM-DD.")
    

import pandas as pd
import preprocessor as p
import numpy as np
import random
import re, string, unicodedata
#Para procesamiento del lenguaje natural
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk import WordPunctTokenizer
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

import string
from string import punctuation
import collections
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import en_core_web_sm
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from langdetect import detect
from sklearn.metrics import jaccard_score
from os import listdir
import gensim
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText
from nltk import word_tokenize,pos_tag

import string
from string import punctuation

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
en_stop = set(nltk.corpus.stopwords.words('english'))

def lemmatize_text(text):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    w_tokenizer =  TweetTokenizer()
    return [(lemmatizer.lemmatize(w)) for w \
                    in w_tokenizer.tokenize((text))]
def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_hashtags(text, replace=''):
    pattern = r'(^|\s)#(\S+)'
    text = re.sub(pattern, ' ' + replace, text).strip()    
    
    return text

def replace_urls(text, replace=''):
    pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    text = re.sub(pattern, replace, text).strip()    
    
    return text

def replace_mentions(text, replace=''):
    pattern = r'(^|\s)@[\S]+'
    text =  re.sub(pattern, ' ' + replace, text).strip()
    return text


def preprocess_text(text, numbers, caps, hashtags, urls, mentions, stopwords_l, lemmatize, stemming, punctuation, tags):
    """
    Processes a given text string by applying a series of text preprocessing techniques.
    
    Parameters:
        text (str): The input text to be preprocessed.
        numbers (str): Determines whether to remove or replace numbers in the text. 
            If set to 'noapply', numbers are not modified. 
            If set to a string value, all numbers in the text are replaced with the provided string.
        caps (str): Determines whether to convert the text to lowercase or uppercase. 
            If set to 'lowercase', the text is converted to lowercase. 
            If set to 'uppercase', the text is converted to uppercase. 
            If set to any other value, the text is left unchanged.
        hashtags (str): Determines whether to remove or replace hashtags from the text.
            If set to 'noapply', hashtags are not modified.
            If set to a string value, all hashtags in the text are replaced with the provided string.
        urls (str): Determines whether to remove or replace URLs from the text.
            If set to 'noapply', URLs are not modified.
            If set to a string value, all URLs in the text are replaced with the provided string.
        mentions (str): Determines whether to remove or replace mentions from the text.
            If set to 'noapply', mentions are not modified.
            If set to a string value, all mentions in the text are replaced with the provided string.
        stopwords_l (str): Determines the set of stopwords to use. 
            If set to 'english' or 'en', the function uses the set of English stopwords provided by the Natural Language Toolkit (nltk).
        lemmatize (bool): Determines whether to lemmatize the text using the WordNet lemmatizer provided by the nltk library.
        stemming (bool): Not implemented in the current version.
        punctuation (bool): Determines whether to remove all punctuation marks from the text.
        tags (bool): Determines whether to apply part-of-speech tagging to the text using the pos_tag() function provided by the nltk library.

    Returns:
        list: The modified tokenized list.

    """

    # Hashtags
    if hashtags != 'noapply':
        text = replace_hashtags(text, hashtags)

    print(text)
    
    # URLs
    if urls != 'noapply':
        text = replace_urls(text, urls)

    print(text)

    # Mentions
    if mentions != 'noapply':
        text = replace_mentions(text, mentions)
    
    print(text)

    data = nltk.word_tokenize(text)

    # Removes Numbers or replace them
    if numbers != 'noapply':
        data = [re.sub(r'\d+', numbers, token) for token in data]
    
    # Lowercase, uppercase or ignore
    if caps == 'lowercase':
        data = [token.lower() for token in data]      
    elif caps == 'uppercase':
        data = [token.upper() for token in data]  

    # Stopwords english
    if stopwords_l == 'english' or stopwords_l == 'en':
        stop_words = set(stopwords.words("english"))        
        data = [token for token in data if not token in stop_words]

    # Lemmatize
    if lemmatize:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        data = [lemmatizer.lemmatize(token) for token in data]

    # Punctuation
    if punctuation:
        data = [re.sub(r'[^\w\s]', '', (token)) for token in data]

    # Remove empty ones
    data = [token.strip() for token in data if token.strip() != ""]

    # Tags
    if tags:
        data = [pos_tag(word_tokenize(token)) for token in data]

    return data


def preprocess_df(df, col_name, numbers, caps, stopwords_l, lemmatize, stemming, punctuation, tags):
    """
    Processes a given column in a dataframe by applying a series of text preprocessing techniques.
    
    Parameters:
        df (pandas DataFrame): The input dataframe.
        col_name (str): The name of the column to preprocess.
        numbers (str): Determines whether to remove or replace numbers in the text. 
            If set to 'noapply', numbers are not modified. 
            If set to a string value, all numbers in the text are replaced with the provided string.
        caps (str): Determines whether to convert the text to lowercase or uppercase. 
            If set to 'lowercase', the text is converted to lowercase. 
            If set to 'uppercase', the text is converted to uppercase. 
            If set to any other value, the text is left unchanged.
        stopwords_l (str): Determines the set of stopwords to use. 
            If set to 'english' or 'en', the function uses the set of English stopwords provided by the Natural Language Toolkit (nltk).
        lemmatize (bool): Determines whether to lemmatize the text using the WordNet lemmatizer provided by the nltk library.
        stemming (bool): Not implemented in the current version.
        punctuation (bool): Determines whether to remove all punctuation marks from the text.
        tags (bool): Determines whether to apply part-of-speech tagging to the text using the pos_tag() function provided by the nltk library.

    Returns:
        pandas DataFrame: The modified dataframe with the column preprocessed.

    """
    data = df[col_name].copy()

    # Tokenize
    data = data.apply(nltk.word_tokenize)

    # Removes Numbers or replace them
    if numbers != 'noapply':
        data = data.apply(lambda x: [re.sub(r'\d+', numbers, token) for token in x])

    # Lowercase, uppercase or ignore
    if caps == 'lowercase':
        data = data.apply(lambda x: [token.lower() for token in x])      
    elif caps == 'uppercase':
        data = data.apply(lambda x: [token.upper() for token in x])

    # Stopwords english
    if stopwords_l == 'english' or stopwords_l == 'en':
        stop_words = set(stopwords.words("english"))        
        data = data.apply(lambda x: [token for token in x if not token in stop_words])

    # Lemmatize
    if lemmatize:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        data = data.apply(lambda x: [lemmatizer.lemmatize(token) for token in x])

    # Punctuation
    if punctuation:
        data = data.apply(lambda x: [re.sub(r'[^\w\s]', '', (token)) for token in x])

    # Remove empty ones
    data = data.apply(lambda x: [token.strip() for token in x if token.strip() != ""])

    # Tags
    if tags:
        data = data.apply(lambda x: [pos_tag(word_tokenize(token)) for token in x])

    # Replace original column with preprocessed data
    df[col_name] = data

    return df


import threading

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return

