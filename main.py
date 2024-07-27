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
    trans = str(translator.translate(trans, f'{lang_to}'))
    for j in range(trans.count('^^*^^')):
        trans = trans.replace('^^*^^', '&'+tend[j], 1)
    return trans


def multiline_translate(i, file, translated_file, lang_to):
    translated_file.write(file[i])
    i += 1
    while not (']' in file[i]):
        if '""' in file[i]:
            translated_file.write(file[i])
            i += 1
        else:
            indexes = [index for index, element in enumerate(file[i]) if element == '"']
            s = translate_to(file[i][indexes[0] + 1:indexes[-1]], lang_to)
            translated_file.write(file[i][:indexes[0] + 1] + s + file[i][indexes[-1]:])
            i += 1
    return i


def oneline_translate(i, file, translated_file, lang_to):
    indexes = [index for index, element in enumerate(file[i]) if element == '"']
    s = translate_to(file[i][indexes[0] + 1: indexes[-1]], lang_to)
    translated_file.write(file[i][:indexes[0] + 1] + s + file[i][indexes[-1]:])


def find_and_translate(file, translated_file, lang_to):
    file = file.readlines()
    i = 0
    while i < len(file):
        if 'description: [' in file[i] and not (']' in file[i]):
            i = multiline_translate(i, file, translated_file, lang_to)
        elif 'description: [' in file[i] and ']' in file[i]:
            oneline_translate(i, file, translated_file, lang_to)
            i += 1
        elif 'title:' in file[i]:
            oneline_translate(i, file, translated_file, lang_to)
            i += 1
        else:
            translated_file.write(file[i])
            i += 1


def main():
    target = input('Enter the path to the file folder (example: C:/.../quests/chapters)')
    lang_to = input('Enter into which language to translate using abbreviated or full names (example: ru or Russian)')
    quest_path = Path(target)
    target_translated = target.replace('chapters', 'chapters-translate')
    if not (os.path.isdir(target_translated)):
        os.mkdir(target_translated)
    for input_path in quest_path.rglob("*.snbt"):
        file = open(f'{input_path}'.replace("\\", "/"), encoding='utf-8')
        translated_file = open(f'{input_path}'.replace('chapters', 'chapters-translate').replace("\\", "/",), 'w', encoding='utf-8')
        print(f'\tTranslating: {input_path}')
        find_and_translate(file, translated_file, lang_to)


if __name__ == '__main__':
    main()
