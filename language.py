#!/usr/bin/env python2.7

import os
import sys
import subprocess
#import findimports
def usage(exit_code=0):
    print '''Usage: {} [filename]'''.format(os.path.basename(sys.argv[0]))
    sys.exit(exit_code)


# FUNCTION THAT CREATES PACKAGE FOR PYTHON SCRIPTS
def python(lines):
    package = []
    newFile = open('package.txt', 'w')
    print>>newFile, '#!/usr/bin/env python'
    for line in lines:
        if line.startswith('import'):
            package.append(line.split()[1])
      
    for item in package:
        print>>newFile, 'import {}'.format(item)


    print ' '.join(package)
    print 'python'

# Parse command line arguments
args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-h':
        usage(0)
    else:
        usage(1)

# Open file and read lines of it
if '.py' in args[0]:
    f = open(args[0])
    lines = f.readlines()
    # if the first line is a shebang to python, print python
    if lines[0].find('python') != -1:
        python(lines)
        sys.exit(0)
else:
    f = subprocess.Popen(["ldd  -v " + args[0]], stdout=subprocess.PIPE, shell=True)
    (out, err) = f.communicate()
    if 'c++' in out:
        print 'c++ executable'
    print 'ldd output: {}'.format(out)
    print type(f)
    #f = os.system('ldd -v ' + args[0])
    #if 'c++' in f:
    #  print 'c++'
    print type(f)
    #lines = f.readlines()
    #for line in lines:
     #  for word in line.split():
    #    if 'gnu' in word:
    #      print line
