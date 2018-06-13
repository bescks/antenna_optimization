import csv
from os import listdir
from os.path import isfile, join

path = 'data'
exclude = ['old']


def get_all_files(path=path, exclude=[]):
    files = []
    for file in listdir(path):
        if file in exclude:
            continue
        if isfile(join(path, file)):
            files.append(join(path, file))
        else:
            files = files + get_all_files(join(path, file))
    return files


all_files = sorted(get_all_files(path, exclude))
for file in all_files:
    if file.endswith('.csv'):
        with open(file) as f:
            reader = csv.reader(f)
            header = next(reader)
            row_num = 1
            start_saving = 0
            errors = {
                "strange header": [],
                "empty line": [],
                "multiple lines": [],
                "missing column": [],
                "strange rssi": [],
                "strange saved data": [],
                "unknown strange line": []}
            if len(header) != 8:
                errors['strange header'].append(len(header))
            for row in reader:
                row_num += 1
                if len(row) == 0:
                    errors["empty line"].append(row_num)
                elif len(row) == 1:
                    if row[0] == "start saving":
                        start_saving = row_num
                    elif row[0] == "end saving":
                        saved_data = row_num - start_saving - 1
                        if saved_data != 500:
                            errors["strange saved data"].append(saved_data)
                    else:
                        errors["unknown strange line"].append(row_num)
                elif 1 < len(row) < 7:
                    errors["missing column"].append(row_num)
                elif len(row) > 7:
                    errors["multiple lines"].append(row_num)
                else:
                    if int(row[-1]) < -105 or int(row[-1]) > 0:
                        errors["strange rssi"].append(row_num)
            msg = ''
            # if file is not raw data, row_num should be 501
            if start_saving == 0 and row_num != 501:
                errors['strange saved data'].append(row_num)
            for key, value in errors.items():
                if len(value) == 0:
                    continue
                else:
                    msg = msg + '%s:%s' % (key, value)
            if msg != '':
                print("[%s] %s" % (file, msg))
