

def lexical_diversity(tokens):
    return 1.0 * len(set(tokens))/len(tokens)

def avarage_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0 * total_words/len(statuses)