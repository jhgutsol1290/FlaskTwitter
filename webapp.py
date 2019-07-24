from flask import Flask, render_template, request, redirect, url_for, flash, session
from translate_tweets import TranslateTweets
from twitter_client import TwitterAuthenticator
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
                term = str(term)
                tweets = tweepy.Cursor(api.search, q=term, lang = 'es', tweet_mode='extended').items(100)
                tweets_translated = TranslateTweets()
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

if __name__ == '__main__':
    app.run(port = 4000, host='0.0.0.0', debug=True)
    