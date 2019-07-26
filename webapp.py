from flask import Flask, render_template, request, redirect, url_for, flash, session
from translate_tweets import TranslateTweets
from twitter_client import TwitterAuthenticator
from sentiment_analyzer import SentimentAnalyzer
import tweepy
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import textblob

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'

####input your credentials here
consumer_key = 'wtFRuCKCv8uB4zchxPpj0IxF7'
consumer_secret = 'SUPHCNtK7QWe8fKpYwPt11CKQ9vWdGwawrrMaItEFIuuSAe9d1'
access_token = '2205718165-0nE4pGg3XxLVDQztEGdKmmiXfOkFBRPF4D7SDTm'
access_token_secret = 'n9HnBZgoH1gXUWEo8KGYepYkNHi9lyJNe3hnfEvmxxy67'

twitter_authenticator = TwitterAuthenticator(consumer_key, consumer_secret, access_token, access_token_secret)
api = twitter_authenticator.twitterClient()
   

@app.route('/')
def home():   
    #tweets_translated = TranslateTweets()
    #tweets_translated_array = tweets_translated.translate_tweets(tweets)
    return render_template('search.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        try:
                percentages = []
                quantities = []
                term = request.form['term']
                term = term + ' -filter:retweets'
                term = str(term)
                print(term)
                tweets = tweepy.Cursor(api.search, q=term, lang = 'es', tweet_mode='extended').items(10)
                tweets_translated = TranslateTweets()
                #tweets_full_text = tweets_translated.get_scores_list(tweets)
                tweets_full_text = tweets_translated.get_full_text_tweet(tweets)
                tweets_translated_array = tweets_translated.translate_tweets(tweets_full_text)
                array_tweets_score = tweets_translated.array_of_tweets_and_score_method()
                array_neutral = tweets_translated.order_array_of_tweets_neutral(array_tweets_score)
                array_positive = tweets_translated.order_array_of_tweets_postive(array_tweets_score)
                array_negative = tweets_translated.order_array_of_tweets_negative(array_tweets_score)
                text_neutral = tweets_translated.text_positive_only(array_neutral)
                text_positive = tweets_translated.text_positive_only(array_positive)
                text_negative = tweets_translated.text_negative_only(array_negative)
                array_without_zeros = tweets_translated.delete_zeros()
                percentage_neutral = tweets_translated.calculate_percentage_neutral()
                percentage_positive = tweets_translated.calculate_percentage_positive()
                percentage_negative = tweets_translated.calculate_percentage_negative()
                neutral_quantity = len(array_neutral)
                positive_quantity = len(array_positive)
                negative_quantity = len(array_negative)
                total_quantity = neutral_quantity + positive_quantity + negative_quantity
                percentages.extend([percentage_neutral, percentage_positive, percentage_negative])
                quantities.extend([neutral_quantity, positive_quantity, negative_quantity, total_quantity])
                data = [{"text_neutral": text_neutral}, {"text_positive": text_positive}, {"text_negative": text_negative}, {"percentages": percentages}, {"quantities": quantities}]
                scores_array = np.array(array_without_zeros)
                sns.set()
                ax = sns.distplot(scores_array)
                plt.show()
                return render_template('show.html', data = data)
        except tweepy.error.TweepError as e:
                print(e.reason)
        except textblob.exceptions.NotTranslated as e:
                print(e)

@app.route('/analysis')
def analysis():
        return render_template('searchAnalysis.html')

@app.route('/analysis/search', methods=['GET', 'POST'])
def analysisSearch():
        if request.method == 'POST':
                quantities = []
                term = request.form['term']     #Term that user types
                term = term + ' -filter:retweets'       #Exclude retweets
                term = str(term)                        #converting term to string
                tweets = tweepy.Cursor(api.search, q=term, lang = 'es', tweet_mode='extended').items(150)       #getting 150 tweets
                sentiment_analyzer = SentimentAnalyzer()        #instanciate the class SentimentAnalyzer
                scores_list = sentiment_analyzer.get_scores_list(tweets)        #get the list of scores without zeros
                array_tweets_score = sentiment_analyzer.array_of_tweets_and_score_method()      #get array of objects with text and score
                arrays_ordered = sentiment_analyzer.order_arrays_list()                 #list in order to create arrays ordered
                text_positive = sentiment_analyzer.get_postive_text(arrays_ordered)     #get only positive text
                text_negative = sentiment_analyzer.get_negative_text(arrays_ordered)    #get only negative text
                text_neutral = sentiment_analyzer.get_neutral_text(arrays_ordered)      #get only neutral text
                percentages = sentiment_analyzer.get_percentages()                      #get percentages
                positive_quantity = len(text_positive)                                  #get quantity of positive tweets
                negative_quantity = len(text_negative)                                  #get quantity of negative tweets
                neutral_quantity = len(text_neutral)                                    #get quantity of neutral tweets
                total_quantity = positive_quantity + negative_quantity + neutral_quantity       #get quantity of total tweets
                quantities.extend([positive_quantity, negative_quantity, neutral_quantity, total_quantity])     #insert quantites in array
                data = [{"text_positive": text_positive}, {"text_negative": text_negative}, {"text_neutral": text_neutral}, {"percentages": percentages}, {"quantities": quantities}]                                   #creating the array that will be send to the template
                scores_array = np.array(scores_list)                                        #for plotting
                sns.set()                                                                   #for plotting
                ax = sns.distplot(scores_array)                                                 
                plt.show()                                                                  #for plotting
                return render_template('showAnalysis.html', data = data)                    #rendering showAnalysis and passing data as data

if __name__ == '__main__':
    app.run(port = 4000, host='0.0.0.0', debug=True)
    