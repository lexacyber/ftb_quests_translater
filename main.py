import os

from translatepy import Translator
import re
from pathlib import Path


translator = Translator()


def translate_to(string, lang_to):
    if string == '':
        return ''
    trans = re.sub(r'&([0-9]{1,3}|[a-z])', '^^*^^', string)
    tend = re.findall(r'&([0-9]{1,3}|[a-z])', string)
    trans = str(translator.translate(trans, f'{lang_to}')).replace('"',"''")
    for j in range(trans.count('^^*^^')):
        trans = trans.replace('^^*^^', '&' + tend[j], 1)
    return trans


def translate_line(i, file, translated_file, lang_to):
    # Check if line is an image-insertion
    if file[i].strip().startswith('"{'):
        translated_file.write(file[i])
        return i + 1

    indexes = [index for index, element in enumerate(file[i]) if element == '"']
    if len(indexes) < 2:
        translated_file.write(file[i])
        return i + 1

    string = translate_to(file[i][indexes[0] + 1:indexes[-1]], lang_to)
    translated_file.write(file[i][:indexes[0] + 1] + string + file[i][indexes[-1]:])
    return i + 1


def find_and_translate(file, translated_file, lang_to):
    file = file.readlines()
    line = 0
    total_lines = len(file)
    while line < total_lines:
        if line % 200 == 0:
            print(f"Progress: {line / total_lines * 100:.2f}%")
        if 'description: [' in file[line] and not ']' in file[line]:
            translated_file.write(file[line])
            line += 1
            while ']' not in file[line]:
                line = translate_line(line, file, translated_file, lang_to)
            translated_file.write(file[line])  # write the closing bracket line
            line += 1
        elif 'description: [' in file[line] and ']' in file[line]:
            line = translate_line(line, file, translated_file, lang_to)
        elif 'title:' in file[line]:
            line = translate_line(line, file, translated_file, lang_to)
        else:
            translated_file.write(file[line])
            line += 1


def main():
    target = input('Enter the path to the file folder (example: C:/.../quests/chapters)\n')
    lang_to = input('Enter into which language to translate using abbreviated or full names (example: ru or Russian): ')
    quest_path = Path(target)
    target_translated = target.replace('chapters', 'chapters-translate')
    if not (os.path.isdir(target_translated)):
        os.mkdir(target_translated)
    for input_path in quest_path.rglob("*.snbt"):
        file = open(f'{input_path}'.replace("\\", "/"), encoding='utf-8')
        translated_file = open(f'{input_path}'.replace('chapters', 'chapters-translate').replace("\\", "/", ), 'w',
                               encoding='utf-8')
        print(f'\tTranslating: {input_path}')
        find_and_translate(file, translated_file, lang_to)


if __name__ == '__main__':
    main()
