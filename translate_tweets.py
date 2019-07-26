from textblob import TextBlob
import numpy as np
from repustate import Client

client = Client(api_key = 'c53d0c7b21b8afb62c4c112a9f4f1070ee6ff308', version = 'v4')


class TranslateTweets():
    def __init__(self, array_of_tweets_translated=[], array_of_tweets_and_score=[], tweets_arr = []):
        self.array_of_tweets_translated = []
        self.array_of_tweets_and_score = []
        self.tweets_arr = []
    
    def get_full_text_tweet(self, tweets):
        for tweet_info in tweets:
            if 'retweeted_status' in dir(tweet_info):
                pass
            else:
                tweet = tweet_info.full_text
                self.tweets_arr.append(tweet)
        return self.tweets_arr

    def translate_tweets(self, tweets):
        #array_of_tweets = np.array([tweet.full_text for tweet in tweets])
        for tweet in tweets:
            t = TextBlob(tweet)
            ten = t.translate(to="en")
            self.array_of_tweets_translated.append(ten.sentiment[0])
            self.array_of_tweets_and_score.append({"text": tweet, "score": ten.sentiment[0]})
        return self.array_of_tweets_translated

    def array_of_tweets_and_score_method(self):
        return self.array_of_tweets_and_score
    
    def order_array_of_tweets_neutral(self, array_tweets_score):
        array_neutral = [element for element in array_tweets_score if element['score'] == 0]
        return array_neutral
        """ array_neutral = []
        for element in array_tweets_score:
            if element['score'] == 0:
                array_neutral.append(element)
        return array_neutral """

    def order_array_of_tweets_postive(self, array_tweets_score):
        array_positive = [element for element in array_tweets_score if element['score'] > 0]
        return array_positive
        """ array_positive = []
        for element in array_tweets_score:
            if element['score'] > 0:
                array_positive.append(element)
        return array_positive """

    def order_array_of_tweets_negative(self, array_tweets_score):
        array_negative = [element for element in array_tweets_score if element['score'] < 0]
        return array_negative
        """ array_negative = []
        for element in array_tweets_score:
            if element['score'] < 0:
                array_negative.append(element)
        return array_negative """
    
    def text_neutral_only(self, array_neutral):
        text_neutral = [comment['text'] for comment in array_neutral]
        return text_neutral
  
    def text_positive_only(self, array_positive):
        text_positive = [comment['text'] for comment in array_positive]
        return text_positive

    def text_negative_only(self, array_negative):
        text_negative = [comment['text'] for comment in array_negative]
        return text_negative

    def delete_zeros(self):
        new_score_list = [score for score in self.array_of_tweets_translated if score != 0]
        return new_score_list
        """ new_score_list = []
        for score in self.array_of_tweets_translated:
            if score == 0:
                pass
            else:
                new_score_list.append(score)
        return new_score_list """
  
    def calculate_percentage_neutral(self):
        neutral_scores = [score for score in self.array_of_tweets_translated if score == 0]
        neutral_percentage = (len(neutral_scores) * 100 / len(self.array_of_tweets_translated))
        return neutral_percentage
        """ total = len(self.tweets_arr)
        neutral = []
        for score in self.array_of_tweets_translated:
            if score == 0:
                neutral.append(score)
        neutral_result = ((len(neutral)) * 100 / total)
        return neutral_result """
  
    def calculate_percentage_positive(self):
        positive_scores = [score for score in self.array_of_tweets_translated if score > 0]
        positive_percentage = (len(positive_scores) * 100 / len(self.array_of_tweets_translated))
        return positive_percentage
        """ total = len(self.tweets_arr)
        positive = []
        for score in self.array_of_tweets_translated:
            if score > 0:
                positive.append(score)
        positive_result = ((len(positive)) * 100 / total)
        return positive_result """

    def calculate_percentage_negative(self):
        negative_scores = [score for score in self.array_of_tweets_translated if score < 0]
        negative_percentage = (len(negative_scores) * 100 / len(self.array_of_tweets_translated))
        return negative_percentage
        """ total = len(self.tweets_arr)
        negative = []
        for score in self.array_of_tweets_translated:
            if score < 0:
                negative.append(score)
        negative_result = ((len(negative)) * 100 / total)
        return negative_result """