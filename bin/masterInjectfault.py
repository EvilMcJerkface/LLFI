#! /usr/bin/env python3

"""

%(prog)s takes a fault injection executable and executes it

Usage: %(prog)s <fault injection executable> <the same options that you use to run the excutable before>

       %(prog)s --help(-h): show help information

Prerequisite:
1. You need to be at the parent directory of the <fault injection executable> to invoke %(prog)s. This is to make it easier for LLFI to track the outputs generated by <fault injection executable>
2. (prog)s only checks recursively at the current directory for possible outputs, if your output is not under current directory, you need to store that output by yourself
3. You need to put your input files (if any) under current directory
4. You need to have 'input.yaml' under your current directory, which contains appropriate options for LLFI.
"""

# This script injects faults the program and produces output
# This script should be run after the profiling step

import sys, os, subprocess
import yaml
import time
import random
import shutil

script_path = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(script_path, '../config'))
import llvm_paths

injectfaultPath = os.path.join(llvm_paths.LLVM_DST_ROOT, "../llfi/bin/injectfault")

env=sys.argv[1]
prog = os.path.basename(sys.argv[2])
basename= os.path.splitext(prog)[0]
basedir = os.getcwd()
basedirfolder = basename.split("-")[0]
GUIyaml = basedir+"/"+basedirfolder+"/Multiple-Failure-Modes/input.yaml"
GUIMFM = basedir+"/"+basedirfolder+"/Multiple-Failure-Modes"
GUIMFMdir = basedir+"/"+basedirfolder+"/"

def UpdateInputYaml():
  global i , size, env 
  if env =="--CLI":
    f = open("input.yaml", "r")
  elif env== "--GUI":
    os.chdir(GUIMFM)
    f = open("input.yaml", "r")
       
  
  master=list(f)
  k=master.index('runOption:\n')
  tail= master [k:]
  f.close()
  howmanymodes()
  for i in range(0, num):
    path= "../MFM%s" %i
    os.chdir(path)
    f = open("input.yaml", "r")
    slave=list(f)
    slave.extend(tail) 
   
# write to each child yaml
    with open('input.yaml' , mode='wt', encoding='utf-8') as myfile:
      for lines in slave:
        print(lines, file = myfile)
      myfile.close 
################################################################################ 
def howmanymodes():
  global num
  f = open("input.yaml", "r")
  master=list(f)
  m=master.index('          include:\n')
  n=master.index('    regSelMethod: customregselector\n')
  MFM=master[m+1:n]
  num= len(MFM)
  for i in range (0,num):
    if MFM[i]== '\n':
      num=num-1
    
  ################################################################################
def callinjectfault():
  if env =="--CLI":
    for i in range (0,num):
      path= "../MFM%s" %i
      os.chdir(path)
      args_num= len(sys.argv)
      result = subprocess.check_output([injectfaultPath] + sys.argv[1:])
      print ("Current path is:", path)
      print (str(result, encoding='UTF-8'))
  elif env== "--GUI":
    for i in range (0,num):
      path= GUIMFMdir+"MFM%s" %i
      os.chdir(path)
      tmp = os.getcwd()
      args_num= len(sys.argv)
      result = subprocess.check_output([injectfaultPath, '--CLI','llfi/%s.exe' %basename] + sys.argv[3:])
      
      print ("Current path is:", path)
      print (str(result, encoding='UTF-8'))
     # newpath= '../'
     # os.chdir(newpath)





################################################################################
def main(argv):
  UpdateInputYaml()
  callinjectfault()

################################################################################

if __name__=="__main__":
  if len(sys.argv) == 1:
    usage('Must provide the fault injection executable and its options')
    exit(1)
  main(sys.argv[1:])