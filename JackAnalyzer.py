import os
import sys

from CompilationEngine import CompilationEngine
from JackTokenaizer import JackTokenaizer


def get_jack_file_list(file_path):
    files = []
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        vm_files = [file for file in files if file[-4:] == "jack"]
        files = [os.path.join(file_path, file) for file in vm_files]
    else:
        files.append(file_path)
    return files


def get_output_file_name(file_path, file):
    if os.path.isdir(file_path):
        return os.path.join(file_path, file[:-4]) + "xml"
    else:
        file_name = file_path[:-2]
        return file_name + "xml"


def main():
    file_path = sys.argv[1]
    files = get_jack_file_list(file_path)

    for file in files:
        output_file = get_output_file_name(file_path, file)
        with open(output_file, "w") as out_file:
            xml = CompilationEngine(file).compile_class()
            out_file.write(xml)

        

if __name__ == "__main__":
    main()
