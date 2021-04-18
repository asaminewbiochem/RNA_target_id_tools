
from pathlib import Path

p = Path('.')

print("All files and dfolders in current direcotry:")


all_items = [x for x in p.iterdir()]
for a in all_items:
    print(a)


# files in current folder
print('\n')
print('Files in current folders:')
files = [x for x in p.iterdir() if x.is_file()]
for f in files:
    print(f)

directory = [x for x in p.iterdir() if x.is_dir()]
# directories in current folder
print('\n')
print('direcotries in current folder:')
for d in directory:
    print(d)
