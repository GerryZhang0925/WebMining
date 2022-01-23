#!/usr/bin/env python3

import time
import twitter
import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from urllib.parse import unquote
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from PIL import Image

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

countries_woe = dict()
countries_woe["world"] = 1
countries_woe["us"] = 23424977
countries_woe["jp"] = 23424856
countries_woe["ca"] = 23424775
countries_woe["kr"] = 23424868  # south korea
countries_woe["sg"] = 23424948
countries_woe["my"] = 23424901
countries_woe["gb"] = 23424975


def open_twitter():
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
    )
    twitter_api = twitter.Twitter(auth=auth)

    return twitter_api


def get_trends(twitter_api, woe_id):
    tweet_list = []
    trends = twitter_api.trends.place(_id=woe_id)
    data = trends[0]["trends"]
    for d in data:
        tweet_list.append(d)
    return tweet_list


def plot_trends(data):
    trend_name = []
    trend_volume = []
    for info in data:
        trend_name.append(info["name"])
        if info["tweet_volume"] == None:
            trend_volume.append(0)
        else:
            trend_volume.append(info["tweet_volume"])
    trends = pd.Series(index=trend_name, data=trend_volume)
    trends = trends.sort_values(ascending=False).head(20)
    trends.plot.barh()
    plt.gca().invert_yaxis()
    plt.title("tweet投稿数")
    plt.grid()
    plt.show()


def get_tweepy_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    tweepy_api = tweepy.API(auth)
    return tweepy_api


def get_timeline(tweepy_api, target_id, target_count, tweets_name):
    info = tweepy_api.user_timeline(id=target_id, count=target_count)
    cnt = 0
    with open(tweets_name, "w", encoding="utf-8") as f:
        for k in info:
            cnt += 1
            f.write(k.text)
            print("Processing tweet ", cnt)


def tokenizer(tweets_name, dicname):
    book = open(tweets_name, "rt", encoding="utf-8")
    text = book.read()
    book.close()

    tok = Tokenizer()

    word_dic = {}
    lines = text.split("\r\n")
    for line in lines:
        token_list = tok.tokenize(line)
        for w in token_list:
            word = w.surface
            ps = w.part_of_speech
            if ps.find("名詞") < 0:
                continue
            if not word in word_dic:
                word_dic[word] = 0
            word_dic[word] += 1

    keys = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)
    with open(dicname, "w", encoding="utf-8") as fp:
        for word, cnt in keys[:100]:
            fp.write(str("{0}\t{1}\n".format(word, cnt)))


def visualize_worldcloud(dicname, pngname):
    with open(dicname, encoding="utf8") as f:
        text = f.read()
        wordcloud = WordCloud(
            font_path="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            max_font_size=40,
        ).generate(text)
        wordcloud.to_file(pngname)
        im = Image.open(pngname)
        im.show()


if __name__ == "__main__":
    twitter_api = open_twitter()
    data = get_trends(twitter_api, countries_woe["jp"])
    print(json.dumps(data, indent=1, ensure_ascii=False))
    plot_trends(data)

    tweepy_api = get_tweepy_api()
    ids_to_get = ["hikakin"]

    ids_to_get = dict()
    ids_to_get["son_masayoshi"] = "masason"
    ids_to_get["horie_takafumi"] = "takapon_jp"
    ids_to_get["matsumoto_hitoshi"] = "matsu_bouzu"
    ids_to_get["abe_shinzou"] = "AbeShinzo"
    # ids_to_get['ariyoshi_hiroiki'] = 'ariyoshihiroiki'
    # ids_to_get['hirose_suzu'] = 'Suzu_Mg'
    # ids_to_get['hashimoto_kanna'] = 'H_KANNA_0203'
    for key in ids_to_get.keys():
        tweets_name = key + "_" + "tweets.txt"
        dicname = key + "_" + "result.txt"
        pngname = key + "_" + "result.png"
        get_timeline(tweepy_api, ids_to_get[key], 200, tweets_name)
        tokenizer(tweets_name, dicname)
        visualize_worldcloud(dicname, pngname)
