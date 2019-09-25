import os
import glob
import xml.dom.minidom
import sys
import re
import argparse

def convert_file_to_node(filename, base):
   if filename.lower().startswith(base.lower()):
      filename = filename[len(base):]
   if filename.lower().endswith(".vcxproj"):
      filename = filename[:-8]
   filename = re.sub('[^0-9a-zA-Z]+', '_', filename)
   if filename[0].isdigit():
      filename = '_' + filename
   return filename

# Check arguments
parser = argparse.ArgumentParser(description='Generate a dependency graph from Visual Studio solution.')
parser.add_argument('--path-root', help='Override file root path')
parser.add_argument('--path-include', help='Override file root path')
parser.add_argument('--output', help='Output graphviz dot file')
parser.add_argument('folder', action='store', default='graphviz.dot')
args = parser.parse_args()

final_folder = args.folder
final_root = args.path_root
final_include = args.path_include

if final_folder == None:
   print("You must specify the root folder of the project.")
   exit(1)

if final_root == None:
    final_root = final_folder

if final_include == None:
    final_include = final_folder

# Get all projects
files = [f for f in glob.glob(final_folder + "/**/*.vcxproj", recursive=True)]

A = {}

# Get all dependencies for all projects
for f in files:
   file = convert_file_to_node(f, final_root)
   A[file] = set()
   doc = xml.dom.minidom.parse(f);
   projectReference = doc.getElementsByTagName("ProjectReference")
   for projectDep in projectReference:
      for attrName, attrValue in projectDep.attributes.items():
         if attrName == "Include":
            file_inc = convert_file_to_node(attrValue, final_include)
            A[file].add(file_inc)

# Remove dependencies if a dependency depend on it.
i = 0
for project in A:
# For keep direct dependencies
   dependenciesChecked = set()
   dependenciesToRemove = set()
   for dep in A[project]:
# Find all project that depend on dep
      for project2 in A[dep]:
# First ignore project if already checked.
         if not project2 in dependenciesChecked:
            dependenciesChecked.add(project2)
# if a subproject already have project, remove project from dependencies.
            if project2 in A[project]:
               dependenciesToRemove.add(project2)
               i = i + 1
   for dep in dependenciesToRemove:
      A[project].remove(dep)


f = open(args.output,"w+")
f.write("digraph D {\n")
for project in A:
   for dep in A[project]:
      f.write(dep + "->" + project + "\n")
f.write("}\n")
f.close()
