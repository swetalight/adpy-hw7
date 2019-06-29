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
        res = re.findall('[+]?\d+', text)
        phone_buf = ''.join(res)
        if phone_buf.startswith('8'):
            phone_buf = '+7' + phone_buf[1:]
        if len(phone_buf) < 12:
            phone_buf = '+7' + phone_buf
        phone = ''.join([
            phone_buf[:2], '(', phone_buf[2:5], ')', phone_buf[5:8],
            '-', phone_buf[8:10], '-', phone_buf[10:12]
        ])
        if len(phone_buf) > 12:
            return ' '.join([phone, 'доб', phone_buf[12:len(phone_buf)]])
        return phone
    return ''


if __name__ == '__main__':
    base_path = os.path.basename('.')
    path_to_data = os.path.join(base_path, 'data.csv')
    phone_data = read_csv_data(path_to_file=path_to_data)

    new_phone_data = {}

    for i, row in enumerate(phone_data):
        if i > 0:
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
                    if len(old_val) < len(new_val):
                        new_phone_data[lastname][key] = new_val

    new_phone_data_list = list(new_phone_data.values())
    save_new_csv_data(
        os.path.join(base_path, 'phonebook.csv'), new_phone_data_list)
