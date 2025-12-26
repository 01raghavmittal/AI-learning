def word_count(text):
    words = text.split()
    return len(words)

def unique_words(text):
    words = text.lower().split()
    return len(set(words))
