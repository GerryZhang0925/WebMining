#!/usr/bin/env python3

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from wordcloud import WordCloud
from PIL import Image


def load_ranking():

    # curl -H "Accept: application/vnd.github.mercy-preview+json" "https://api.github.com/search/repositories?q=stars:%3E1&s=stars&type=Repositories"

    headers = {
        "Accept": "Accept: application/vnd.github.mercy-preview+json",
    }

    url = "https://api.github.com/search/repositories?q=stars:%3E1&s=stars&type=Repositories"

    response = requests.get(url)

    return response


def save_json(filename, json_data):
    with open(filename, "w", encoding="utf­8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_json(filename):
    with open(filename, "r", encoding="utf­8") as f:
        return json.load(f)


def plot_ranking(json_data):
    repo_name = []
    # lang_name = []
    stargazers = []
    for info in json_data:
        repo = str(info.get("language", "-")) + "/" + str(info["name"])
        repo_name.append(repo)
        # lang_name.append(info.get('language', 0))
        stargazers.append(info["stargazers_count"])

    ranking = pd.Series(index=repo_name, data=stargazers)
    ranking = ranking.sort_values(ascending=False).head(20)
    print(ranking)
    ranking.plot.barh()
    plt.gca().invert_yaxis()
    plt.title("githubスター数")
    plt.grid()
    plt.show()


def visualize_worldcloud(json_data):
    filename = "tmp.txt"

    with open(filename, "w") as f:
        for info in json_data:
            f.write(str(info.get("language", "unknown")))
            f.write("\n")

    with open(filename, encoding="utf8") as f:
        text = f.read()
        wordcloud = WordCloud(max_font_size=40).generate(text)
        wordcloud.to_file("result.png")
        im = Image.open("result.png")
        im.show()


if __name__ == "__main__":
    filename = "github.json"
    data = load_ranking().json()
    save_json(filename, data)

    result = load_json(filename)
    print(json.dumps(result, indent=1, ensure_ascii=False))
    plot_ranking(result["items"])
    visualize_worldcloud(result["items"])
