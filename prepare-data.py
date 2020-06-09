import hashlib
import os
import random
import zipfile

from utils import ProgressBar, Chrono, malware_path, benign_path, train_path, valid_path, train_csv, valid_csv, Utils


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
    if not os.path.isdir(path):
        os.makedirs(path)

    csv_file = open(csv_file_name, "w")

    total_malwares = len(malwares)
    progress_bar.newbar(total_malwares, 'Malware')
    for i in range(total_malwares):
        with chrono.measure('step'):
            malware_hash = md5('%s/%s' % (malware_path, malwares[i]))
            csv_file.write('%s,1\n' % malware_hash)
            extract_dex('%s/%s' % (malware_path, malwares[i]), '%s/%s' % (path, malware_hash))
        progress_bar.update(i, 'Malware | Time: %s' % Utils.format_time(chrono.last('step')))

    total_benigns = len(benigns)
    progress_bar.newbar(total_benigns, 'Benign')
    for i in range(total_benigns):
        with chrono.measure('step'):
            benign_hash = md5('%s/%s' % (benign_path, benigns[i]))
            csv_file.write('%s,0\n' % benign_hash)
            extract_dex('%s/%s' % (benign_path, benigns[i]), '%s/%s' % (path, benign_hash))
        progress_bar.update(i, 'Benign | Time: %s' % Utils.format_time(chrono.last('step')))
    csv_file.close()


if __name__ == '__main__':
    progress_bar = ProgressBar()
    chrono = Chrono()

    if not os.path.isdir(train_path):
        os.makedirs(train_path)
    if not os.path.isdir(valid_path):
        os.makedirs(valid_path)

    malware_files = [f for f in os.listdir(malware_path) if os.path.isfile(os.path.join(malware_path, f))]
    benign_files = [f for f in os.listdir(benign_path) if os.path.isfile(os.path.join(benign_path, f))]

    random.shuffle(malware_files)
    random.shuffle(benign_files)

    malwares_split_index = int(0.8 * len(malware_files))
    malwares_train = malware_files[:malwares_split_index]
    malwares_valid = malware_files[malwares_split_index:]

    benigns_split_index = int(0.8 * len(benign_files))
    benigns_train = benign_files[:benigns_split_index]
    benigns_valid = benign_files[benigns_split_index:]

    print('Processing training dataset')
    with chrono.measure('process'):
        method_name(train_csv, train_path, malwares_train, benigns_train)
    print('Completed in: %s' % Utils.format_time(chrono.last('process')))

    print('Processing validation dataset')
    with chrono.measure('process'):
        method_name(valid_csv, valid_path, malwares_valid, benigns_valid)
    print('Completed in: %s' % Utils.format_time(chrono.last('process')))
    print('Total time: %s' % Utils.format_time(chrono.total('process')))
