import unicodedata


def delete_verified(text):
    # This function deletes the verified text from the username
    new_text = text.split('\n')
    if (len(new_text) > 1):
        new_text.pop()
    return new_text[0]


def text_to_unicode(text):
    # This function converts the text to unicode
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
