import os
import re
import string
import random
from graph import Graph

def get_words_from_text(text_path):
    with open(text_path, 'rb') as file:
        text = file.read().decode("utf-8")#read the file 

        # remove [verse 1: artist]
        # include the following line if you are doing song lyrics
        # text = re.sub(r'\[(.+)\]', ' ', text)

        text = ' '.join(text.split())#join the words
        text = text.lower()#lowercase the text
        text = text.translate(str.maketrans('', '', string.punctuation))#remove punctuation

    words = text.split()#split the text into words

    words = words[:1000]#limit the words to 1000

    return words

# makes a graph from the words
def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if does not exist
        # if exists, increment weight by 1
        if prev_word:  # prev word should be a Vertex
            # check if edge exists from previous word to current word
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex#set the previous word to the current word

    g.generate_probability_mappings()#generate probability mappings
    
    return g

# makes a composition from the graph
def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)#add the word to the composition
        word = g.get_next_word(word)#get the next word

    return composition

# main function
def main():
    words = get_words_from_text('texts/hp_sorcerer_stone.txt')

    # for song in os.listdir('songs/{}'.format(artist)):
        # if song == '.DS_Store':
        #     continue
        # words.extend(get_words_from_text('songs/{artist}/{song}'.format(artist=artist, song=song)))
    
    # make a graph    
    g = make_graph(words)
    # make a composition
    composition = compose(g, words, 100)
    print(' '.join(composition))


if __name__ == '__main__':
    main()