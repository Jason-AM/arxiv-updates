import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

from article_info_extraction import get_and_save_info

DATA_DIR = Path("./data")
date_from = "2022-06-16"
date_to = "2022-06-17"

filename = DATA_DIR / f"stat-ml_cs-LG_{date_from}-{date_to}.pkl"

if filename.is_file():
    print("loaded_data")
    with open(filename, "rb") as fp:
        titles_urls = pickle.load(fp)
else:
    titles_urls = get_and_save_info(date_from, date_to)


all_titles_list = [title for title, _ in titles_urls]

stop_words = text.ENGLISH_STOP_WORDS.union(
    [
        "deep",
        "machine",
        "learning",
        "neural",
        "network",
        "models",
        "model",
        "based",
        "networks",
        "data",
        "using",
    ]
)
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words)
X = vectorizer.fit_transform(all_titles_list)
words = vectorizer.get_feature_names_out()

scores = X.mean(axis=0)
scores = np.asarray(scores)[0]

word_freq_dict = dict(zip(words, scores))

# Generate a word cloud image
wordcloud = WordCloud().generate_from_frequencies(word_freq_dict)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate_from_frequencies(word_freq_dict)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
