from preprocessing_service import Preprocesamiento
from model_word2vec_service import ModelWord2Vec
import joblib

# Load models
pp = Preprocesamiento()
w2v = ModelWord2Vec()
clf = joblib.load('./models/logistic_regression.pkl')

while True:
  # Get 10 comments from database
  comments = ['Estoy super feliz, quiero salir a pasear', 'Estoy muy triste, no quiero salir de mi casa']
  for comment in comments:
    # TODO: Identify if the comment is in Spanish or English    
    # Preprocessing comment
    comment_processed = pp.preprocesamiento_con_ortografia(comment)
    if(comment_processed == ""):
      # TODO: Change status of comment to "REVIEWED"
      continue
    # TODO: Check if exists user in database
    print('Comment processed: ', comment_processed)
    cosine_similarity_beck = w2v.get_cosine_similarity_BECK(comment_processed)
    print('Cosine similarity BECK: ', cosine_similarity_beck)
    results_beck = w2v.get_result_beck(cosine_similarity_beck)
    print('Results BECK: ', results_beck)
