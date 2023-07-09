import unicodedata

def delete_verified(text):
  # This function deletes the verified text from the username
  newText = text.split('\n')
  if(len(newText) > 1):
    newText.pop()
  return newText[0]

def text_to_unicode(text):
  # This function converts the text to unicode
  return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
