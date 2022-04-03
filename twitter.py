import tweepy
import json


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("H43NnEVDF28PPoBetXxzFcEJd", "Qe8NKqtF9zMtCS8HU4C1UjtYCeCTBExE2rWQyznBOe641d8xBb")
        self.auth.set_access_token("373839213-FZs4kUvi1kyjPPkAanhKBBv0KiaP7SeKgRH4CrVZ", "UFILHVcRYgpQkCl3VtZbDTJmK1AupUv5s4IOMfXOlFOj4")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def sample_call(self):
        vaccine_text_query_en = "vaccine -filter:retweets AND -filter:replies"
        vaccineTweetList = list()
        enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query_en, lang='en', tweet_mode="extended").items(1)
        for tweet in enTweets:
            vaccineTweetList.append(tweet._json)

        return vaccineTweetList

    def _meet_basic_tweet_requirements(self):
        covid_keywords_en = 'covid19 hospital testing covidappropriatebehaviour healthcare transmission socialdistance travelban immunity deltavariant epidemic socialdistancing quarantine workfromhome'.replace(" "," OR ")
        print(len(covid_keywords_en.split('OR')))
        #vaccine_keywords_en = ' antibodies getvaccinatedfullyvaccinated vaccination vaccinemandate firstdose covidvaccine vaccinated vaccinessavelives'.replace(" "," OR ")

        #covid_keywords_hi = 'वैश्विकमहामारी "सुरक्षित रहें" मास्क "कोविड मृत्यु" संगरोध "स्वयं संगरोध" डेल्टा संस्करण "दूसरी लहर" मुखौटा अस्पताल कोविड19 सैनिटाइज़र वायरस संक्रमण "सामाजिक दूरी" प्रक्षालक कोरोना कोविड-19 "कोविड 19" वाइरस वेंटिलेटर डेल्टा "कोविड महामारी" मौत फ़्लू प्रकोप संक्रमित कोरोनावाइरस "मास्क पहनें" ऑक्सीजन लॉकडाउन'.replace(" "," OR ")

        #vaccine_keywords_hi = 'टीकाकरण एंटीबॉडी कोविशील्ड टीके वैक्सीनेशन "वैक्सीन पासपोर्ट" "दूसरी खुराक" "टीकाकरण अभियान" "पहली खुराक" "पूर्ण टीकाकरण" कोवेक्सिन फाइजर लसीकरण'.replace(" "," OR ")

        #covid_keywords_es = 'quarentena cierredeemergencia autoaislamiento sintomas casos asintomático encierro "pandemia de covid-19" oxígeno desinfectante ventilador "quedate en casa" "trabajar desde casa" "cilindro de oxígeno" yomequedoencasa "distancia social" susanadistancia quedateencasa "distanciamiento social" transmisión distanciamientosocial variante lavadodemanos fiebre enfermedad "propagación en la comunidad" aislamiento distanciasocial'. replace(" "," OR ")

        #vaccine_keywords_es = 'anticuerpos "eficacia de la vacuna" "vacuna covid" "dosis de vacuna" "campaña de vacunación" vacunar "efectos secundarios de la vacuna" "inyección de refuerzo" vacunacovid19 inmunización yomevacunoseguro yomevacunoseguro ivermectin cansino vacunas "efectos secundarios" "la inmunidad de grupo" vacuna "vacuna para el covid-19" vacunada'.replace(" ", " OR ")

        #covid_text_query_en = covid_keywords_en + " -filter:retweets"

        #enTweets = tweepy.Cursor(self.api.search, q=covid_text_query_en, lang='en').items()
        #covidTweetsList = list()
        vaccineTweetList = list()
        #keywords_split_en = vaccine_keywords_en.split(' OR ')
        #for word in keywords_split_en:
            #vaccine_text_query_en = word + " -filter:retweets AND -filter:replies"
            #enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query_en, count=100, lang='en', tweet_mode="extended").items(
                #2)
            #for tweet in enTweets:
                #vaccineTweetList.append(tweet._json)
        #enListC = list()
        #for tweet in enTweets:
            #covidTweetsList.append(tweet.id_str)
            #enListC.append(tweet.text)
            #print(str(tweet.text) + " -> " + str(tweet.created_at))


        #print('Successfully Retrieved English Covid Keywords' + str(len(enListC)) + " Tweets !!!")

    def get_tweets_by_poi(self, poi_name):
        poiTweetList = list()
        pages = tweepy.Cursor(self.api.user_timeline, id=poi_name, count=190, exclude_replies=True,
                              include_rts=False, tweet_mode="extended").pages(30)
        for page in pages:
            for tweet in page:
                poiTweetList.append(tweet._json)

        return poiTweetList

    def get_tweets_by_poi_screen_name(self, poi_name):
        #user_statuses = self.api.user_timeline("JoeBiden", count=10, exclude_replies=False, include_rts=False)
        poiTweetList = list()
        poi_tweets = tweepy.Cursor(self.api.user_timeline, screen_name= poi_name, count=190, exclude_replies=True,
                                   include_rts=False, tweet_mode="extended").items(500)
        for tweet in poi_tweets:
            poiTweetList.append(tweet._json)

        return poiTweetList
        #for status in user_statuses:
            #json_object = json.dumps(status._json, indent=4)
            #print(status.text + '\n')

    def get_tweets_by_lang_and_keyword(self, vaccine_text_query, query_lang):
        vaccine_keywords_en = 'covid,vaccine'.replace(",", " OR ")
        print(len(vaccine_keywords_en.split(' OR ')))

        vaccineTweetList = list()
        enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query, lang=query_lang, tweet_mode="extended").items(
            1000)
        #esListV = list()
        #hiListV = list()
        for tweet in enTweets:
                vaccineTweetList.append(tweet._json)

        return vaccineTweetList

    def get_replies(self, conversation_id):
        # conversationId = ' OR '.join([conversation for conversation in conversation_ids])
        text_query = f"conversation_id:{conversation_id} filter:replies"
        lang = 'en OR hi'

        repliesTweets = tweepy.Cursor(self.api.search, q=text_query, lang=lang, count=190, tweet_mode="extended").pages(10)
        tweetRepliesList = list()
        for page in repliesTweets:
            for tweet in page:
                tweetRepliesList.append(tweet._json)

        return tweetRepliesList

