import os
import re
import csv


def read_csv_data(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as opened_file:
        rows = csv.reader(opened_file, delimiter=',')
        return list(rows)


def save_new_csv_data(path_to_file, data_list):
    rows = [
        ['lastname', 'firstname', 'surname', 'organization',
         'position', 'phone', 'email']
    ]
    for dict_item in data_list:
        sub_list = list(dict_item.values())
        row = sub_list[:1][0]
        row.extend(sub_list[1:len(sub_list)])
        rows.append(row)
    with open(path_to_file, 'w', newline='', encoding='utf-8') as opened_file:
        writer = csv.writer(opened_file, delimiter=',')
        writer.writerows(rows)


def get_fio(text):
    res = re.findall('[А-Я][а-я]+', text)
    return res


def get_phone(text):
    if text != '':
        res_text = re.sub('[^\d]', '', text)
        res = re.findall("^\d{11}$", res_text)
        if res:
            res = res[0]
            return '+7({}){}-{}-{}'.format(res[1:4], res[4:7], res[7:9], res[9:11])
        else:
            res = re.findall("^\d{15}$", res_text)
            res = res[0]
            return '+7({}){}-{}-{} доб {}'.format(res[1:4], res[4:7], res[7:9], res[9:11], res[11:15])


if __name__ == '__main__':
    base_path = os.path.basename('.')
    path_to_data = os.path.join(base_path, 'data.csv')
    phone_data = read_csv_data(path_to_file=path_to_data)[1:]

    new_phone_data = {}

    for row in phone_data:

        fio_row_str = ' '.join(row[0:3])
        fio = get_fio(fio_row_str)
        lastname = fio[0]

        dict_item = {
            'ФИО': fio, 'Организация': row[3], 'Должность': row[4],
            'Телефон': get_phone(row[5]), 'Email': row[len(row)-1]
        }
        if not lastname in new_phone_data:
            new_phone_data[lastname] = dict_item
        else:
            for key, new_val in dict_item.items():
                old_val = new_phone_data[lastname][key]
                if len(str(old_val)) < len(str(new_val)):
                    new_phone_data[lastname][key] = new_val

    new_phone_data_list = list(new_phone_data.values())
    save_new_csv_data(
        os.path.join(base_path, 'phonebook.csv'), new_phone_data_list)
