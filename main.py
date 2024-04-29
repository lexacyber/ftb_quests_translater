import os

from translatepy import Translator
import re
from pathlib import Path


translator = Translator()


def translateto(s, lang_to):
    trans = re.sub(r'&([0-9]{1,3}|[a-z])', '^^*^^', s)
    tend = re.findall(r'&([0-9]{1,3}|[a-z])', s)
    trans = str(translator.translate(trans, f'{lang_to}'))
    for j in range(trans.count('^^*^^')):
        trans = trans.replace('^^*^^', '&'+tend[j], 1)
    return trans


def manylines_translate(i, f, a, lang_to):
    a.write(f[i])
    i += 1
    while not (']' in f[i]):
        if '""' in f[i]:
            a.write(f[i])
            i += 1
        else:
            indexes = [index for index, element in enumerate(f[i]) if element == '"']
            s = translateto(f[i][indexes[0]+1:indexes[-1]], lang_to)
            a.write(f[i][:indexes[0]+1] + s + f[i][indexes[-1]:])
            i += 1
    return i


def oneline_translate(i, f, a, lang_to):
    indexes = [index for index, element in enumerate(f[i]) if element == '"']
    s = translateto(f[i][indexes[0] + 1: indexes[-1]], lang_to)
    a.write(f[i][:indexes[0] + 1] + s + f[i][indexes[-1]:])


def notranslate(i, f, a):
    a.write(f[i])


def find_and_translate(f, a, lang_to):
    f = f.readlines()
    i = 0
    while i < len(f):
        if 'description: [' in f[i] and not (']' in f[i]):
            i = manylines_translate(i, f, a, lang_to)
        elif 'description: [' in f[i] and ']' in f[i]:
            oneline_translate(i, f, a, lang_to)
            i += 1
        elif 'title:' in f[i]:
            oneline_translate(i, f, a, lang_to)
            i += 1
        else:
            notranslate(i, f, a)
            i += 1


def main():
    target = input('Enter the path to the file folder (for example: C:/.../quests/charapters)')
    lang_to = input('enter into which language to translate using abbreviated or full names(for example: ru or Russian)')
    quest_path = Path(target)
    target2 = target.replace('chapters', 'chapters-translate')
    if not (os.path.isdir(target2)):
        os.mkdir(target2)
    for input_path in quest_path.rglob("*.snbt"):
        f = open(f'{input_path}'.replace("\\", "/"), encoding='utf-8')
        a = open(f'{input_path}'.replace('chapters', 'chapters-translate').replace("\\", "/",), 'w', encoding='utf-8')
        print(f' Translating - {input_path}')
        find_and_translate(f, a, lang_to)


if __name__ == '__main__':
    main()
