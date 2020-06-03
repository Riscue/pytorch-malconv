from os import listdir, rmdir, makedirs
from os.path import isdir, isfile, join
import shutil
import random

malware_path =  './data/malware'
benign_path =   './data/benign'
train_path =    './data/train'
valid_path =    './data/valid'
train_csv =    './data/train.csv'
valid_csv =    './data/valid.csv'

if not isdir(train_path):
        makedirs(train_path);
if not isdir(valid_path):
        makedirs(valid_path);

malwares = [f for f in listdir(malware_path) if isfile(join(malware_path, f))]
benigns = [f for f in listdir(benign_path) if isfile(join(benign_path, f))]

random.shuffle(malwares)
random.shuffle(benigns)

malwares_split_index = int(0.8*len(malwares))
malwares_train = malwares[:malwares_split_index]
malwares_valid = malwares[malwares_split_index:]

benigns_split_index = int(0.8*len(benigns))
benigns_train = benigns[:benigns_split_index]
benigns_valid = benigns[benigns_split_index:]

train_csv = open(train_csv, "w")
for malware in malwares_train:
    train_csv.write('%s,1\n' % malware)
    shutil.move('%s/%s' % (malware_path, malware), train_path)
for benign in benigns_train:
    train_csv.write('%s,0\n' % benign)
    shutil.move('%s/%s' % (benign_path, benign), train_path)
train_csv.close()

valid_csv = open(valid_csv, "w")
for malware in malwares_valid:
    valid_csv.write('%s,1\n' % malware)
    shutil.move('%s/%s' % (malware_path, malware), valid_path)
for benign in benigns_valid:
    valid_csv.write('%s,0\n' % benign)
    shutil.move('%s/%s' % (benign_path, benign), valid_path)
valid_csv.close()

if isdir(malware_path) and not listdir(malware_path) :
    rmdir(malware_path)

if isdir(benign_path) and not listdir(benign_path) :
    rmdir(benign_path)
