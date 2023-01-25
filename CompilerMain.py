import os
import sys

from jackParser import JackParser
from VmWriter import VmWriter
from XmlWriter import XmlWriter


def get_jack_file_list(file_path):
    files = []
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        jack_files = [file for file in files if file[-4:] == "jack"]
        files = [os.path.join(file_path, file) for file in jack_files]
    else:
        files.append(file_path)
    return files


def get_output_file_name(file_path, file):
    if os.path.isdir(file_path):
        return os.path.join(file_path, file[:-4])
    else:
        file_name = file_path[:-4]
        return file_name


def output_xml(output_file, class_element):
    with open(output_file, "w") as out_file:
        XmlWriter(out_file).write_tree(class_element)


def output_vm(output_file, class_element):
    with open(output_file, "w") as out_file:
        VmWriter(out_file).write_tree(class_element)


def main():
    file_path = sys.argv[1]
    files = get_jack_file_list(file_path)

    for file in files:
        output_file = get_output_file_name(file_path, file)
        class_element = JackParser(file).compile_class()
        output_xml(output_file + "xml", class_element)
        output_vm(output_file + "vm", class_element)


if __name__ == "__main__":
    main()
