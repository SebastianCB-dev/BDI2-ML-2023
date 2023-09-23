from pprint import pprint
from gensim.models import Word2Vec
import numpy as np
import os
import json
from services.logging_service import LoggingService
import joblib

class ModelWord2Vec:
  modelES = None
   # Public Properties
  logger = LoggingService().get_logging()
  clf = None

  def __init__(self):
    """
    This function loads the Word2Vec model for depression.
    """
    self.set_model()  
    self.clf = joblib.load('./models/logistic_regression.pkl')  

  def set_model(self):    
    print(os.getcwd());    
    self.modelES = Word2Vec.load('model/depresion.es.model')
    self.logger.info("Model loaded")

  def get_beck(self):
    """
    Open the JSON file of the BECK items vectorized, read it and return the data from the JSON file in a Python dictionary
    :return: A dictionary of dictionaries.
    """
    beck_data_preprocessing = {}
    try:
        if open('./JSON/items_preprocessing.json', 'r'):
            beck_data_preprocessing = json.loads(
                open('./JSON/items_preprocessing.json', 'r', encoding='utf-8').read())
    except Exception as e:
      print(f'Error: {e}')
    return beck_data_preprocessing

  def get_model(self):
    """
    Return the Word Embedding.
    :return: Word2Vec model of depression.
    """

    return self.modelES
  
  def add_corpus(self, corpus):
    """
    The function takes a corpus as input, adds it to the existing model and saves the updated model.

    :param corpus: The corpus is a list of lists. Each list is a document. Each document is a list of words
    """

    corpus = [corpus]
    self.modelES.build_vocab(corpus, update=True)
    self.save_model()

  def save_model(self):
    """
    Take the model, and save it as a file called 'model/depresion.model'
    """

    self.modelES.save('model/depresion.es.model')

  def get_cosine_similarity(self, corpus_a, corpus_b):
    """
    The function takes two lists of words as input and returns the cosine similarity between the two lists

    :param corpus_a: a list of words
    :param corpus_b: The corpus to compare with
    :return: The cosine similarity between the two documents.
    """

    return self.modelES.wv.n_similarity(corpus_a, corpus_b)

  def get_word_vectors(self, corpus):
    """
    Return the word vectors for the words in the corpus.

    :param corpus: The corpus is the list of words for which you want to get the vectors
    :return: The word vectors for each word in the corpus.
    """

    array_result = []
    for word in corpus:
      try:
        array_result.append(self.modelES.wv[word])
      except Exception as e:
        return self.get_vector_250()
    return array_result

  def get_cosine_similarity_BECK(self, corpus):
    """
    This function takes a corpus and returns a list of cosine similarities between the corpus and each of the 90 results of the BECK Depression Inventory (BDI-II) inventory.

    :param corpus: The text you want to compare with the BECK corpus
    :return: A list of cosine similarities between the corpus and the BECK data.
    """

    self.add_corpus(corpus)
    beck = self.get_beck()
    data = []
    for item in beck.keys():
      for result in beck[item].keys():
        similarity = self.get_cosine_similarity(corpus, beck[item][result]["data"])
        data.append(similarity)
    return data    

  def get_result_beck(self, cosine_similarities):
    """
    Take the cosine similarities and return the results of the survey filled in a flat list.

    :param cosine_similarities: The cosine similarities between the query and the documents
    :return: The results are returned as a list of lists.
    """

    results = []
    primera_parte = cosine_similarities[:60]  # 4 respuestas
    segunda_parte = cosine_similarities[60:67]  # 7 respuestas
    tercera_parte = cosine_similarities[67:71]  # 4 respuestas
    cuarta_parte = cosine_similarities[71:78]  # 7 respuestas
    quinta_parte = cosine_similarities[78:]  # 4 respuestas
    results.append(self.get_max_beck_4_items(primera_parte))
    results.append(self.get_max_beck_7_items(segunda_parte))
    results.append(self.get_max_beck_4_items(tercera_parte))
    results.append(self.get_max_beck_7_items(cuarta_parte))
    results.append(self.get_max_beck_4_items(quinta_parte))
    results_flat = [x for sublist in results for x in sublist]
    return results_flat

  def get_max_beck_4_items(self, array):
    """
    Take a matrix of numbers and return a matrix of the index of the largest number in each group of 4

    :param array: The matrix of numbers to process
    :return: The index of the maximum value in each group of 4 elements.
    """

    results = []
    for index in range(0, len(array), 4):
      item = array[index: index + 4]
      mayor = 0
      mayor_idx = 0
      for index, result in enumerate(item):
        if result > mayor:
          mayor = result
          mayor_idx = index
      results.append(mayor_idx)
    return results

  def get_max_beck_7_items(self, array):
    """
    Take a matrix of numbers and return a matrix of the index of the largest number in each group of 7

    :param array: The matrix of numbers to process
    :return: The index of the maximum value in each group of 7 elements.
    """

    results_beck = [0, 1, 1, 2, 2, 3, 3]
    results = []
    for index in range(0, len(array), 7):
      item = array[index: index + 7]
      mayor = 0
      mayor_idx = 0
      for index, result in enumerate(item):
        if result > mayor:
          mayor = result
          mayor_idx = results_beck[index]
      results.append(mayor_idx)
    return results

  def get_vector_250(self):
    """
    Return a list of 250 zeros.
    :return: A list of 250 zeros.
    """
    return list(np.zeros(250))
  
  def get_predict(self, corpus):
    """
    Return the prediction of the model.

    :param corpus: The corpus to predict
    :return: The prediction of the model.
    """
    
    return self.clf.predict([corpus])
