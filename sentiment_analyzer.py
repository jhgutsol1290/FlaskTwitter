from repustate import Client

client = Client(api_key = 'c53d0c7b21b8afb62c4c112a9f4f1070ee6ff308', version = 'v4')

class SentimentAnalyzer():
    def get_scores_list(self, tweets):
        scores = []
        newList = [tweet.full_text for tweet in tweets]
        for comment in newList:
            score = client.sentiment(comment, lang='es')
            scores.append(score)
        return scores