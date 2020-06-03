from os import listdir
from os.path import isfile, join
import random

malwarepath = './data/malware'
benignpath = './data/benign'

malwares = [f for f in listdir(malwarepath) if isfile(join(malwarepath, f))]
benigns = [f for f in listdir(benignpath) if isfile(join(benignpath, f))]

random.shuffle(malwares)
random.shuffle(benigns)

malwares_split_index = int(0.8*len(malwares))
malwares_train = malwares[:malwares_split_index]
malwares_valid = malwares[malwares_split_index:]

benigns_split_index = int(0.8*len(benigns))
benigns_train = benigns[:benigns_split_index]
benigns_valid = benigns[benigns_split_index:]

train_csv = open("./data/train-label.csv", "w")
for malware in malwares_train:
    train_csv.write('%s,1\n' % malware)
for benign in benigns_train:
    train_csv.write('%s,0\n' % benign)
train_csv.close()

valid_csv = open("./data/valid-label.csv", "w")
for malware in malwares_valid:
    valid_csv.write('%s,1\n' % malware)
for benign in benigns_valid:
    valid_csv.write('%s,0\n' % benign)
valid_csv.close()
