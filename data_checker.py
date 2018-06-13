import csv
from os import listdir
from os.path import isfile, join

path = 'data'


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
            start_saving = 0
            errors = {"unformed header":[],"empty line": [], "multiple lines": [], "missing column": [], "strange rssi": [],
                      "strange saved data": [], "unknown strange line": []}
            for row in reader:
                row_num += 1
                if len(row) == 0:
                    errors["empty line"].append(row_num)
                elif len(row) == 1:
                    if row[0] == "start saving":
                        start_saving = row_num
                    elif row[0] == "end saving":
                        saved_data = row_num - start_saving
                        if saved_data != 500:
                            errors["strange saved data"].append(saved_data)
                    else:
                        errors["unknown strange line"].append(row_num)
                elif 1 < len(row) < 7:
                    errors["missing column"].append(row_num)
                elif len(row) > 7:
                    errors["multiple lines"].append(row_num)
                else:
                    if int(row[-1]) < -100 or int(row[-1]) > 0:
                        errors["strange rssi"].append(row_num)
            msg = ''
            for key, value in errors.items():
                if len(value) == 0:
                    continue
                else:
                    msg = msg + '%s:%s' % (key, value)
            if msg != '':
                print("[%s] %s" % (file, msg))
