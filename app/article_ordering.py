from itertools import combinations, filterfalse, tee


def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))


def get_word_combinations(list_of_words):
    """
    Gets a list of all possible combinations of search words for instance if:
    [deep, bayesian] -> [['bayesian', 'deep'], ['baysian'], ['deep']]
    Notice that it should be in alphabetical order and largest list first
    """
    word_combos = []
    for L in range(len(list_of_words) + 1, 0, -1):
        for subset in combinations(list_of_words, L):
            word_combos.append(sorted(subset))
    return word_combos


def sort_articles_by_key_words(list_of_titles_urls, list_of_key_words):
    list_of_key_words = [w.strip() for w in list_of_key_words]

    titles_to_bottom = list_of_titles_urls
    titles_to_top = []

    search_word_combinations = get_word_combinations(list_of_key_words)

    for words in search_word_combinations:

        def are_search_words_in_title(x):
            return all(word.lower() in x[0].lower() for word in words)

        titles_to_bottom, titles_to_top_p = partition(
            are_search_words_in_title, titles_to_bottom
        )

        titles_to_top.extend(titles_to_top_p)

    return titles_to_top + titles_to_bottom
