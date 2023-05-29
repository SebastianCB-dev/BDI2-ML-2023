FROM ubuntu:22.04

# Install dependencies

# Install Python 3.9
RUN apt-get update && apt-get install -y python3.9

# Install pip
RUN apt-get install -y python3-pip

# Install app dependencies
RUN apt-get install libhunspell-dev -y

# Install packages
RUN pip install emoji nltk sklearn spacy stanza wheel hunspell numpy gensim pyemd joblib scikit-learn

# Install dictiionaries
RUN python3 -m spacy download es_core_news_md

# Set working directory
WORKDIR /app

# Infinite loop
CMD ["tail", "-f", "/dev/null"]