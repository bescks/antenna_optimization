import csv
from os import listdir
from os.path import isfile, join

path = '/Users/gengdongjie/WorkSpace/Bitbucket/optimization_antenna/data_new'


def get_all_files(path):
    files = []
    for file in listdir(path):
        if isfile(join(path, file)):
            files.append(join(path, file))
        else:
            files = files + get_all_files(join(path, file))
    return files


for file in get_all_files(path):
    if file.endswith('.csv'):
        with open(file)  as f:
            reader = csv.reader(f)
            header = next(reader)
            row_num = 1
            for row in reader:
                row_num += 1
                if len(row) != 6:

                    print(len(row))
                    print("multiple lines in [%s], row [%s]" % (file, row_num))
