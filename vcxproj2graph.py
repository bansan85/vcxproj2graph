import os
import glob
import xml.dom.minidom

# Get all projects
files = [f for f in glob.glob("C:\\Sources\\Nagoya\\output\\Washington8x9BackEnd\\build\\" + "**\\*.vcxproj", recursive=True)]

#A = dict([("sape", set()), ("guido", set()), ("jack", set())])
A = {}

print(A)

# Get all dependencies for all projects
for f in files:
   file = f
   A[file] = set()
   doc = xml.dom.minidom.parse(f);
   projectReference = doc.getElementsByTagName("ProjectReference")
   for projectDep in projectReference:
      for attrName, attrValue in projectDep.attributes.items():
         if attrName == "Include":
            A[file].add(attrValue)

# Remove dependencies if a dependancie depend on it.
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
print (i)


f = open("graphivz.txt","w+")
f.write("digraph D {\r\n")
for project in A:
   for dep in A[project]:
      f.write(dep + "->" + project + "\r\n")
f.write("}\r\n")
f.close()
