import numpy as np
import spacy
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

# from wordcloud import WordCloud


def get_important_words(titles_urls):

    all_titles_list = [title for title, _, _ in titles_urls]

    nlp = spacy.load("en_core_web_sm")
    docs = [nlp(title) for title in all_titles_list]

    noun_chunks = [
        chunk.text.lower().replace(" ", "_")
        for doc in docs
        for chunk in doc.noun_chunks
    ]

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
            "pre",
            "applications",
            "training",
            "context",
            "non",
        ]
    )
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words)
    X = vectorizer.fit_transform(noun_chunks)
    words = vectorizer.get_feature_names_out()

    scores = X.mean(axis=0)
    scores = np.asarray(scores)[0]

    word_freq_dict = dict(zip(words, scores))
    # word_freq_dict = WordCloud(stopwords=stop_words).process_text(" ".join(noun_chunks))

    sorted_word_freq_dict = [
        k.replace("_", " ")
        for k, v in sorted(word_freq_dict.items(), key=lambda item: item[1])
    ]

    return sorted_word_freq_dict[::-1][:30]
