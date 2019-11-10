
# Convert fo AES module
# author: Marcin Ziajkowski
import Cryptodome

# from_string_to_SHA512
import hashlib
# AES_encode, AES_decode
from Crypto.Cipher import AES



def from_string_to_SHA512(key:str):
    m = hashlib.sha512()
    res = bytes(key, 'utf-8') 
    m.update(res)
    return m.hexdigest()
    
def AES_encode(sha512Key, textToEncode):
    data = bytes(textToEncode, 'utf-8')
    key = bytes(sha512Key, 'utf-8')[:16]

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    nonce = cipher.nonce
    encoded_data = (ciphertext, tag, nonce)
    
    return encoded_data


def AES_decode(sha512Key, encoded_data):
    key = bytes(sha512Key, 'utf-8')[:16]
    nonce = encoded_data[2]
    tag = encoded_data[1]
    ciphertext = encoded_data[0]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_data


if __name__ == "__main__":
    
    print("General Kenobi")

    klucz = 'Tajny klucz sha512'
    sha512Key = from_string_to_SHA512(klucz)

    text = "Amper jest moim prywatnym kotem!"
    encoded_data = AES_encode(sha512Key, text)
    print(encoded_data[0])

    decrypted_data = AES_decode(sha512Key, encoded_data)
    print(decrypted_data)



    
