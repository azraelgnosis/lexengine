import csv
import os

tengwar_path = os.path.dirname(__file__)

consonants = {}
with open(os.path.join(tengwar_path, "cymraeg_consonants.csv"), "r", newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        consonants[row[0]] = {'key': row[1], 'position': int(row[2])}

digraphs = {
    'c': ['h'], 
    'd': ['d'], 
    'f': ['f'],
    'l': ['l'], 
    'p': ['h'], 
    'n': ['g', 'h'],
    'm': ['h'], 
    'r': ['h'], 
    't': ['h']
}

vowels = {}
with open(os.path.join(tengwar_path, "cymraeg_vowels.csv"), "r", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    for row in reader:
        vowels[row[0]] = row[1].split(',')

diphthongs = {
    'a': ['e', 'i', 'u', 'w'],
    'e': ['i', 'u', 'y', 'w'],
    'i': ['w'],
    'o': ['e', 'i', 'u'],
    'u': ['w'],
    'w': ['y'],
    'y': ['w']
}

vowels_long = ['â', 'ê', 'î', 'ô', 'û', 'ŵ', 'ŷ']

def convert(word:str) -> str:
    tengwar = ""
    vowel = ""

    i = 0
    while i < len(word):
        letter = word[i]

        if letter in consonants:
            if (graph := word[i:i+3]) in consonants:
                if letter == 's' and vowel:
                    tengwar += 'i'
                else:
                    tengwar += consonants.get(graph)['key']
                i += 2
            elif (graph := word[i:i+2]) in consonants:
                if letter == 's' and vowel:
                    tengwar += 'i'
                else:
                    tengwar += consonants.get(graph)['key']
                i += 1
            elif (graph := word[i]) in consonants:
                if letter == 's' and vowel:
                    tengwar += 'i'
                else:
                    tengwar += consonants.get(graph)['key']
                
            if vowel:
                if vowel == 'a' and word[i:i+2] in ('ff', 'ph', 'th'):
                    tengwar += 'D'
                elif vowel == 'y' and any([V in vowels for V in word[i+1:]]):
                    if letter == 's':
                        tengwar = tengwar[:-1] + '8'
                    tengwar += '(' if consonants.get(graph)['position'] == 0 else 'O'
                else:
                    tengwar += vowels.get(vowel)[consonants.get(graph)['position']]
                vowel = ""

        elif letter in vowels:
            if letter in vowels_long:
                tengwar += '~' + vowels.get(letter)[0]
            elif i == len(word)-1: # vowel-final word
                if letter == 'y' and len([x for x in word if x in vowels]) == 1:
                    tengwar += '(' if consonants.get(graph)['position'] == 0 else 'O'
                else:
                    tengwar += '`' + vowels.get(letter)[3]
            elif (diphthong := word[i:i+2]) in vowels: # diphthongs
                tengwar += vowels.get(diphthong)[0]
                i += 1
            elif word[i+1] in vowels:
                tengwar += '`' + vowels.get(letter)[3]
            else:
                vowel = letter
            
        else:
            raise KeyError(f"Character '{letter}' not available.")
        i += 1

    return tengwar

def conversion(cymraeg):
    return " ".join([convert(word.lower()) for word in cymraeg.split(" ")])
