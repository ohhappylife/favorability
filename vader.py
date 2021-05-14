import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

# Get current date
now = datetime.now()
date = now.strftime("%m/%d/%Y")
date = date.replace("/", '_')
nations = ["china", "korea", "Japan"]

for x in nations:

    # Read the Crawled data
    df = pd.read_csv(date + "_" + x + "_twitter.csv")

    # If there is no file, then make one
    if not os.path.exists("result_vader_" + x + ".csv"):
      df2 = pd.DataFrame(columns = ['date', 'pos','neu','neg', 'comp'])
      result_vader = df2
      df2.to_csv("result_vader_" + x + ".csv", index=False)
    # If there is a file, then import it
    else:
      result_vader = pd.read_csv("result_vader_" + x + ".csv")

    # sentiment...
    sid_obj = SentimentIntensityAnalyzer()

    def pos(x):
        sentiment_dict = sid_obj.polarity_scores(x)
        return sentiment_dict['pos']
    def neu(x):
        sentiment_dict = sid_obj.polarity_scores(x)
        return sentiment_dict['neu']
    def neg(x):
        sentiment_dict = sid_obj.polarity_scores(x)
        return sentiment_dict['neg']
    def comp(x):
        sentiment_dict = sid_obj.polarity_scores(x)
        return sentiment_dict['compound']

    # convert from dict type to string type
    df['tweet_text'] = df['tweet_text'].astype(str)

    # sentiment analysis
    df['senti_score_pos'] = df['tweet_text'].apply(pos)
    df['senti_score_neg'] = df['tweet_text'].apply(neg)
    df['senti_score_neu'] = df['tweet_text'].apply(neu)
    df['senti_score_comp'] = df['tweet_text'].apply(comp)

    # average [mean] value
    avg_pos = sum(df.senti_score_pos)/len(df.senti_score_pos)
    avg_neutral = sum(df.senti_score_neg)/len(df.senti_score_neg)
    avg_negative = sum(df.senti_score_neu)/len(df.senti_score_neu)
    avg_compound = sum(df.senti_score_comp)/len(df.senti_score_comp)

    # store the values
    new_row = {'date': date, 'pos':avg_pos,'neu':avg_neutral,'neg':avg_negative, 'comp':avg_compound}
    result_vader = result_vader.append(new_row, ignore_index=True)
    result_vader.to_csv("result_vader_" + x + ".csv", index=False)

    # save the original values as well
    df.to_csv(date + "_vader_raw_" + x + ".csv", index=False)
