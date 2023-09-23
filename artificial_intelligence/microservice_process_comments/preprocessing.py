# Local libraries
import re

# External libraries
import hunspell
import spacy
import stanza
import emoji
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

class Preprocessing:

  # delete tags
  # delete emojis
  # delete useless information
  # stop words
  # stemming

  def __init__(self):
    """
      1. Download the Spanish or English model for Stanforn NLP
      2. Load the model
      3. Load the dictionary
      4. Load the model for Spacy
      # Load empty words
    """
    stanza.download('es', package='ancora',
                             processors='tokenize,mwt,pos,lemma', verbose=True)
    self.stNLP = stanza.Pipeline(
      processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)
    # global environment variables
    self.dic = hunspell.HunSpell(
            "./Diccionario/es_ANY.dic", "./Diccionario/es_ANY.aff")
    self.sp = spacy.load('es_core_news_md')
    self.all_stopwords = self.sp.Defaults.stop_words

  def process_comment(self, comment):
    """    
    Take a string, remove emojis, remove useless data, normalize, lemmatize,
    remove empty words and remove duplicates.
    :param comment: The comment to process
    :return: The processed comment.
    """
    try:
      comment = self.delete_tags(comment)
      comment = self.delete_emojis(comment)
      comment = self.delete_useless_data(comment)
      comment = self.fix_ortography(comment)
      comment = self.normalize_text(comment)
      comment = comment.split(" ")
      comment = self.lemma_words(comment)
      comment = " ".join(comment)
      comment = self.delete_stop_words(comment)
      comment = self.delete_duplicates(comment)
      return comment
    except Exception as e:
      print(e)
      return ""
    
  def delete_tags(self, text):
    """
    Take a string, split it into a list of words and then join the list back into a string,
    but only if the word does not start with @ or #

    :param text: The text to clean
    :return: The text without the tags.
    """
    text = text.split(" ")
    text_tagless = []
    for word in text:
      if not (word.startswith("@") or word.startswith("#")):
        text_tagless.append(word)
    text = " ".join(text_tagless)
    return text

  def delete_emojis(self, text):
    """
    Take a string and remove the emojis

    :param text: str
    :type text: str
    :return: A string without emojis.
    """
    return emoji.replace_emoji(text, "")

  def delete_useless_data(self, text):
    """ 
    This function cleans the text by removing web pages, punctuation, numbers, and multiple white spaces.
    In the order in which the text is cleaned is not arbitrary.
    The list of punctuation marks has been obtained from: print(string.punctuation)
    and re.escape(string.punctuation)
    """
    # Eliminación de páginas web (palabras que empiezan por "http")
    new_text = re.sub('http\S+', ' ', text)
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~\\¿\\¡\\”]'
    new_text = re.sub(regex, ' ', new_text)
    # Eliminación de números
    new_text = re.sub("\d+", ' ', new_text)
    # Eliminación de espacios en blanco múltiples
    new_text = re.sub("\\s+", ' ', new_text)
    # Tokenización por palabras individuales
    new_text = new_text.split(sep=' ')
    return " ".join(new_text)


  def delete_stop_words(self, text):
    """
    Take a string, tokenize it and then remove all the stop words

    :param text: The text to process
    :return: A list of words that are not stop words.
    """

    text_tokens = word_tokenize(text)
    tokens_without_sw = [
      word for word in text_tokens if not word in self.all_stopwords]
    return tokens_without_sw

  def lemmatize_words(self, words):
    """
    1. Take a list of words as input.
    2. Then iterate over each word in the list.
    3. For each word, call the stNLP function, which returns a list of lemmas.
    4. Then add the first lemma from the list to a new list.
    5. Return the new list.

    :param words: The list of words to lemmatize
    :return: A list of lemmas
    """

    new_words = []
    for word in words:
      result = self.stNLP(word)
      new_words.append(
          [word.lemma for sent in result.sentences for word in sent.words][0])
    return new_words

  def fix_ortography(self, text):    
    """
    Take a string and correct the word if it is necessary

    :param text: The text to correct
    :return: A string with the text corrected.
    """

    words = text.split(" ")
    result = ""
    for word in words:
      res = self.dic.spell(word)
      if not res:
        try:
          res = self.dic.suggest(word)[0]
        except Exception:
          res = word
      else:
        res = word
      result += res + " "
    result = result.strip()
    return result

  def normalize_text(self, text):
    """
    1. Take a string as input.
    2. Then transform the string to lowercase.
    3. Replace the letters with accents with normal letters.

    :param text: The text to convert
    :return: The converted text
    """

    new_text = text.lower()

    new_text = re.sub('á', 'a', new_text)
    new_text = re.sub('é', 'e', new_text)
    new_text = re.sub('í', 'i', new_text)
    new_text = re.sub('ó', 'o', new_text)
    new_text = re.sub('ú', 'u', new_text)
    new_text = re.sub('ü', 'u', new_text)
    new_text = re.sub('ñ', 'n', new_text)

    return new_text

  def delete_duplicates(self, words_list):
    """
    Take a list as argument and return a list with all the duplicates removed

    :param words_list: The list of strings
    :return: A list of unique elements from the list.
    """

    return list(set(words_list))
