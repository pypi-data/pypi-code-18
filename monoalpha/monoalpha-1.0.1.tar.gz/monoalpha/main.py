# Functions for monoalpha - please read README.txt for more information

import string

def alphatrans(plaintext, alpha1, alpha2):
    """
    Function for translation from a plaintext alphabet to a 
    codetext alphabet.

    Args:
    plaintext -- plaintext to be coded.
    alpha1 -- plaintext alphabet.
    alpha2 -- codetext alphabet.

    Returns:
    Coded text string.
    """
    alpha1 = alpha1.lower()
    alpha2 = alpha2.lower()
    plaintext = plaintext.lower()
    codetext = "" # Initialises the coded text to be returned.
    for char in plaintext:
        try:
            # Attempts to locate character of plaintext in alpha1,
            # and add the corresponding character of alpha2
            # to codetext.
            index = alpha1.index(char)
            codetext += alpha2[index].upper()
        except:
            # Adds original character to codetext if it cannot be encrypted.
            codetext += char
    return codetext


def encrypt(plaintext, alphabet):
    """
    Function for translation from the Latin alphabet to a codetext 
    alphabet.

    Args:
    plaintext -- plaintext to be coded.
    alphabet -- codetext alphabet.

    Returns:
    Coded text string.
    """
    plainalpha = string.ascii_lowercase # Gets plaintext alpabet.
    return alphatrans(plaintext, plainalpha, alphabet)

def decrypt(plaintext, alphabet):
    """
    Function for translation from a codetext alphabet to
    the Latin alpabet.

    Args:
    plaintext -- plaintext to be coded.
    alphabet -- codetext alphabet.

    Returns:
    Coded text string.
    """
    plainalpha = string.ascii_lowercase # Gets plaintext alpabet.
    return alphatrans(plaintext, alphabet, plainalpha)


def caesar(offset):
    """
    Function returning a caesar-shifted alphabet.

    Args:
    offset -- caesar shift offset.

    Returns:
    Code alphabet.
    """
    offset = int(offset)
    plainalpha = string.ascii_lowercase
    codealpha = "" # Initialises the coded alphabet to be returned.
    for i in range(26):
        # Adds offset to index, and then applies modulo
        # to keep within the range of the alphabet.
        index = (i+offset)%26
        codealpha += plainalpha[index]
    return codealpha

def rot13():
    """
    Function returning a the ROT13 code alphabet.

    Returns:
    Coded text string.
    """
    return caesar(13)

def affine(a, b):
    """
    Function returning an affine code alphabet.

    Args:
    a -- "a" paramater.
    b -- "b" paramater.

    Returns:
    Code alphabet.
    """
    a = int(a)
    b = int(b)
    plainalpha = string.ascii_lowercase
    codealpha = "" # Initialises the coded alphabet to be returned.
    for i in range(26):
        index = ((a*i)+b)%26 # Applies the affine formula to the index.
        codealpha += plainalpha[index]
    return codealpha

def atbash():
    """
    Function returning the atbash code alphabet.

    Returns:
    Code alphabet.
    """
    # Atbash is the same as affine where a = 25 and b = 25.
    return affine(25, 25)

def keyword(word):
    """
    Function returning a keyword code alphabet.

    Args:
    word -- keyword.

    Returns:
    Code alphabet.
    """
    plainalpha = string.ascii_lowercase
    word = word.lower()
    codealpha = ""
    for char in word:
        if char in plainalpha:
            codealpha += char
            # Removes character so it will not be repeated.
            plainalpha = plainalpha.replace(char, "")
    for char in plainalpha:
        codealpha += char # Adds remainder of alphabet.
    return codealpha


def caesar_encrypt(plaintext, offset):
    """
    Function for caeser cipher encryption.

    Args:
    plaintext -- plaintext to be encrypted.

    Returns:
    Coded text string.
    """
    return encrypt(plaintext, caesar(offset))

def caesar_decrypt(plaintext, offset):
    """
    Function for caeser cipher decryption.

    Args:
    plaintext -- plaintext to be decrypted.

    Returns:
    Plain text string.
    """
    return decrypt(plaintext, caesar(offset))

def rot13_encrypt(plaintext):
    """
    Function for ROT13 cipher encryption.

    Args:
    plaintext -- plaintext to be encrypted.
    
    Returns:
    Coded text string.
    """
    return encrypt(plaintext, rot13())

def rot13_decrypt(plaintext):
    """
    Function for ROT13 cipher decryption.

    Args:
    plaintext -- plaintext to be decrypted.

    Returns:
    Plain text string.
    """
    return decrypt(plaintext, rot13())

def affine_encrypt(plaintext, a, b):
    """
    Function for affine cipher encryption.

    Args:
    plaintext -- plaintext to be encrypted.
    a -- "a" parameter.
    b -- "b" parameter.

    Returns:
    Coded text string.
    """
    return encrypt(plaintext, affine(a, b))

def affine_decrypt(plaintext, a, b):
    """
    Function for caeser cipher decryption.

    Args:
    plaintext -- plaintext to be decrypted.
    a -- "a" parameter.
    b -- "b" parameter.

    Returns:
    Plain text string.
    """
    return decrypt(plaintext, affine(a, b))

def atbash_encrypt(plaintext):
    """
    Function for atbash cipher encryption.

    Args:
    plaintext -- plaintext to be encrypted.

    Returns:
    Coded text string.
    """
    return encrypt(plaintext, atbash())

def atbash_decrypt(plaintext):
    """
    Function for atbash cipher decryption.

    Args:
    plaintext -- plaintext to be decrypted.

    Returns:
    Plain text string.
    """
    return decrypt(plaintext, atbash())

def keyword_encrypt(plaintext, word):
    """
    Function for keyword cipher encryption.

    Args:
    plaintext -- plaintext to be encrypted.
    word -- keyword.

    Returns:
    Coded text string.
    """
    return encrypt(plaintext, keyword(word))

def keyword_decrypt(plaintext, word):
    """
    Function for keyword cipher decryption.

    Args:
    plaintext -- plaintext to be decrypted.
    word -- keyword.

    Returns:
    Plain text string.
    """
    return decrypt(plaintext, keyword(word))
