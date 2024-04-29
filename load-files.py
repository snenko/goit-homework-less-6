import os
import sys
import shutil
import zipfile
import tarfile
import gzip
import shutil

base_folder_for_scan = ''

rools = {
    'images': {'JPEG', 'PNG', 'JPG', 'SVG'} ,
    'documents': {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'},
    'audio' : {'MP3', 'OGG', 'WAV', 'AMR'},
    'video' : {'AVI', 'MP4', 'MOV', 'MKV'},
    'archives' : {'ZIP', 'GZ', 'TAR'},
    'other' : {''}
}

def move_dir(filename, destination):
    global base_folder_for_scan

    if not os.path.exists(destination):
        os.makedirs(destination)

    try:
        shutil.move(filename, destination)
    except shutil.Error as e:
        e.errno
        print("Ділення на нуль!")

def get_file_extension(filename):
    _, extension = os.path.splitext(filename)

    extension = os.path.normpath(extension.upper())
    extension = extension[1:]

    return extension

def get_folder_by_file_type(file, extension):
    global rools

    for category, extensions in rools.items():
        if extension in extensions:
            return category

    return 'other'

def unpack_archive(file, extension):
    if(extension == 'ZIP'):
        return unpack_zip(file)
    elif(extension == 'TAR'):
        return unpack_tar(file)
    elif(extension == 'GZ'):
        return unpack_gz(file)
    return ''



def unpack_tar(file, destination):
    try:
        with tarfile.open(file, 'r') as tar_ref:
            tar_ref.extractall(destination)
    except zipfile.BadZipFile:
        print("Помилка! Невірний формат архіва. Файл пошкоджений.")
    except FileNotFoundError:
        print("Помилка! Файл не знайдений.")
    except Exception as e:
        print("Виникла помилка:", e)

def remove_file(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        print("Помилка: файл не знайдений")
    except PermissionError:
        print("Помилка: У вас немає дозволу на видалення файлу")
    except Exception as e:
        print("Відбулась помилка:", e)

def unpack_zip(file, destination):
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(destination)
    except zipfile.BadZipFile:
        print("Помилка! Невірний формат архіва. Файл пошкоджений.")
    except FileNotFoundError:
        print("Помилка! Файл не знайдений.")
    except Exception as e:
        print("Виникла помилка:", e)

def unpack_gz(file, destination):
    try:
        with gzip.open(file, 'rb') as gzip_file:
            with open(destination, 'wb') as extracted_file:
                shutil.copyfileobj(gzip_file, extracted_file)
    except zipfile.BadZipFile:
        print("Помилка! Невірний формат архіва. Файл пошкоджений.")
    except FileNotFoundError:
        print("Помилка! Файл не знайдений.")
    except Exception as e:
        print("Виникла помилка:", e)



def is_unavaliable_path(current_path, current_folder_name):
    global rools
    global base_folder_for_scan

    if base_folder_for_scan != current_path:
        return False

    if current_folder_name in rools.keys():
        return True
    
    return False

def get_base_folder_category(category):
    global base_folder_for_scan

    return f"{base_folder_for_scan}{category}/"

def scan_files(path):
    
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            if is_unavaliable_path(path, entry):
                continue
            else:
                if not os.listdir(full_path) == 0: 
                    shutil.rmtree(full_path)
                else:
                    scan_files(full_path)

        else:
            extension = get_file_extension(full_path)
            category = get_folder_by_file_type(full_path, extension)
            destination = get_base_folder_category(category)

            if(category == 'archives'):
                if extension == 'ZIP':
                    unpack_zip(full_path, destination)
                    remove_file(full_path)
                elif extension == 'TAR':
                    unpack_tar(full_path, destination)
                    remove_file(full_path)
                elif extension == 'GZ':
                    unpack_gz(full_path, destination)
                    remove_file(full_path)

            else:
                move_dir(full_path, destination)


def console_read_first_paremeter():
    if len(sys.argv) > 1:
        first_parameter = sys.argv[1]
        print("параметер:", first_parameter)
        return first_parameter
    
    print("відсутні аргументи")
    return ''



base_folder_for_scan = console_read_first_paremeter()

if os.path.exists(base_folder_for_scan) and os.path.isdir(base_folder_for_scan):
    scan_files(base_folder_for_scan)