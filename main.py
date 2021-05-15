import tweepy
import string
import re
from datetime import datetime
from nltk.corpus import stopwords
now = datetime.now()

# Import stopwords from NLTK.
stop_words = set(stopwords.words('english'))

nations = ["china", "korea", "Japan"]

for x in nations:
    keyword = x
    number = 3000 #Number of Tweets to be crawled
    dsince = now.strftime("%Y/%m/%d") # Tweet Date
    duntil = '2022-05-30' # Tweet Date
    location = "%s,%s,%s" % ("37.09024", "-95.712891", "2000mi") # Roughly covers the USA

    # Twitter Login Info. DO NOT SHARE.
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # English Stopword needs to be Deleted; i.e., “the”, “is” and “and”,
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    date = date.replace("/", '_')

    """
    Clear the text data by
    1. Removing Emoji
    2. Removing URLs
    3. Removing @ (Mention) or # (Hashtag)
    4. Removing RT
    5. Removing Stopwords
    6. Tokenizing the sentences
    """
    
    # Remove Emoji; might or might not delete all emoji.
    # Please see https://unicode.org/emoji/charts/full-emoji-list.html to see the full list of emoji.
    def emoji(text):
        emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\U00002500-\U00002BEF"
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001FA9F"
                                   u"\U0001F190-\U0001F1FF"
                                   u"\U00010000-\U0010ffff"
                                   u"\U0001F600-\U0001F92F"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23F0"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"
                                   u"\u3030"
                                   "]+", re.UNICODE)
        return emoji_pattern.sub(r'', text)

    # Remove URL
    def strip_links(text):
        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')
        return text

    # Remove '@' and '#'
    def strip_all_entities(text):
        entity_prefixes = ['@', '#']
        for separator in string.punctuation:
            if separator not in entity_prefixes:
                text = text.replace(separator, ' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)

    # Remove 'RT'
    def removeRT(text):
        modified = lambda x: re.compile('\#').sub('', re.compile('rt @').sub('@', x, count=1).strip())
        return modified(text)

    # Remove stopwords
    def stopwords(text):
        return " ".join([word for word in str(text).split() if word not in stop_words])

    # File name = date_nations_twitter.csv
    wfile = open(date + "_" + keyword + "_twitter.csv", mode='w', encoding='utf8')

    # Cursor Setting
    cursor = tweepy.Cursor(api.search,
                           q=keyword,
                           since=dsince,
                           until=duntil,
                           tweet_mode='extended',
                           count=number,
                           lang='en',
                           geocode=location,
                           include_entities=True)

    for i, tweet in enumerate(cursor.items(3000)):
        if i == 0:
            wfile.write("{},{},{},{},{}".format('no',
                                                'time',
                                                'favorite_count',
                                                'tweet_retweet_count',
                                                'tweet_text' +
                                                '\n')
                        )
        try:
            wfile.write("{},{},{},{},{}".format(i,
                                                tweet.created_at,
                                                tweet.favorite_count,
                                                tweet.retweet_count,
                                                (emoji
                                                 (stopwords
                                                  (strip_all_entities
                                                   (strip_links
                                                    (removeRT
                                                     (tweet.retweeted_status.full_text.lower().replace
                                                      ('\n', ''
                                                       )
                                                      )
                                                     )
                                                    )
                                                   )
                                                  )
                                                 )
                                                ) + '\n'
                        )
        except:
            pass

    wfile.close()

