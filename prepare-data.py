import hashlib
import os
import os.path as path
import random
import zipfile

malware_path = './raw-data/malware'
benign_path = './raw-data/benign'
train_path = './data/train'
valid_path = './data/valid'
train_csv = './data/train.csv'
valid_csv = './data/valid.csv'


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def extract_dex(source, target):
    apk_zip = zipfile.ZipFile(source, 'r')
    dex_zip = zipfile.ZipFile(target, mode='w')

    dex_files = [f for f in apk_zip.namelist() if f.endswith('.dex')]
    for dexFile in dex_files:
        apk_zip.extract(dexFile)
        dex_zip.write(dexFile)
        os.remove(dexFile)


def method_name(csv_file_name, path, malwares, benigns):
    if not path.isdir(path):
        os.makedirs(path)

    csv_file = open(csv_file_name, "w")
    for malware in malwares:
        malware_hash = md5('%s/%s' % (malware_path, malware))
        csv_file.write('%s,1\n' % malware_hash)
        extract_dex('%s/%s' % (malware_path, malware), '%s/%s' % (path, malware_hash))
    for benign in benigns:
        benign_hash = md5('%s/%s' % (benign_path, benign))
        csv_file.write('%s,0\n' % benign_hash)
        extract_dex('%s/%s' % (benign_path, benign), '%s/%s' % (path, benign_hash))
    csv_file.close()


if not path.isdir(train_path):
    os.makedirs(train_path);
if not path.isdir(valid_path):
    os.makedirs(valid_path);

malware_files = [f for f in os.listdir(malware_path) if path.isfile(path.join(malware_path, f))]
benign_files = [f for f in os.listdir(benign_path) if path.isfile(path.join(benign_path, f))]

random.shuffle(malware_files)
random.shuffle(benign_files)

malwares_split_index = int(0.8 * len(malware_files))
malwares_train = malware_files[:malwares_split_index]
malwares_valid = malware_files[malwares_split_index:]

benigns_split_index = int(0.8 * len(benign_files))
benigns_train = benign_files[:benigns_split_index]
benigns_valid = benign_files[benigns_split_index:]

method_name(train_csv, train_path, malwares_train, benigns_train)
method_name(valid_csv, valid_path, malwares_valid, benigns_valid)
