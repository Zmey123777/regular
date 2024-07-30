import csv
import re
from pprint import pprint
from collections import defaultdict
import os

# Функция для форматирования телефонных номеров при помощи regex
def format_phone(phone):
    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(.*)")
    match = pattern.match(phone)
    if not match:
        return phone
    formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(6):
        ext = re.search(r"доб\.?\s*(\d+)", match.group(6))
        if ext:
            formatted_phone += f" доб.{ext.group(1)}"
    return formatted_phone

# Функция для форматирвоания ФИО
def split_name(fullname):
    parts = fullname.strip().split()
    if len(parts) == 3:
        return parts
    elif len(parts) == 2:
        return parts + [""]
    return [parts[0], "", ""]

# Функция для мерджа по ФИО
def merge_records(contacts):
    merged_contacts = defaultdict(lambda: ["", "", "", "", "", "", ""])
    for contact in contacts:
        lastname, firstname, surname = contact[:3]
        key = f"{lastname} {firstname}"
        for i, value in enumerate(contact):
            if value:
                merged_contacts[key][i] = value
    return list(merged_contacts.values())

if __name__ == "__main__":
    # Читаем csv файл
    file_path = os.path.join(os.getcwd(), 'phonebook_raw.csv')
    with open(file_path, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # Вызываем форматирование контактов
    processed_contacts = []
    for contact in contacts_list[1:]:
        fullname = " ".join(contact[:3])
        lastname, firstname, surname = split_name(fullname)
        contact[0], contact[1], contact[2] = lastname, firstname, surname
        contact[5] = format_phone(contact[5])
        processed_contacts.append(contact)

    # Вызываем функцию и мерджим одинаковые ФИО
    merged_contacts = merge_records(processed_contacts)

    header = contacts_list[0]
    merged_contacts.insert(0, header)

    # Сохраняем результат в файл
    output_file_path = os.path.join(os.getcwd(), 'phonebook.csv')
    with open(output_file_path, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(merged_contacts)

    pprint(merged_contacts)
