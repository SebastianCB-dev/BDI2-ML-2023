

def deleteVerified(text):
  newText = text.split('\n')
  if(len(newText) > 1):
    newText.pop()
  
  return newText[0]