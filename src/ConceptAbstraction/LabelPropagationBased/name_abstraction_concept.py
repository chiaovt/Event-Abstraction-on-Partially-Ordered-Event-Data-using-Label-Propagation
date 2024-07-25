from nltk.corpus import wordnet
import nltk
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string



def get_synonyms(word):
    nltk.download('wordnet')
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


def name_title(words):
    # Preprocess the words
    preprocessed_words = preprocess_string(' '.join(words))

    # Create a dictionary from the preprocessed words
    dictionary = Dictionary([preprocessed_words])

    # Convert the words to a bag-of-words representation
    bow_corpus = [dictionary.doc2bow(preprocessed_words)]

    # Train LDA model
    lda_model = LdaModel(bow_corpus, num_topics=1, id2word=dictionary, passes=10)

    # Get the most representative topic
    topic = lda_model.print_topics()[0][1]
    print('topic', topic)

    # Construct title based on the topic
    title = '--'.join([word for word, _ in lda_model.show_topic(0, topn=len(words)) if word not in words])

    return title

