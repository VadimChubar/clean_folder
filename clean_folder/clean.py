from pathlib import Path
import shutil
import sys
from clean_folder import file_processing
import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name
def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
def handle_archive(filename: Path, target_folder: Path):
    # Створюємо папку для архіву
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо папку куди розпакуємо архів
    # Беремо суфікс у файла і удаляємо replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    # Створюємо папку для архіву з іменем файлу
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'This doesn’t  archive: {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()
def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Error delete folder: {folder}')
def main():
    folder_for_scan = Path(sys.argv[1])
    print(f'Start in folder {folder_for_scan.resolve()}')
    file_processing.scan(folder_for_scan)
    for file in file_processing.IMAGES:
        handle_media(file, folder_for_scan / 'images')
    for file in file_processing.DOCUMENTS:
        handle_media(file, folder_for_scan / 'documents')
    for file in file_processing.AUDIO:
        handle_media(file, folder_for_scan / 'audio')
    for file in file_processing.VIDEO:
        handle_media(file, folder_for_scan / 'video')
    for file in file_processing.MY_OTHER:
        handle_other(file, folder_for_scan / 'my_other')
    for file in file_processing.ARCHIVES:
        handle_archive(file, folder_for_scan / 'archives')
    # Виконуємо реверс списку для того щоб видалити всі папки
    for folder in file_processing.FOLDERS[::-1]:
        handle_folder(folder)
# if __name__ == '__main__':
#     if sys.argv[1]:
#         folder_for_scan = Path(sys.argv[1])
#         print(f'Start in folder {folder_for_scan.resolve()}')
#         main(folder_for_scan.resolve())