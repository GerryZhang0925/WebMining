#!/usr/bin/env python3

import json
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import unicodedata

# API Information
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

categories = dict()
categories["1"] = "Film & Animation"
categories["2"] = "Autos & Vehicles"
categories["10"] = "Music"
categories["15"] = "Pets & Animals"
categories["17"] = "Sports"
categories["18"] = "Short Movies"
categories["19"] = "Travel & Events"
categories["20"] = "Gaming"
categories["21"] = "Videoblogging"
categories["22"] = "People & Blogs"
categories["23"] = "Comedy"
categories["24"] = "Entertainment"
categories["25"] = "News & Politics"
categories["26"] = "Howto & Style"
categories["27"] = "Education"
categories["28"] = "Science & Technology"
categories["30"] = "Movies"
categories["31"] = "Anime/Animation"
categories["32"] = "Action/Adventure"
categories["33"] = "Classics"
categories["34"] = "Comedy"
categories["35"] = "Documentary"
categories["36"] = "Drama"
categories["37"] = "Family"
categories["38"] = "Foreign"
categories["39"] = "Horror"
categories["40"] = "Sci-Fi/Fantasy"
categories["41"] = "Thriller"
categories["42"] = "Shorts"
categories["43"] = "Shows"
categories["44"] = "Trailers"

categories_jp = dict()
categories_jp["1"] = "映画"
categories_jp["2"] = "車"
categories_jp["10"] = "音楽"
categories_jp["15"] = "動物"
categories_jp["17"] = "スポーツ"
categories_jp["18"] = "Short Movies"
categories_jp["19"] = "旅行"
categories_jp["20"] = "ゲーム"
categories_jp["21"] = "VLOG"
categories_jp["22"] = "人物"
categories_jp["23"] = "コメディ"
categories_jp["24"] = "エンター"
categories_jp["25"] = "ニュース"
categories_jp["26"] = "ハウツー"
categories_jp["27"] = "教育"
categories_jp["28"] = "科学技術"
categories_jp["30"] = "ムービー"
categories_jp["31"] = "アニメ"
categories_jp["32"] = "冒険"
categories_jp["33"] = "クラシック"
categories_jp["34"] = "Comedy"
categories_jp["35"] = "ドキュメンタリー"
categories_jp["36"] = "ドラマ"
categories_jp["37"] = "ファミリ"
categories_jp["38"] = "外国"
categories_jp["39"] = "ホラー"
categories_jp["40"] = "SF"
categories_jp["41"] = "スリラー"
categories_jp["42"] = "Shorts"
categories_jp["43"] = "ショー"
categories_jp["44"] = "予告"

categories_color = dict()
categories_color["1"] = matplotlib.colors.cnames["salmon"]  # 映画
categories_color["2"] = matplotlib.colors.cnames["tomato"]  # 車
categories_color["10"] = matplotlib.colors.cnames["red"]  # 音楽
categories_color["15"] = matplotlib.colors.cnames["greenyellow"]  # 動物
categories_color["17"] = matplotlib.colors.cnames["orangered"]  # スポーツ
categories_color["18"] = matplotlib.colors.cnames["mistyrose"]  # Short Movies
categories_color["19"] = matplotlib.colors.cnames["chartreuse"]  # 旅行
categories_color["20"] = matplotlib.colors.cnames["coral"]  # ゲーム
categories_color["21"] = matplotlib.colors.cnames["lightcoral"]  # VLOG
categories_color["22"] = matplotlib.colors.cnames["wheat"]  # 人物
categories_color["23"] = matplotlib.colors.cnames["rosybrown"]  # コメディ
categories_color["24"] = matplotlib.colors.cnames["peru"]  # エンター
categories_color["25"] = matplotlib.colors.cnames["blanchedalmond"]  # ニュース
categories_color["26"] = matplotlib.colors.cnames["orange"]  # ハウツー
categories_color["27"] = matplotlib.colors.cnames["lemonchiffon"]  # 教育
categories_color["28"] = matplotlib.colors.cnames["gold"]  # 科学技術
categories_color["30"] = matplotlib.colors.cnames["lightsalmon"]  # ムービー
categories_color["31"] = matplotlib.colors.cnames["peachpuff"]  # アニメ
categories_color["32"] = matplotlib.colors.cnames["maroon"]  # 冒険
categories_color["33"] = matplotlib.colors.cnames["dodgerblue"]  # クラシック
categories_color["34"] = matplotlib.colors.cnames["rosybrown"]  # Comedy
categories_color["35"] = matplotlib.colors.cnames["lightskyblue"]  # ドキュメンタリー
categories_color["36"] = matplotlib.colors.cnames["deepskyblue"]  # ドラマ
categories_color["37"] = matplotlib.colors.cnames["turquoise"]  # ファミリ
categories_color["38"] = matplotlib.colors.cnames["lightgreen"]  # 外国
categories_color["39"] = matplotlib.colors.cnames["black"]  # ホラー
categories_color["40"] = matplotlib.colors.cnames["gainsboro"]  # SF
categories_color["41"] = matplotlib.colors.cnames["dimgray"]  # スリラー
categories_color["42"] = matplotlib.colors.cnames["lightgrey"]  # Shorts
categories_color["43"] = matplotlib.colors.cnames["lightgray"]  # ショー
categories_color["44"] = matplotlib.colors.cnames["whitesmoke"]  # 予告


def truncate(string, length, ellipsis="..."):
    """文字列を切り詰める

    string: 対象の文字列
    length: 切り詰め後の長さ
    ellipsis: 省略記号
    """
    return string[:length] + (ellipsis if string[length:] else "")


def get_youtube():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    return youtube


def get_channel_detail(youtube):

    """
    search_response = youtube.search().list(
                                       q='',
                      part='id,snippet',
    ).execute()

    print(search_response)
    """
    search_response = (
        youtube.channels()
        .list(part="snippet,contentDetails", id="UCMUnInmOkrWN4gof9KlhNmQ")
        .execute()
    )

    return search_response["items"][0]


def get_video_categories(youtube):
    search_response = (
        youtube.videoCategories().list(part="id,snippet", regionCode="JP").execute()
    )

    # return search_response['items'][0]
    return search_response["items"]


def get_video_list(youtube, upload_id):
    video_list = []
    request = youtube.playlistItems().list(
        part="snippet, contentDetails", playlistId=upload_id, maxResults=50
    )
    next_page = True

    while next_page:
        response = request.execute()
        data = response["items"]

        for video in data:
            video_id = video["contentDetails"]["videoId"]
            if video_id not in video_list:
                video_list.append(video_id)

        if "nextPageToken" in response.keys():
            next_page = True

            request = youtube.playlistItems().list(
                part="snippet, contentDetails",
                playlistId=upload_id,
                maxResults=50,
                pageToken=response["nextPageToken"],
            )
        else:
            next_page = False

    return video_list


def get_video_details(youtube, video_list):
    stats_list = []

    for i in range(0, len(video_list), 50):
        request = youtube.videos().list(
            part="snippet, contentDetails, statistics", id=video_list[i : i + 50]
        )
        data = request.execute()

        for video in data["items"]:
            title = video["snippet"]["title"]
            published = video["snippet"]["publishedAt"]
            description = video["snippet"]["description"]
            tag_count = len(video["snippet"].get("tags", []))
            view_count = video["statistics"].get("viewCount", 0)
            like_count = video["statistics"].get("likeCount", 0)
            dislike_count = video["statistics"].get("dislikeCount", 0)
            comment_count = video["statistics"].get("commentCount", 0)

            stats_dictionary = dict(
                title=title,
                published=published,
                description=description,
                tag_count=tag_count,
                view_count=view_count,
                like_count=like_count,
                dislike_count=dislike_count,
                comment_count=comment_count,
            )

            stats_list.append(stats_dictionary)

    return stats_list


def get_subscriptions(youtube):
    request = (
        youtube.subscriptions()
        .list(part="id, snippet, contentDetails", channelId="UCIzyCSfrZfVfYr0o6n1m5rA")
        .execute()
    )

    print(request)


def get_popular_videos(youtube, target_category_id=0):
    vid_list = []  # video id
    channel_list = []  # chnnel id
    title_list = []  # title of video
    view_list = []  # view count
    like_list = []  # like count
    comment_list = []  # comment cout
    category_list = []  # category id
    lan_list = []  # default language
    audio_lan_list = []  # audio language

    request = youtube.videos().list(
        # part='snippet, contentDetails, statistics, liveStreamingDetails, player, processingDetails, recordingDetails, status, suggestions, topicDetails',
        part="snippet, contentDetails, statistics",
        chart="mostPopular",
        regionCode="SG",
        videoCategoryId=target_category_id,
    )

    next_page = True

    while next_page:
        response = request.execute()
        data = response["items"]

        for video in data:
            vid = video["id"]
            if vid not in vid_list:
                vid_list.append(vid)
                title_list.append(video["snippet"]["title"])
                channel_list.append(video["snippet"]["channelId"])
                view_list.append(int(video["statistics"].get("viewCount", 0)))
                like_list.append(int(video["statistics"].get("likeCount", 0)))
                comment_list.append(int(video["statistics"].get("commentCount", 0)))
                category_list.append(video["snippet"]["categoryId"])
                lan_list.append(video["snippet"].get("defaultLanguage", "ja"))
                audio_lan_list.append(
                    video["snippet"].get("defaultAudioLanguage", "ja")
                )

        if "nextPageToken" in response.keys():
            next_page = True

            request = youtube.videos().list(
                part="snippet, contentDetails, statistics",
                chart="mostPopular",
                regionCode="SG",
                videoCategoryId=target_category_id,
                pageToken=response["nextPageToken"],
            )
        else:
            next_page = False

    df = pd.DataFrame(
        {
            "title": title_list,
            "channelId": channel_list,
            "viewCount": view_list,
            "likeCount": like_list,
            "commentCount": comment_list,
            "categoryId": category_list,
            "language": lan_list,
            "audioLanguage": audio_lan_list,
        },
        index=vid_list,
    )

    return df


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    return count


def plot_popular_videos_df(dataframe):

    df = dataframe.sort_values("viewCount", ascending=False).head(20)
    raw_title = df["title"].values
    category_id = df["categoryId"].values
    view_count = df["viewCount"].values

    title = []
    colorlist = []
    label_length = 14
    for i in range(len(category_id)):
        left_length = (
            label_length - get_east_asian_width_count(categories_jp[category_id[i]]) - 1
        )
        title.append(
            categories_jp[category_id[i]]
            + "/"
            + truncate(raw_title[i], left_length * 2)
        )
        colorlist.append(categories_color[category_id[i]])

    trends = pd.Series(index=title, data=view_count)
    trends.plot.barh(color=colorlist)
    plt.gca().invert_yaxis()
    # plt.gca().set_yticklabels(plt.gca().yaxis.get_majorticklabels(), ha="left")
    plt.title("youtube view count ranking (2021/12/27)")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    youtube = get_youtube()

    """
    # get video categories
    video_categories = get_video_categories(youtube)
    print(json.dumps(video_categories, indent=1, ensure_ascii=False))
    
    """

    df = get_popular_videos(youtube)
    plot_popular_videos_df(df)
