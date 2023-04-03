import unicodedata

def deleteVerified(text):
  newText = text.split('\n')
  if(len(newText) > 1):
    newText.pop()
  
  return newText[0]

def text_to_unicode(text):
  return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
