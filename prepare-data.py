from os import listdir, rmdir, makedirs
from os.path import isdir, isfile, join
import hashlib
import shutil
import random

malware_path =  './raw-data/malware'
benign_path =   './raw-data/benign'
train_path =    './data/train'
valid_path =    './data/valid'
train_csv =    './data/train.csv'
valid_csv =    './data/valid.csv'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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
    malware_hash = md5('%s/%s' % (malware_path, malware))
    train_csv.write('%s,1\n' % malware_hash)
    shutil.copy('%s/%s' % (malware_path, malware), '%s/%s' % (train_path, malware_hash))
for benign in benigns_train:
    benign_hash = md5('%s/%s' % (benign_path, benign))
    train_csv.write('%s,0\n' % benign_hash)
    shutil.copy('%s/%s' % (benign_path, benign), '%s/%s' % (train_path, benign_hash))
train_csv.close()

valid_csv = open(valid_csv, "w")
for malware in malwares_valid:
    malware_hash = md5('%s/%s' % (malware_path, malware))
    valid_csv.write('%s,1\n' % malware_hash)
    shutil.copy('%s/%s' % (malware_path, malware), '%s/%s' % (valid_path, malware_hash))
for benign in benigns_valid:
    benign_hash = md5('%s/%s' % (benign_path, benign))
    valid_csv.write('%s,0\n' % benign_hash)
    shutil.copy('%s/%s' % (benign_path, benign), '%s/%s' % (valid_path, benign_hash))
valid_csv.close()
