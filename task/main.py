import os
import shutil
import logging
import time
import hashlib
import sys

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, handlers=[
        logging.FileHandler("sync_app.log"),
        logging.StreamHandler()
    ])


def sync_files(src_path, replica_path):
    src_dir_list = os.listdir(src_path)
    replica_dir_list = os.listdir(replica_path)
    for files in src_dir_list:
        src_file_path = src_path + '/' + files
        if files in replica_dir_list:
            replica_file_path = replica_path + '/' + files
            check_flag = compare_files([src_file_path, replica_file_path])
            if not check_flag:
                logging.info(f'Copying contents in {files} to the copy in replica folder')
                shutil.copyfile(src_file_path, replica_file_path)
        else:
            logging.info(f'Copying {files} to the replica folder')
            shutil.copy2(src_file_path, replica_path)

def compare_files(file_list):
    digests = []
    for filename in file_list:
        hasher = hashlib.md5()
        with open(filename, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            a = hasher.hexdigest()
            digests.append(a)
    return digests[0] == digests[1]

def main():
    if len(sys.argv[1:]) < 3:
        logging.error('Invalid Arguments')
    else:
        src_path = sys.argv[1:][0]
        replica_path = sys.argv[1:][1]
        interval = int(sys.argv[1:][2])
        nexttime = time.time()
        while True:
            sync_files(src_path, replica_path)
            nexttime += interval
            sleeptime = nexttime - time.time()
            if sleeptime > 0:
                time.sleep(sleeptime)



if __name__ == '__main__':
    main()
