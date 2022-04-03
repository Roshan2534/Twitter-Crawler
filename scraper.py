import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor, preprocessing_hi
from indexer import Indexer
import time


reply_collection_knob = False
poi_collection = False
normal_tweets_collection = True

def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)
    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    indexer = Indexer()
    twitter = Twitter()

    if normal_tweets_collection:
        vaccine_keywords_hin = 'टीकाकरण,एंटीबॉडी,कोविशील्ड,टीके,वैक्सीनेशन,"वैक्सीन पासपोर्ट","दूसरी खुराक","टीकाकरण अभियान","पहली खुराक","पूर्ण टीकाकरण",कोवेक्सिन,फाइजर,लसीकरण,खुराक,"रोग प्रतिरोधक शक्ति",'.replace(","," OR ")
        keywords_split_hin = vaccine_keywords_hin.split(' OR ')

        for word in keywords_split_hin:
            print(f"Getting Tweets for: {word}...")
            vaccine_text_query_hin = word + " -filter:retweets AND -filter:replies"
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_lang_and_keyword(vaccine_text_query_hin, 'hi')
            print(f"--- Took %s seconds for {word} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {word}")

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

                # indexer.create_documents(processed_tweets)
            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"hi_keywords_{word}.pkl")
            print('Indexing and Saving Done for { ' + word + ' }')

        print("Hindi Words Done")
    if poi_collection:
        indian_pois = ['narendramodi', 'MoHFW_INDIA', 'RahulGandhi', 'myogiadityanath', 'smritiirani']

        us_pois = ['JoeBiden', 'BarackObama', 'CDCgov', 'BernieSanders', 'Mike_Pence']

        mexico_pois = ['lopezobrador_', 'RicardoAnayaC', 'SSalud_mx', 'JoseAMeadeK', 'JaimeRdzNL']

        for poi in indian_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"us_poi_{poi}.pkl',")
            print('Indexing and Saving Done for { ' + poi + ' }')
        print("Indian  POI Done")

        for poi in us_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"us_poi_{poi}.pkl',")
            print('Indexing and Saving Done for { ' + poi + ' }')
        print("USA POI Done")

        for poi in mexico_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            filtered_tweets = []
            vaccine_keywords_en_full_list = 'vaccine'
            for vaccine in vaccine_keywords_en_full_list:
                for tweet in raw_tweets:
                    if vaccine in tweet['full_text']:
                        filtered_tweets.append(tweet)

            print(f"Filtered Tweets: {len(filtered_tweets)}")

            fids = []
            for ftweet in filtered_tweets:
                fids.append(ftweet['id_str'])
            # print(','.join([fid for fid in fids]))
            save_file(fids, f"mexico_poi_covid_ids_{poi}.pkl")

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"us_poi_{poi}.pkl',")
            print('Indexing and Saving Done for { ' + poi + ' }')
        print("Mexico POI Done")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        enFiles = []

        tweets_received = []
        for file in enFiles:
            ids = read_file(file)['id']
            for _id in ids:
                print(f"Getting Tweets for: {file} with Conversation ID: {id} ...")
                start_time = time.time()
                raw_tweets = twitter.get_replies(_id)
                print(f"--- Took %s seconds for {file} ---" % (time.time() - start_time))
                print(f"Retrieved {len(raw_tweets)} for {file}")

                if len(raw_tweets) != 0:
                    processed_tweets = []
                    for tw in raw_tweets:
                        processed_tweets.append(TWPreprocessor.preprocess(tw, False))

                    indexer.create_documents(processed_tweets)
                    print('Indexing and Saving Done')

        print("Total Received: " + str(len(tweets_received)))





if __name__ == "__main__":
    main()
