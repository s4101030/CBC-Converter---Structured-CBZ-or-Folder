import zipfile
import argparse
import os
import sys
from pathlib import Path
import shutil

# Manga CBC Converter - Structured CBZ or Folder

parser = argparse.ArgumentParser(description="Structured CBZ or folder to indexed CBC converter")
parser.add_argument("file", type=str, help="File to read")
# parser.add_argument("-folder", help="Target is a folder instead of a zipped CBZ", action="store_true")
parser.add_argument("-delete", help="Delete original cbz file when done", action="store_true")
parser.add_argument("-omove", help="Move original cbz file when done", action="store_true")
parser.add_argument("-nmove", help="Move new cbc file when done", action="store_true")
args, unknown = parser.parse_known_args()

cbz_file_path = ''

if args.file:
    # print(args.file)
    cbz_file_path = args.file

file_drops = sys.argv[1:]

if file_drops:
	cbz_file_path = file_drops[0]

if cbz_file_path == '':
	print("ERROR: No cbz or folder given via commandline or drop - exiting")
	os._exit(0)

if not os.path.exists(cbz_file_path):
	print("ERROR: Given file or folder does not exist - exiting")
	os._exit(0)

if args.omove and args.delete:
	print("ERROR: Choose only one of delete and omove - exiting")
	os._exit(0)

folderMode = False

if not os.path.isfile(cbz_file_path): # Path(cbz_file_path).is_dir
	folderMode = True
	# print("FOLDER")
elif str(cbz_file_path).rsplit('.', 1)[1] == "cbz" or str(cbz_file_path).rsplit('.', 1)[1] == "CBZ":
	# print("CBZ")
	folderMode = False
else:
	print("ERROR: Invalid file/folder, expected .cbz or directory - exiting")
	os._exit(0)

print("Creating cbc for: " + cbz_file_path)

source_dir = 'Working'
original_dir = 'Done'
new_dir = 'Output'

if not os.path.exists(source_dir):
	os.makedirs(source_dir)

filefolders = list()

if folderMode: # args.folder
	for item in Path(cbz_file_path).iterdir():
		if item.is_dir():
			filefolders.append(item.name)
			filefolders = list(set(filefolders))
			filefolders.sort()

			shutil.copytree(cbz_file_path+'/'+item.name, source_dir+'/'+item.name)
	#print(folder_names)
else:
	with zipfile.ZipFile(cbz_file_path, 'r') as archive:
		file_list = archive.namelist()
		#print(file_list)
		filefolders = list()
		for filename in file_list:
			#print(filename.split('/')[0])
			filefolders.append(filename.rsplit('/', 1)[0])
		filefolders = list(set(filefolders))

		filefolders.sort()
		archive.extractall(source_dir)

if len(filefolders) == 0:
	print("ERROR: No folders inside to convert - exiting")
	os._exit(0)

folderno = 0
for folder in filefolders:
	archive_name = source_dir + '/' + folder + ".cbz"
	folder_to_zip = source_dir + '/' + folder
	folderno += 1

	print(f"Creating cbz {folderno}/{len(filefolders)}: {folder + ".cbz"}")

	with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
		for file_path in Path(folder_to_zip).rglob('*'):
			if file_path.is_file():
				arcname = file_path.relative_to(source_dir)
				zipf.write(file_path, arcname=arcname)
	shutil.rmtree(folder_to_zip)

print("Creating comics.txt")
with open(source_dir+"/comics.txt", "w", encoding='utf-8') as f:
	for folder in filefolders:
		f.write(folder + ".cbz:" + folder+'\n')

archive_name = str(cbz_file_path).rsplit('.', 1)[0] + ".cbc"
folder_to_zip = source_dir

print(f"Creating cbc: {archive_name}")
with zipfile.ZipFile(Path(archive_name), 'w', zipfile.ZIP_DEFLATED) as zipf:
	for file_path in Path(folder_to_zip).rglob('*'):
		if file_path.is_file():
			arcname = file_path.relative_to(source_dir)
			zipf.write(file_path, arcname=arcname)
print(f"Created cbc: {archive_name}")
shutil.rmtree(source_dir)

if args.delete:
	if os.path.exists(cbz_file_path):
		print("Deleting source file")
		if folderMode: # args.folder
			shutil.rmtree(cbz_file_path)
		else:
			os.remove(cbz_file_path)


if args.omove:
	if not os.path.exists(original_dir):
		os.makedirs(original_dir)
	print("Moving source file")
	shutil.move(cbz_file_path, original_dir+'/'+cbz_file_path)

if args.nmove:
	if not os.path.exists(new_dir):
		os.makedirs(new_dir)
	print("Moving created file")
	shutil.move(archive_name, new_dir+'/'+archive_name)
