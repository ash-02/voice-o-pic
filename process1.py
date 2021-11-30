import re
import process2
import nltk
from nltk import text

def part(text):
    words = text.split()
    part_of_speech = nltk.pos_tag(words)
    print(part_of_speech)
    # word = [words_with_pos[0] for words_with_pos in part_of_speech]
    # tag = [words_with_pos[1] for words_with_pos in part_of_speech]
    # print(word)
    # print(tag)
    # print(type(word))
    # print(words)

    words_with_pos=[]

    for grp in part_of_speech:
            noun = re.search(r'N[A-Z]', grp[1])
            pronoun = re.search(r'PR[A-Z$]', grp[1])
            pronoun1 = re.search(r'words_with_pos[P$]', grp[1])
            verb = re.search(r'V[A-Z]', grp[1])
            adjective = re.search(r'J[A-Z]', grp[1])
            adverb = re.search(r'R[A-Z]', grp[1])
            adverb1 = re.search(r'WRB', grp[1])
            preposition = re.search(r'IN', grp[1])
            conjunction = re.search(r'CC', grp[1])
            interjection = re.search(r'UH', grp[1])
            to = re.search(r'TO', grp[1])
            determiner = re.search(r'DT', grp[1])

            if noun:
                words_with_pos.append(tuple((grp[0], "noun")))
            if pronoun:
                words_with_pos.append(tuple((grp[0], "pronoun")))
            if pronoun1:
                words_with_pos.append(tuple((grp[0], "pronoun")))
            if verb:
                words_with_pos.append(tuple((grp[0], "verb")))
            if adjective:
                words_with_pos.append(tuple((grp[0], "adjective")))
            if adverb:
                words_with_pos.append(tuple((grp[0], "adverb")))
            if adverb1:
                words_with_pos.append(tuple((grp[0], "adverb")))
            if preposition:
                words_with_pos.append(tuple((grp[0], "preposition")))
            if conjunction:
                words_with_pos.append(tuple((grp[0], "conjunction")))
            if interjection:
                words_with_pos.append(tuple((grp[0], "interjection")))
            if to:
                words_with_pos.append(tuple((grp[0], "to")))
            if determiner:
                words_with_pos.append(tuple((grp[0], "determiner")))

    print(words_with_pos)
    return process2.search_and_download(words_with_pos)