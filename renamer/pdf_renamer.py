from PIL import Image
from pdf2image import convert_from_path as conv
import pytesseract
import re
import sys
import os
import ctypes
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

osname = os.name
if osname == 'nt':
    ctypes.windll.kernel32.SetConsoleTitleW("AutoRename by Υπλγός (ΠΒ) Λόλας Ιωάννης")

# pdfs used in debugging
# pdfs = ['test.pdf','test1.pdf','test2.pdf','test3.pdf',
#        'test4.pdf','test5.pdf','test6.pdf','test7.pdf','test8.pdf']

''' Patterns to search: 
    pattern_f = arithmos fakelou
    pattern_s  = arithmos sxediou
    pattern_date = hmeromhnia '''

# the bellow regex doesn't work if ocr recognizes digits as chars
# pattern_f = re.compile('(Φ\.[1-9]{3}|Φ\.[0-9]{3}\.[0-9]{1,3})\s?/[0-9]*\s?/[0-9]*')
# this solves the above problem
pattern_f = re.compile('(Φ\..{3}|Φ\..{3}\..{1,3})\s?/.*\s?/.*')
# same with this on
# pattern_s = re.compile('Σ\.[0-9]*')
# bellow the solution
pattern_s = re.compile('Σ\..*')
pattern_date = re.compile(
    '[0-9]{1,2}\s*(Ιαν|Φεβ|Μαρ|Απρ|Μαι|Μαϊ|Ιουν|Ιούν|Ιουλ|Ιούλ|Αυγ|Σεπ|Οκτ|Νοε|Νοέ|Δεκ)\s*[0-9]{2,4}')

# Cannot use because we ocr a cropped image so theme is lost
# pattern_theme = re.compile('(?<=ΘΕΜΑ:)[\s\S]*(?=\s*ΣΧΕΤ)')
if osname == 'posix':
    mistakes = {'Ο': '0',
                'O': '0',
                'Δ': '4',
                'a': '',
                'ἂ': '',
                'Ί': '1'
                }
elif osname == 'nt':
    mistakes = {'Ο': '0',
                'O': '0',
                'Δ': '4',
                }


def pdftxt(pdf):
    # first page only dpi=278 (best for army docs maybe...)
    page = conv(pdf, 278, first_page=1, last_page=1)

    page[0].save('test.jpg', 'JPEG')

    # text = str(((pytesseract.image_to_string(Image.open('test.jpg'), lang='ell'))))

    text = str(((
        pytesseract.image_to_string(Image.open('test.jpg').crop(box=(1100, 200, 5000, 1800)),
                                    lang='ell+grc',
                                    config="--oem 6 ")
    )))

    fakelos = pattern_f.search(text)[0].replace(' ', '')
    # split fakelos to [fak1, fak2, fak3] to catch mistakes
    fak1, fak2, fak3 = fakelos.split('/')
    sxedio = pattern_s.search(text)[0].replace(' ', '').replace('/', '7')
    hmnia = pattern_date.search(text)[0].replace('/', '7')

    for mistake, fix in mistakes.items():
        fak1 = fak1.replace(mistake, fix)
        fak2 = fak2.replace(mistake, fix)
        fak3 = fak3.replace(mistake, fix)
        sxedio = sxedio.replace(mistake, fix)
        hmnia = hmnia.replace(mistake, fix)

    new_name = f"{fak1}/{fak2}/{fak3}a{sxedio}/{hmnia}.pdf".replace('/', '_').replace('a', '_')

    return new_name


# get directory from file explorer add final exe for :sendto
# directory = sys.argv[1]

directory = QFileDialog.getExistingDirectory()  # shows dialog box and return the path
#print(path)

def renamer(directory):
    # operate on every file under given directory
    total = 0
    actual = 0
    for root, dirs, files in os.walk(directory):
        for fname in files:
            if ".pdf" in fname:
                total += 1
                old_name = os.path.join(root, fname)
                new_name = old_name
                try:
                    new_name = os.path.join(root, pdftxt(old_name))
                except:
                    pass
                if new_name != old_name:
                    try:
                        os.rename(old_name, new_name)
                        actual += 1
                        print(f"{fname} ==> {new_name}     {actual}/{total}")
                    except:
                        pass
                else:
                    print(f"No change for {old_name}     {actual}/{total}")


renamer(directory)