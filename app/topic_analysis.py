import pickle
from pathlib import Path

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

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
features = list(vectorizer.get_feature_names_out())

dimension = 10
lda = LDA(n_components=dimension)
lda_array = lda.fit_transform(X)


components = [lda.components_[i] for i in range(len(lda.components_))]
important_words = [
    sorted(features, key=lambda x: components[j][features.index(x)], reverse=True)[:5]
    for j in range(len(components))
]
for topic in important_words:
    print(topic)
    print("")
