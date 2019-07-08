import oauth2 as oauth
import pandas as pd
import datetime
import json
import cgi
import re
import os
import tweepy
import twitter
import pandas as pd
import operator

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from analysisApp.models import Profile
from tweepy import OAuthHandler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from itertools import islice
from collections import Counter

# from .tasks import get_followers_n
# Create your views here.
languages = [
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('bm', 'Bambara'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bo', 'Tibetan'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan; Valencian'),
    ('cs', 'Czech'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('nl', 'Dutch; Flemish'),
    ('dz', 'Dzongkha'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ff', 'Fulah'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gv', 'Manx'),
    ('el', 'Greek, Modern (1453-)'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('ig', 'Igbo'),
    ('is', 'Icelandic'),
    ('io', 'Ido'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('iu', 'Inuktitut'),
    ('ie', 'Interlingue; Occidental'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ik', 'Inupiaq'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kn', 'Kannada'),
    ('ks', 'Kashmiri'),
    ('ka', 'Georgian'),
    ('kr', 'Kanuri'),
    ('kk', 'Kazakh'),
    ('km', 'Central Khmer'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lu', 'Luba-Katanga'),
    ('lg', 'Ganda'),
    ('mk', 'Macedonian'),
    ('mh', 'Marshallese'),
    ('ml', 'Malayalam'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('Mi', 'Micmac'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('mi', 'Maori'),
    ('ms', 'Malay'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ng', 'Ndonga'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('or', 'Oriya'),
    ('om', 'Oromo'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('rn', 'Rundi'),
    ('ru', 'Russian'),
    ('sg', 'Sango'),
    ('sa', 'Sanskrit'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('so', 'Somali'),
    ('st', 'Sotho, Southern'),
    ('es', 'Spanish; Castilian'),
    ('sq', 'Albanian'),
    ('sc', 'Sardinian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ty', 'Tahitian'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('ti', 'Tigrinya'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('tw', 'Twi'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu'),
    ('und', 'Undefined')
]

def take(n,iterable):
    return list(islice(iterable,n))

consumer = oauth.Consumer(settings.TWITTER_TOKEN,settings.TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'

authenticate_url = 'https://api.twitter.com/oauth/authenticate'

def f(x):
    return x.decode('UTF-8')

def twitter_login(request):
    resp, content = client.request(request_token_url,"GET")
    content = content.decode('UTF-8')
    if resp['status'] != '200':
        print(resp['status'])
        raise Exception("Invalid response from Twitter")

    request.session['oauth_token'] = re.findall('oauth_token=(.*?)&oauth_token',content)[0]
    request.session['oauth_token_secret'] = re.findall('oauth_token_secret=(.*?)&oauth',content)[0]
    url = authenticate_url+"?oauth_token="+request.session['oauth_token']
    return HttpResponseRedirect(url)

@login_required
def twitter_logout(request):
    logout(request)
    for key in request.session.keys():
        del request.session[key]
        print(key)
    return redirect('/')

def twitter_authenticated(request):
    token = oauth.Token(request.session['oauth_token'], request.session['oauth_token_secret'])
    token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer,token)

    resp, content = client.request(access_token_url,"GET")
    content = content.decode('UTF-8')
    print(content)
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter")

    screen_name = re.findall('&screen_name=(.*?)$',content)[0]
    oauth_token = re.findall('oauth_token=(.*?)&',content)[0]
    oauth_token_secret = re.findall('&oauth_token_secret=(.*?)&',content)[0]
    try:
        user = User.objects.get(username=screen_name)
    except User.DoesNotExist:
        user = User.objects.create_user(screen_name,'%s@twitter.com' % screen_name,oauth_token_secret)
        profile = Profile()
        profile.user = user
        profile.screen_name = screen_name
        profile.oauth_token = oauth_token
        profile.oauth_secret = oauth_token_secret
        profile.save()

    user = authenticate(username=screen_name,password=oauth_token_secret)
    login(request,user)
    return HttpResponseRedirect("/")

def process_or_store(tweet,screen_name):
    with open("{}.json".format(screen_name),"a+") as f:
        f.write(json.dumps(tweet))

@login_required
def home(request):
    username = request.user.username
    x = Profile.objects.get(pk=username)
    oauth_secret = x.oauth_secret
    oauth_token = x.oauth_token
    clean_url = lambda x: re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',x)
    clean_mentions = lambda x: re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)','',x)
    api = twitter.Api(consumer_key=settings.TWITTER_TOKEN,
                      consumer_secret=settings.TWITTER_SECRET,
                      access_token_key=oauth_token,
                      access_token_secret=oauth_secret)
    api.VerifyCredentials()
    user = api.GetUser(screen_name=username)
    followers_count = user.followers_count
    t = api.GetUserTimeline(screen_name=username,count=200)
    tweets = [i.AsDict() for i in t]
    df = pd.DataFrame(columns=('tweet_id','tweet_text','hashtags','source',
                               'mentions','lang'))
    pd_dict = {}
    tweet_text = []
    tweet_id = []
    for t in tweets:
        z = t['hashtags']
        if z == []:
            pd_dict['hashtags'] =  ""
        else:
            temp = list()
            for i in z:
                temp.append(i['text'])
            pd_dict['hashtags'] = temp
        pd_dict['source'] = re.findall('rel\=\"nofollow\"\>(.*?)\<\/a\>',t['source'])[0]
        y = t['user_mentions']
        if y:
            for i in y:
                pd_dict['mentions'] = i['screen_name']
        else:
            pd_dict['mentions'] = "NaN"
        pd_dict['lang'] = t['lang']
        pd_dict['tweet_id'] = t['id']
        pd_dict['tweet_text'] = t['text']
        df = df.append(pd_dict,ignore_index=True)
        #df.to_csv("test.csv",sep="|")
        tweet_text.append(t['text'])
        tweet_id.append(t['id'])
        if t['lang'] == 'en' or t['lang'] == 'und':
            with open("tweets.txt","a+") as f:
                f.write(t['text']+"\n")
    mentions = api.GetMentions(count=200)
    mentions = [i.AsDict() for i in mentions]
    mention_text = []
    for t in mentions:
        mention_text.append(t['text'])
    mention_text = [clean_url(item) for item in mention_text]
    mention_text = [clean_mentions(item) for item in mention_text]
    sid = SentimentIntensityAnalyzer()
    positive_mentions = negative_mentions = neutral_mentions = 0
    for item in mention_text:
        ss = sid.polarity_scores(item)
        if ss['pos'] > ss['neg']:
            positive_mentions = positive_mentions + 1
        if ss['neg'] > ss['pos']:
            negative_mentions = negative_mentions + 1
    neutral_mentions = len(mention_text) - (positive_mentions+negative_mentions)

    tweet_text = [clean_url(item) for item in tweet_text]
    tweet_text = [clean_mentions(item) for item in tweet_text]
    positive_tweets = []
    negative_tweets = []
    positive = negative = 0
    for item in tweet_text:
        ss = sid.polarity_scores(item)
        if ss['pos'] > ss['neg']:
            positive = positive + 1
            positive_tweets.append(item)
        if ss['neg'] > ss['pos']:
            negative = negative + 1
            negative_tweets.append(item)
    senti_tweets = positive_tweets + negative_tweets
    neutral_tweets = list(set(tweet_text) - set(senti_tweets))
    neutral = len(neutral_tweets)
    global languages
    languages = dict(languages)
    lang = list(df['lang'])
    lang_map = {k:v for k,v in languages.items()}
    lang = [lang_map.get(item,item) for item in lang]
    lang_dict = dict(Counter(lang))
    lang_dict = dict(sorted(lang_dict.items(), key=operator.itemgetter(1),reverse=True))
    lang_dict = take(3,lang_dict.items())

    tweet_text_dict = list(df['tweet_text'])
    tweet_text_dict = [clean_url(x) for x in tweet_text_dict]
    tweet_text_dict = [clean_mentions(x) for x in tweet_text_dict]
    stop_words = set(stopwords.words('english'))
    c = dict(Counter(i.lower() for x in tweet_text_dict for i in x.split()))
    cleaned_tweet_text = {}
    for key, value in c.items():
        word_token = word_tokenize(key)[0]
        if key.startswith('#') and len(key) > 3:
            cleaned_tweet_text[key] = value
        elif re.findall('^[a-zA-Z]+',key) and word_token not in stop_words and len(key) > 3:
            cleaned_tweet_text[key] = value

    cleaned_tweet_text = dict(sorted(cleaned_tweet_text.items(),key=operator.itemgetter(1),reverse=True))
    cleaned_tweet_text = take(3,cleaned_tweet_text.items())

    df['hashtags'] = df['hashtags'].map(lambda x: re.sub('\[\'','',str(x)))
    df['hashtags'] = df['hashtags'].map(lambda x: re.sub('\'\, \'',',',str(x)))
    df['hashtags'] = df['hashtags'].map(lambda x: re.sub('\'\]','',str(x)))

    hashtags = list(df['hashtags'][df.hashtags != 'nan'])

    hashtags = [x for xs in hashtags for x in xs.split(',')]
    cleaned_hashtags = dict(Counter(i for x in hashtags for i in x.split()))
    cleaned_hashtags = dict(sorted(cleaned_hashtags.items(), key=operator.itemgetter(1),reverse=True))
    cleaned_hashtags = take(3,cleaned_hashtags.items())
    # followers = api.GetFollowers()
    # followers = [i.AsDict() for i in followers]
    # for i in followers:
    #     print(i['screen_name'])
    #     user = api.GetUser(screen_name=i['screen_name'])
    #     print(user.followers_count)
    return render(request,'analysisApp/home.html',{'username':username,
                                                   'dashboard':'active',
                                                   'followers_count':followers_count,
                                                   'positive':positive,
                                                   'negative':negative,
                                                   'neutral':neutral,
                                                   'positive_mentions':positive_mentions,
                                                   'negative_mentions':negative_mentions,
                                                   'neutral_mentions':neutral_mentions,
                                                   'lang_dict':lang_dict,
                                                   'cleaned_tweet_text':cleaned_tweet_text,
                                                   'cleaned_hashtags':cleaned_hashtags
                                                   })

def index(request):
    if request.user.is_authenticated:
        print("Authenticated")
        return redirect('/home')
    else:
        print("Not Authenticated")
        return render(request,"analysisApp/index.html")

def privacy_policy(request):
    return render(request,'analysisApp/privacy_policy.html')

def terms_and_conditions(request):
    return render(request,'analysisApp/terms.html')
