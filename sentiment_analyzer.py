from repustate import Client

client = Client(api_key = 'f8bc4e11603bbfcd6737510a95873625d6d2330c', version = 'v4')

"""
Creating a class
"""

class SentimentAnalyzer():
    def __init__(self, scores_list=[], array_of_tweets_and_score=[]):
        self.scores_list = []
        self.array_of_tweets_and_score = []

    def get_scores_list(self, tweets):      #Function to get the list of scores, first get full text, then get scores from Repustate, then create                                          array with objects, return the list of scores without zeros
        scores = []
        newList = [tweet.full_text for tweet in tweets]
        for comment in newList:
            score = client.sentiment(comment, lang='es')
            scores.append(score)
            self.array_of_tweets_and_score.append({'text': comment, 'score': score['score']})
        self.scores_list = [score['score'] for score in scores]
        new_scores_list = [score for score in self.scores_list if score != 0]
        return new_scores_list

    def array_of_tweets_and_score_method(self):     #return the object that has been created in the func before
        return self.array_of_tweets_and_score
    
    def order_arrays_list(self):                    #function that oreders the arrays using list comprenhension
        positive_array = [element for element in self.array_of_tweets_and_score if element['score'] > 0]
        negative_array = [element for element in self.array_of_tweets_and_score if element['score'] < 0]
        neutral_array = [element for element in self.array_of_tweets_and_score if element['score'] == 0]
        return [positive_array, negative_array, neutral_array]
        """
        positive_array = []
        for element in self.array_of_tweets_and_score:
            if element['score] > 0:
                positive_array.append(element)
        """
    
    def get_postive_text(self, array_ordered):          #funcs that returns the text positive
        text_positive = [element['text'] for element in array_ordered[0]]
        return text_positive
        """
        text_positive = []
        for element in array_ordered[0]:
            text.positive.append(element['text])
        """
    
    def get_negative_text(self, array_ordered):
        text_negative = [element['text'] for element in array_ordered[1]]
        return text_negative
    
    def get_neutral_text(self, array_ordered):
        text_neutral = [element['text'] for element in array_ordered[2]]
        return text_neutral

    def get_percentages(self):                  #func that returns percentages
        total = len(self.scores_list)
        positive = [score for score in self.scores_list if score > 0]
        positive_percentage = ((len(positive) * 100) / total)
        negative = [score for score in self.scores_list if score < 0]
        negative_percentage = ((len(negative) * 100) / total)
        neutral = [score for score in self.scores_list if score == 0]
        neutral_percentage = ((len(neutral) * 100) / total)
        return [positive_percentage, negative_percentage, neutral_percentage]

    