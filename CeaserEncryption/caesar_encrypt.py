def caesar_encrypt(key, message):
    """Encrypt a message"""
    encrypted_message = ''
    try:
        #check if length is greater than 0
        if len(message) < 0:
            print('Please enter a non-empty message')
        #check to make sure key is between 1 and 26
        elif 1 > int(key) or int(key) > 26:
            return 'Please enter a key value between 1 and 26 to shift the letters'
        else:
            for letter in message:
                #keep spaces as is
                if letter == ' ':
                    encrypted_message = encrypted_message + ' '
                #ignore any non alph-numeric characters i.e. punctuation
                elif not(letter.isalnum()):
                    encrypted_message = encrypted_message + letter
                elif letter.isupper():
                    #found this stackflow link which details how to cycle through unicode text using modular arithmetic 
                    #and only return letters https://stackoverflow.com/questions/64559066/limiting-ord-to-letters-only
                    #chr(ord('A') + (ord(s) - ord('A') + 26) % 26)
                    encrypted_message = encrypted_message + chr(ord('A') + (ord(letter) - ord('A') + key) % 26)
                elif letter.islower():
                    encrypted_message = encrypted_message + chr(ord('a') + (ord(letter) - ord('a') + key) % 26)
            return encrypted_message
    except:
        print("An error occured, please ensure that you enter an integer for the key and that you provide a valid string")

#same logic as above but subtract the key instead of adding it
def caesar_decrypt(key, message):
    """Decrypt a message"""
    decrypted_message = ''
    try:
        if len(message) < 0:
            print('Please enter a non-empty message')
        elif 1 > int(key) or int(key) > 26:
            return 'Please enter a key value between 1 and 26 to shift the letters'
        else:
            for letter in message:
                if letter == ' ':
                    decrypted_message = decrypted_message + ' '
                elif not(letter.isalnum()):
                    decrypted_message = decrypted_message + letter
                elif letter.isupper():
                    #found this stackflow link which details how to cycle through unicode text using modular arithmetic 
                    #and only return letters https://stackoverflow.com/questions/64559066/limiting-ord-to-letters-only
                    #chr(ord('A') + (ord(s) - ord('A') + 26) % 26)
                    decrypted_message = decrypted_message + chr(ord('A') + (ord(letter) - ord('A') - key) % 26)
                elif letter.islower():
                    decrypted_message = decrypted_message + chr(ord('a') + (ord(letter) - ord('a') - key) % 26)
            return decrypted_message
    except:
        print("An error occured, please ensure that you enter an integer for the key and that you provide a valid string")
print(f'\t---BEGIN ENCRYPTION!---\nI will begin encrypting the Julius Caesar Quote "Experience is the teacher of all things." with a key of 12\n\t...encrypting...')
s = 'Experience is the teacher of all things.'
s_encrypted = caesar_encrypt(12, s)
print(f'The encrypted message is:\n{s_encrypted}\n\t ---DONE ENCRYPTING!---')

print(f'\t---BEGIN DECRYPTION!---\nI will begin decrypting the hidden message with a key of 12\n\t...decrypting...')
s_decrypted = caesar_decrypt(12, s_encrypted)
print(f'The original encrypted message is:\n{s_encrypted}\nThe decrypted message is:\n{s_decrypted}\n\t---DONE DECRYPTING!---')
#QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD
