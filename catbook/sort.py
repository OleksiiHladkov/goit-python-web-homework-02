from pathlib import Path
import os
import shutil
from glob import glob
import re
import sys


CATEGORIES = {"Audio": [".mp3", ".aiff", ".wav"],
              "Documents": [".docx", ".txt", ".pdf", ".xls", ".xlsx", ".doc", ".ppt", ".pptx"],
              "Images": [".jpg", ".jpeg", ".png"],
              "archives": [".zip", ".rar", ".gz", ".tar"],
              "Other":[]}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
BAD_SYMBOLS = ("%", "*", " ", "-")

TRANS = {}
 
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"
    
def normalize(name: str) -> str:
    return name.translate(TRANS)
 
    
def get_categories(path: Path) -> str: 
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"
           
def sort_folder(path: Path) -> None: 
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)
            
def move_file(path: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    
def delete_empty(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_empty(item)
            if not os.listdir(item):
                item.rmdir()
            
def unpack_archive(path: Path) -> None:
    archive_folder = "archives"
    for item in path.glob(f"{archive_folder}/*"):
        filename = item.stem
        arh_dir = path.joinpath(path / archive_folder / filename)
        if not arh_dir.exists():  
            arh_dir.mkdir()
            try:
                shutil.unpack_archive(item, arh_dir)
                item.unlink()
            except:
                continue
        else:
            return "Other"
    
def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} doesn't exists"
    
    sort_folder(path)
    unpack_archive(path)
    delete_empty(path)
    
    return "All ok"

if __name__ == "__main__":
    print(main())
    
    
    



   

        




