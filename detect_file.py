import numpy as np
import database_logic
import hashlib
import concurrent.futures

def get_md5_hash(file_name):
    hash_of_file = ''
    hasher = hashlib.md5()
    with open(file_name, 'rb') as openFile:
        content = openFile.read()
    hasher.update(content)
    hash_of_file = hasher.hexdigest()
    return hash_of_file

def logic(file_name):
    database = database_logic.import_data_from_database('database/malware_file_samples.data')
    #print(len(database))
    hash_of_test = get_md5_hash(file_name)
    malicious_string = 'Warning! Malicious file!'
    clean_string = 'Clean file!'
    if hash_of_test in database:
        #print(hash_of_test)
        return malicious_string
    else:
        #print(hash_of_test)
        return clean_string

def threaded_logic(file_name):
    def classifier():
        database = database_logic.import_data_from_database('database/malware_file_samples.data')
        hash_of_test = get_md5_hash(file_name)
        malicious_string = 'Warning! Malicious file!'
        clean_string = 'Clean file!'
        if hash_of_test in database:
            #print(hash_of_test)
            return malicious_string
        else:
            #print(hash_of_test)
            return clean_string
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(classifier)
        return classifier()
