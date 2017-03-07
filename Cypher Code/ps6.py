import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        l=string.ascii_lowercase
        u=string.ascii_uppercase
        d={}
        for i in l:
          x=ord(i)+shift
          if (x>122):
            d[i]=chr(96+(x%122))
          else:
            d[i]=chr(x)
        for i in u:
          x=ord(i)+shift
          if (x>90):
            d[i]=chr(64+(x%90))
          else:    
            d[i]=chr(x)
        return d

    def apply_shift(self, shift):
        d=self.build_shift_dict(shift)
        l=list(self.message_text)
        for i in range(len(l)):
            if l[i] in d:
                l[i]=d[l[i]]
        return (''.join(l))
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self,text)
        self.shift=shift
        self.encrypting_dict=Message.build_shift_dict(self,shift)
        self.message_text_encrypted=Message.apply_shift(self,shift)

    def get_shift(self):
        return self.shift

    def get_encrypting_dict(self):
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        PlaintextMessage.__init__(self,Message.get_message_text(self),shift)
        #self.shift=shift
        #self.encrypting_dict=Message.build_shift_dict(self,shift)
        #self.message_text_encrypted=Message.apply_shift(self,shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self,text)
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_count=0
        best=0
        decrypted=''
        for i in range(0,27):
        	count=0
        	msg=Message.apply_shift(self,i).split(' ')
        	for word in msg:
        		if (is_word(self.valid_words,word)):
        			count+=1
        	if count>best_count:
        		best_count=count
        		best=i
        		decrypted=' '.join(msg)
        return (best,decrypted)


#Example test case (PlaintextMessage)
#plaintext = PlaintextMessage('Message to be cyphered', 13)
#print('Expected Output: --')
#('Actual Output:', plaintext.get_message_text_encrypted())
    
#Example test case (CiphertextMessage)
#ciphertext = CiphertextMessage('Enter your cypher text')
#print('Expected Output:', (24, 'hello'))
#print('Actual Output:', ciphertext.decrypt_message())

def decrypt_story():
    ciphertext = CiphertextMessage(get_story_string())
    return ciphertext.decrypt_message()

print(decrypt_story())