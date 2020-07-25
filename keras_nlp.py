from numpy import array
from keras.utils import to_categorical
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
import csv
import nltk
from nltk.corpus import stopwords
import neo4j_test


# generate a sequence from a language model
def test(query):
    tokens1 = nltk.word_tokenize(query)
    tagged1 = nltk.pos_tag(tokens1)
    stop_words = stopwords.words('english')
    words1 = [w[0].lower() for w in tagged1 if not w[0] in stop_words]
    for w in words1:
        if w in unique_words:
            pass
        else:
            words1.remove(w)
            print(w)
    # words1 = [w[0] for w in words1 if not w[1].startswith('P')]
    encoded = np.zeros(shape=(1, 242))
    for i in words1:
        if i == '':
            continue
        encoded[0][words_dic[i]] = 1
    print(words1)
    # print(array(encoded).shape)
    predict = model.predict(encoded)
    #return np.argmax(predict) + 1
    return neo4j_test.gen_res(np.argmax(predict)+1)


X1 = []
Y1 = []

unique_words = []
with open('RNN_data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        tokens1 = nltk.word_tokenize(row[1])
        tagged1 = nltk.pos_tag(tokens1)
        tokens = nltk.word_tokenize(row[0])
        tagged = nltk.pos_tag(tokens)
        stop_words = stopwords.words('english')
        words1 = [w for w in tagged1 if not w[0] in stop_words]
        words = [w for w in tagged if not w[0] in stop_words]
        words1 = [w for w in words1 if not w[1].startswith('P')]
        words = [w for w in words if not w[1].startswith('P')]
        unique_words.extend([x[0].lower() for x in words])
        unique_words.extend([x[0].lower() for x in words1])
        X1 = X1 + [" ".join(x[0].lower() for x in words1)]
        Y1 = Y1 + [" ".join(x[0].lower() for x in words)]

unique_words = list(set(unique_words))
arr = range(len(unique_words))
words_dic = dict(zip(unique_words, arr))

vocab_size = len(unique_words)
print('Vocabulary Size: %d' % vocab_size)
# create line-based sequences
encoded = np.zeros(shape=(len(X1), vocab_size))
# print(words_dic['pain'])
k = 0
for line in X1:
    for i in line.strip().split(' '):
        if i == '':
            continue
        encoded[k][words_dic[i.lower()]] = 1
    k += 1
# print(encoded[2])
encoded = encoded[:-1]
print('Total Sequences: %d' % len(encoded))
# split into input and output elements
Y1 = Y1[:-1]
Y1 = [int(x) - 1 for x in Y1]
# print(Y1)
y = to_categorical(Y1, num_classes=30)
# print(y[0])
# exit(0)
X = encoded[:, :]

#print(X[0])
# exit(0)

model = Sequential()
model.add(Dense(60, activation='sigmoid', input_dim=vocab_size))
model.add(Dense(40, activation='sigmoid'))
model.add(Dense(30, activation='softmax'))

# compile network
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

model.fit(X, y, epochs=500, verbose=2)
#print(X.shape)
# print(model.predict(X))

# evaluate model
#print(test('sweat in sleep'))
# print(generate_seq(model, tokenizer, max_length, 'Rising body temperature', 4))
# print(generate_seq(model, tokenizer, max_length, 'eye infection', 4))