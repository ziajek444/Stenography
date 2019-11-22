
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
    encoded_data = (tag, nonce, ciphertext)
    
    return encoded_data


def bytes_to_string(bytes_container):
    assert type(bytes_container) == bytes
    assert len(bytes_container) > 0
    dataString = ''
    for b in bytes_container:
        dataString += chr(b)
    return dataString


def convert_encode_to_string(encoded_data):
    # convert [tag (16B), nonce (16B), cripertext (xB) ]
    # to solid string 16+16+x Characters
    (tag, nonce, ciphertext) = encoded_data
    # check
    assert len(tag) == 16
    assert len(nonce) == 16
    assert len(ciphertext) > 0
    fullLen = 32 + len(ciphertext)
    # convert
    data_l = ['','','']
    data_l[0] = bytes_to_string(tag)
    data_l[1] = bytes_to_string(nonce)
    data_l[2] = bytes_to_string(ciphertext)
    # check
    assert len(data_l[0]) == 16 and len(data_l[1]) == 16
    assert fullLen == len(data_l[0]) + len(data_l[1]) + len(data_l[2])
    # summary
    return_str = data_l[0] + data_l[1] + data_l[2]
    if type(return_str) == str and len(return_str) == fullLen:
        return return_str
    else:
        raise 'convert error (convert_encode_to_string)'


def convert_string_to_encode(str_data):
    # split string to 3 values,
    # tag, nounce and cripertext
    # tag is 16B, nonce is 16B, rest is cripertext
    # split strings
    # test data
    assert type(str_data) == str and len(str_data) > 32
    fullLength = len(str_data)
    tag = str_data[0:16]
    nonce = str_data[16:32]
    cripertext = str_data[32:]
    # make int lists
    tag_l = []
    for t in tag:
        tag_l.append(ord(t))
    nonce_l = []
    for t in nonce:
        nonce_l.append(ord(t))
    cripertext_l = []
    for t in cripertext:
        cripertext_l.append(ord(t))
    # make bytearrays from lists
    tag_ba = bytearray(tag_l)
    nonce_ba = bytearray(nonce_l)
    cripertext_ba = bytearray(cripertext_l)
    # make bytes for return
    tag_b = bytes(tag_ba)
    nonce_b = bytes(nonce_ba)
    cripertext_b = bytes(cripertext_ba)
    # check data
    assert len(tag_b) == 16 and len(nonce_b) == 16 and len(cripertext_b) > 0
    assert fullLength == 32 + len(cripertext_b)
    # clustered data to one structure
    encoded_data = (tag_b, nonce_b, cripertext_b)
    return encoded_data


def AES_decode(sha512Key, encoded_data, returnBytes = False):
    key = bytes(sha512Key, 'utf-8')[:16]
    nonce = encoded_data[1]
    tag = encoded_data[0]
    assert len(tag) == 16
    assert len(nonce) == 16
    assert len(key) == 16
    ciphertext = encoded_data[2]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    returnData = None
    if type(decrypted_data) == bytes and returnBytes:
            returnData = decrypted_data
    elif type(decrypted_data) != bytes and returnBytes:
        raise 'not implemented !!'
    elif type(decrypted_data) != bytes and not returnBytes:
        raise 'not implemented !!'
    else:
        returnData = bytes_to_string(decrypted_data)

    return returnData


if __name__ == "__main__":
    
    print("General Kenobi ?")

    # String-Byte-String converter test
    shaKey = '0123456789abcdef'
    SecretData = 'Amper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kotatny kotAmper to moj prywatny kotAmper to moj prywatny kotAmper to moj prywatny kot'
    topSecret = AES_encode(shaKey, SecretData)
    testString = convert_encode_to_string(topSecret)
    testBytes = convert_string_to_encode(testString)
    for i in range(3):
        print(topSecret[i])
        print(testBytes[i])
        assert topSecret[i] == testBytes[i]

    ExternData = AES_decode(shaKey, testBytes)
    print(ExternData)
    assert ExternData == SecretData
    print("ok")
