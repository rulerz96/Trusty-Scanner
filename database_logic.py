import csv

def import_data_from_database(file):
    data = []
    with open(file, 'r') as csvFile:
        fileRead = csv.reader(csvFile)
        for hash in fileRead:
            data.append(hash[0])
    csvFile.close()
    return data
