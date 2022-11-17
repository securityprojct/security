from django.shortcuts import render
import sys
import string
import math
import json
import requests

# ENCODING FUNCTION
def encode_words(words, shifts):
    """This encodes a word using Caesar cipher."""

    # Variable for storing the encoded word.
    encoded_word = ''

    for i in words:

        # Check for space and tab
        if ord(i) == 32 or ord(i) == 9:
            shifted_word = ord(i)

        # Check for punctuations
        elif i in string.punctuation:
            shifted_word = ord(i)

        # Check if the character is lowercase or uppercase
        elif i.islower():
            shifted_word = ord(i) + shifts

            # Lowercase spans from 97 to 122 (decimal) on the ASCII table
            # If the chars exceeds 122, we get the number it uses to exceed it and add to 96 (the character before a)
            if shifted_word > 122:
                shifted_word = (shifted_word - 122) + 96

        else:
            shifted_word = ord(i) + shifts

            # Uppercase spans from 65 to 90 (decimal) on the ASCII table
            # If the chars exceeds 90, we get the number it uses to exceed it and add to 64 (the character before A)
            if shifted_word > 90:
                shifted_word = (shifted_word - 90) + 64

        encoded_word = encoded_word + chr(shifted_word)
    return encoded_word
# DECODING FUNCTION


def decode_words(words, shifts):
    """This decodes a word using Caesar cipher"""

    # Variable for storing the decoded word.
    decoded_word = ''

    for i in words:

        # Check for space and tab
        if ord(i) == 32 or ord(i) == 9:
            shifted_word = ord(i)

        # Check for punctuations
        elif i in string.punctuation:
            shifted_word = ord(i)

        # Check if the character is lowercase or uppercase
        elif i.islower():
            shifted_word = ord(i) - shifts

            # If the char is less 122, we get difference subtract from 123 (the character after z)
            if shifted_word < 97:
                shifted_word = (shifted_word - 97) + 123

        else:
            shifted_word = ord(i) - shifts

            # If the char is less 65, we get difference and subtract from 91 (the character after Z)
            if shifted_word < 65:
                shifted_word = (shifted_word - 65) + 91

        decoded_word = decoded_word + chr(shifted_word)
    return decoded_word


def home(request):
    if request.method == "POST":
        text = request.POST.get('text')
        shift = request.POST.get('key')
        if request.POST.get('type') == "encode":
            result = encode_words(text, int(shift))
        elif request.POST.get('type') == "decode":
            result = decode_words(text, int(shift))
        # show = pass
        context = {'data': result, 'text': text, 'valu': shift}
        return render(request, 'caser.html', context=context)
    else:
        context = {'text': 'test', 'valu': 3}
        return render(request, 'caser.html', context=context)

# Implementation of Affine Cipher in Python
def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u*q, y-v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

# affine cipher encryption function
# returns the cipher text


def affine_encrypt(text, key):
    '''
    C = (a*P + b) % 26
    '''
    return ''.join([chr(((key[0]*(ord(t) - ord('A')) + key[1]) % 26)
                        + ord('A')) for t in text.upper().replace(' ', '')])


# affine cipher decryption function
# returns original text
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# Notre liste d'alphabet en minuscule
alphabet2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# Notre liste d'alhabet en majuscule


def pgcd(a, b):
    while b != 0:  # Boucle tant que b différent de 0
        a, b = b, a % b  # On change le a avec le b ensuite on fait a%b
    return a  # On retourne a


def inverse(a):
    x = 0  # x prend la valeur 0 au départ
    while (a*x % 26 != 1):  # Boucle tant que a*x%26 n'est pas différent de 1
        x = x+1  # x prend la valeure de x + 1 tant que la boucle est vrai
    return x  # On retourne la valeure de x


def dechiffrementAffine(a, b, L):
    if L in alphabet:  # Si L est une lettre en minuscule
        # x prend l'indice de la lettre dans l'alphabet en minuscule
        x = alphabet.index(L)
        # y prend la valeur de la lettre en minsucle L après déchiffrement affine
        y = (inverse(a)*(x-b)) % 26
        return alphabet[y]  # On retourne la lettre déchiffrée en minuscule
    elif L in alphabet2:  # Sinon si L est une lettre en majuscule
        # x prend l'indice de la lettre dans l'alphabet en majuscule
        x = alphabet2.index(L)
        # y prend la valeur de la lettre en majuscule L après déchiffrement affine
        y = (inverse(a)*(x-b)) % 26
        return alphabet2[y]  # On retourne la lettre déchiffrée en majuscle
    else:  # Sinon c'est un symbole non chiffré
        return L  # On retourne le symbole


def affine_decrypt(M, a, b):
    if (pgcd(a, 26) == 1):  # Si le pgcd de a et 26 est égale à 1
        mot = []  # On initialiste un string vide
        for i in range(0, len(M)):  # Boucle qui parcours la longeur du message à déchiffré
            # mot prend à chaque parcours la lettre déchiffré après appel à la fonction déchiffrementAffine et on la met à la fin de mot
            mot.append(dechiffrementAffine(a, b, M[i]))
        # On retourne le mot avec toute les lettres ou symboles déchiffrés
        return "".join(mot)
    else:  # Sinon il y a une erreur
        # On retourne que a n'est pas premier avec 26
        return "Déchiffrement impossible. Le nombre a n'est pas premier avec 26."


def affine(request):
    if request.method == "POST":
        text = request.POST.get('text')
        key11 = request.POST.get('key1')
        key22 = request.POST.get('key2')
        key1 = int(key11)
        key2 = int(key22)
        mylist = [key1, key2]
        if request.POST.get('type') == "encode":
            result = affine_encrypt(text, mylist)
        elif request.POST.get('type') == "decode":
            result = affine_decrypt(text, key1, key2)

        context = {'data': result, 'text': text, 'valu1': key1, 'valu2': key2}
        return render(request, 'affine.html', context=context)
    else:
        context = {'text': 'test', 'valu1': 3, 'valu2': 4}
        return render(request, 'affine.html', context=context)


def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return (key)
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])
    return ("" . join(key))


def vir_en(string, key):
    encrypt_text = []
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 26
        x += ord('A')
        encrypt_text.append(chr(x))
    return ("" . join(encrypt_text))


def vir_de(encrypt_text, key):
    orig_text = []
    for i in range(len(encrypt_text)):
        x = (ord(encrypt_text[i]) - ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return ("" . join(orig_text))


def vigenere(request):
    if request.method == "POST":
        text = request.POST.get('text')
        key = request.POST.get('key')
        keyx = generateKey(text, str(key).upper())
        if request.POST.get('type') == "encode":
            result = vir_en(str(text).upper(), keyx)
        elif request.POST.get('type') == "decode":
            text2 = request.POST.get('text')
            keyx2 = generateKey(text2, key)
            result = vir_de(text2, keyx2)
        context = {'data': result, 'text': text, 'valu': key}
        return render(request, 'vigenere.html', context=context)
    else:
        context = {'text': 'test', 'valu': 'slaw'}
        return render(request, 'vigenere.html', context=context)

# Python3 implementation of 
# Columnar Transposition
  
  
# Encryption
def encryptMessage(msg,k):
    cipher = ""
    key=""
    if(k=="1"):
        key="A"
    elif(k=="2"):
        key="AB"
    elif(k=="3"):
        key="ABC"
    elif(k=="4"):
        key="ABCD"
    elif(k=="5"):
        key="ABCDE"
    elif(k=="6"):
        key="ABCDEF"
    elif(k=="7"):
        key="ABCDEFG"
    elif(k=="8"):
        key="ABCDEFGH"
    elif(k=="9"):
        key="ABCDEFGHI"
    elif(k=="10"):
        key="ABCDEFGHIJ"
    elif(k=="11"):
        key="ABCDEFGHIJK"
    elif(k=="12"):
        key="ABCDEFGHIJKL"
    elif(k=="13"):
        key="ABCDEFGHIJKLM"
    elif(k=="14"):
        key="ABCDEFGHIJKLMN"
    elif(k=="15"):
        key="ABCDEFGHIJKLMNO"
    elif(k=="16"):
        key="ABCDEFGHIJKLMNOP"
    elif(k=="17"):
        key="ABCDEFGHIJKLMNOPQ"
    elif(k=="18"):
        key="ABCDEFGHIJKLMNOPQR"
    elif(k=="19"):
        key="ABCDEFGHIJKLMNOPQRS"
    elif(k=="20"):
        key="ABCDEFGHIJKLMNOPQRST"
    elif(k=="21"):
        key="ABCDEFGHIJKLMNOPQRSTU"
    elif(k=="22"):
        key="ABCDEFGHIJKLMNOPQRSTUV"
    elif(k=="23"):
        key="ABCDEFGHIJKLMNOPQRSTUVW"
    elif(k=="24"):
        key="ABCDEFGHIJKLMNOPQRSTUVWX"
    elif(k=="25"):
        key="ABCDEFGHIJKLMNOPQRSTUVWXY"
    elif(k=="26"):
        key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        key="A"
    # track key indices
    k_indx = 0
  
    msg_len = float(len(msg))
    msg_lst = list(msg)
    key_lst = sorted(list(key))
  
    # calculate column of the matrix
    col = len(key)
      
    # calculate maximum row of the matrix
    row = int(math.ceil(msg_len / col))
  
    # add the padding character '_' in empty
    # the empty cell of the matix 
    fill_null = int((row * col) - msg_len)
    msg_lst.extend('_' * fill_null)
  
    # create Matrix and insert message and 
    # padding characters row-wise 
    matrix = [msg_lst[i: i + col] 
              for i in range(0, len(msg_lst), col)]
  
    # read matrix column-wise using key
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx] 
                          for row in matrix])
        k_indx += 1
  
    return cipher
  
# Decryption
def decryptMessage(cipher,k):
    msg = ""
    key=""
    if(k=="1"):
        key="A"
    elif(k=="2"):
        key="AB"
    elif(k=="3"):
        key="ABC"
    elif(k=="4"):
        key="ABCD"
    elif(k=="5"):
        key="ABCDE"
    elif(k=="6"):
        key="ABCDEF"
    elif(k=="7"):
        key="ABCDEFG"
    elif(k=="8"):
        key="ABCDEFGH"
    elif(k=="9"):
        key="ABCDEFGHI"
    elif(k=="10"):
        key="ABCDEFGHIJ"
    elif(k=="11"):
        key="ABCDEFGHIJK"
    elif(k=="12"):
        key="ABCDEFGHIJKL"
    elif(k=="13"):
        key="ABCDEFGHIJKLM"
    elif(k=="14"):
        key="ABCDEFGHIJKLMN"
    elif(k=="15"):
        key="ABCDEFGHIJKLMNO"
    elif(k=="16"):
        key="ABCDEFGHIJKLMNOP"
    elif(k=="17"):
        key="ABCDEFGHIJKLMNOPQ"
    elif(k=="18"):
        key="ABCDEFGHIJKLMNOPQR"
    elif(k=="19"):
        key="ABCDEFGHIJKLMNOPQRS"
    elif(k=="20"):
        key="ABCDEFGHIJKLMNOPQRST"
    elif(k=="21"):
        key="ABCDEFGHIJKLMNOPQRSTU"
    elif(k=="22"):
        key="ABCDEFGHIJKLMNOPQRSTUV"
    elif(k=="23"):
        key="ABCDEFGHIJKLMNOPQRSTUVW"
    elif(k=="24"):
        key="ABCDEFGHIJKLMNOPQRSTUVWX"
    elif(k=="25"):
        key="ABCDEFGHIJKLMNOPQRSTUVWXY"
    elif(k=="26"):
        key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        key="A"
    # track key indices
    k_indx = 0
  
    # track msg indices
    msg_indx = 0
    msg_len = float(len(cipher))
    msg_lst = list(cipher)
  
    # calculate column of the matrix
    col = len(key)
      
    # calculate maximum row of the matrix
    row = int(math.ceil(msg_len / col))
  
    # convert key into list and sort 
    # alphabetically so we can access 
    # each character by its alphabetical position.
    key_lst = sorted(list(key))
  
    # create an empty matrix to 
    # store deciphered message
    dec_cipher = []
    for _ in range(row):
        dec_cipher += [[None] * col]
  
    # Arrange the matrix column wise according 
    # to permutation order by adding into new matrix
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
  
        for j in range(row):
            dec_cipher[j][curr_idx] = msg_lst[msg_indx]
            msg_indx += 1
        k_indx += 1
  
    # convert decrypted msg matrix into a string
    try:
        msg = ''.join(sum(dec_cipher, []))
    except TypeError:
        raise TypeError("This program cannot",
                        "handle repeating words.")
  
    null_count = msg.count('_')
  
    if null_count > 0:
        return msg[: -null_count]
  
    return msg

def columnart(request):
    if request.method == "POST":
        text = request.POST.get('text')
        key = request.POST.get('key')
        if request.POST.get('type') == "encode":
            result3 = encryptMessage(text,key)
            context = {'data': result3, 'text': text, 'valu': key}
        elif request.POST.get('type') == "decode":
            # text2 = request.POST.get('text')
            result = decryptMessage(text,key)
            context = {'data': result, 'text': text, 'valu': key}
        return render(request, 'columnar_t.html', context=context)
    else:
        context = {'text': 'test', 'valu': 'slaw'}
        return render(request, 'columnar_t.html', context=context)


def encryptSimple(p,k):
    text=str(p)
    sort=k 
    payload = {
            'tool': 'transposition-cipher',
            'plaintext': text,
            'keep_punctuation': 'true',
            'permutation': '{"permutation":['+sort+']}',
            'directions': 'hh',
            'fill': 'false',}
    url = 'https://www.dcode.fr/transposition-cipher'

    with requests.Session() as s:
        r = s.post(url, data=payload)
        lol = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        lol=str(lol).replace("{","",1)
        lol=lol.replace("}",",")
    try:
        text=str(p)
        sort=k 
        k=lol.replace("'PHPSESSID': ","")
        k=k[1:]
        k=k[:-1]
        k=k[:-1]
        cookies = {
            'PHPSESSID': k,
        }
        headers = {
            'referer': 'https://www.dcode.fr/transposition-cipher',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'tool': 'transposition-cipher',
            'plaintext': text,
            'keep_punctuation': 'true',
            'permutation': '{"permutation":['+sort+']}',
            'directions': 'hh',
            'fill': 'false',
        }
        response = requests.post('https://www.dcode.fr/api/', headers=headers, data=data,cookies=cookies)
        r = json.loads(response.text)
        return r["results"]
    except KeyError:
        return "Please update cookies!"

def decryptSimple(p,k):
    text=str(p)
    sort=k 
    payload = {
            'tool': 'transposition-cipher',
            'plaintext': text,
            'keep_punctuation': 'true',
            'permutation': '{"permutation":['+sort+']}',
            'directions': 'hh',
            'fill': 'false',}
    url = 'https://www.dcode.fr/transposition-cipher'

    with requests.Session() as s:
        r = s.post(url, data=payload)
        lol = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        lol=str(lol).replace("{","",1)
        lol=lol.replace("}",",")
    try:
        text=str(p)
        sort=k 
        k=lol.replace("'PHPSESSID': ","")
        k=k[1:]
        k=k[:-1]
        k=k[:-1]
        cookies = {
            'PHPSESSID': k,
        }
        headers = {
            'referer': 'https://www.dcode.fr/transposition-cipher',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'tool': 'transposition-cipher',
            'ciphertext': text,
            'keep_punctuation': 'false',
            'lang': 'en',
            'method': 'key',
            'permutation': '{"permutation":['+sort+']}',
            'key_length': 'true',
            'directions': 'hh',
        }

        response = requests.post('https://www.dcode.fr/api/', headers=headers, data=data,cookies=cookies)
        r = json.loads(response.text)
        return r["results"]
    except KeyError:
        return "Please update cookies!"
  
def simplet(request):
    if request.method == "POST":
        text = request.POST.get('text')
        key = request.POST.get('pkey')
        print(key)
        if request.POST.get('type') == "encode":
            result3 = encryptSimple(text,key)
            context = {'data': result3, 'text': text, 'valu': key}
        elif request.POST.get('type') == "decode":
            # text2 = request.POST.get('text')
            result = decryptSimple(text,key)
            context = {'data': result, 'text': text, 'valu': key}
        return render(request, 'simple_t.html', context=context)
    else:
        context = {'text': 'test', 'valu': 'slaw'}
        return render(request, 'simple_t.html', context=context)
    return render(request, 'simple_t.html', context={})

def encryptIrregular(msg,key):
    cipher = ""
  
    # track key indices
    k_indx = 0
  
    msg_len = float(len(msg))
    msg_lst = list(msg)
    key_lst = sorted(list(key))
  
    # calculate column of the matrix
    col = len(key)
      
    # calculate maximum row of the matrix
    row = int(math.ceil(msg_len / col))
  
    # add the padding character '_' in empty
    # the empty cell of the matix 
    fill_null = int((row * col) - msg_len)
    msg_lst.extend('_' * fill_null)
  
    # create Matrix and insert message and 
    # padding characters row-wise 
    matrix = [msg_lst[i: i + col] 
              for i in range(0, len(msg_lst), col)]
  
    # read matrix column-wise using key
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx] 
                          for row in matrix])
        k_indx += 1
  
    return cipher

def decryptIrregular(cipher,key):
    msg = ""
  
    # track key indices
    k_indx = 0
  
    # track msg indices
    msg_indx = 0
    msg_len = float(len(cipher))
    msg_lst = list(cipher)
  
    # calculate column of the matrix
    col = len(key)
      
    # calculate maximum row of the matrix
    row = int(math.ceil(msg_len / col))
  
    # convert key into list and sort 
    # alphabetically so we can access 
    # each character by its alphabetical position.
    key_lst = sorted(list(key))
  
    # create an empty matrix to 
    # store deciphered message
    dec_cipher = []
    for _ in range(row):
        dec_cipher += [[None] * col]
  
    # Arrange the matrix column wise according 
    # to permutation order by adding into new matrix
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
  
        for j in range(row):
            dec_cipher[j][curr_idx] = msg_lst[msg_indx]
            msg_indx += 1
        k_indx += 1
  
    # convert decrypted msg matrix into a string
    try:
        msg = ''.join(sum(dec_cipher, []))
    except TypeError:
        raise TypeError("This program cannot",
                        "handle repeating words.")
  
    null_count = msg.count('_')
  
    if null_count > 0:
        return msg[: -null_count]
  
    return msg
def irregulart(request):
    if request.method == "POST":
        text = request.POST.get('text')
        text.upper()
        key = request.POST.get('key')
        key.upper()
        if request.POST.get('type') == "encode":
            result3 = encryptIrregular(text,key)
            context = {'data': result3, 'text': text, 'valu': key}
        elif request.POST.get('type') == "decode":
            # text2 = request.POST.get('text')
            result = decryptIrregular(text,key)
            context = {'data': result, 'text': text, 'valu': key}
        return render(request, 'irregular_t.html', context=context)
    else:
        context = {'text': 'test', 'valu': 'slaw'}
        return render(request, 'irregular_t.html', context=context)
    return render(request, 'irregular_t.html', context={})