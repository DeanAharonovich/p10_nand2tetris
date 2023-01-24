import os
import sys
import re
from xml.etree import ElementTree

from CompilationEngine import CompilationEngine
from vmWriter import vmWriter


def get_jack_file_list(file_path):
    files = []
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        jack_files = [file for file in files if file[-4:] == "jack"]
        files = ["{}/{}".format(file_path, file) for file in jack_files] # os.path.join(file_path, file)
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
        tree = ElementTree.ElementTree(class_element)
        ElementTree.indent(tree, '  ')
        xmlstr = ElementTree.tostring(class_element, encoding='utf8', method='html').decode("utf8")
        xmlstr = xmlstr.replace("></", ">\n</")
        out_file.write(xmlstr)


def output_vm(output_file, class_element):
    with open(output_file, "w") as out_file:
        vmWriter(out_file).write_tree(class_element)


def main():
    file_path = sys.argv[1]
    files = get_jack_file_list(file_path)

    for file in files:
        output_file = get_output_file_name(file_path, file)
        class_element = CompilationEngine(file).compile_class()
        output_xml(output_file + "p11_xml", class_element)
        output_vm(output_file + "p11_vm", class_element)


if __name__ == "__main__":
    main()
