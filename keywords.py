from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk import pos_tag
import nltk
nltk.download('averaged_perceptron_tagger_eng')
english_words = set(words.words())
stop_words = set(stopwords.words('english'))


def extract_keyword(text):
    word_list = word_tokenize(text)
    tagged_words = pos_tag(word_list)
    keywords = [word for word, tag in tagged_words if tag in ('NN', 'JJ')]
    return keywords








