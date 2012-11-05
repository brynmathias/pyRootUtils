#!/usr/bin/env python

import glob
import threading
import subprocess
import argparse
import errno
import os


def ensure_dir(path):
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST:
        pass
      else: raise

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def haddF(ofName = None, ifList = [] ):
    "hadd a list of files, will be dumped in to a thread"
    ifStr = " "
    for f in ifList: ifStr+="%s "%(f)    
    cmd = ["hadd "+ofName+ ifStr]
    subprocess.call(cmd,shell=True)


    
    
    
def getList(path = None):
    l = glob.glob(path+"/*.root")
    return l
    



def main():
    """docstring for main"""
    
    parser = argparse.ArgumentParser(description="Multi threaded hadd.")
    parser.add_argument("--input",type = str,dest='inputFile')
    parser.add_argument("--nThreads",type = int,dest="nThreads",default=5)
    args = parser.parse_args()
    if args.inputFile[-1]=="/":args.inputFile= args.inputFile[:-1]
    if args.inputFile[1]=="/":args.inputFile= args.inputFile[1:]
     tmpDir = "./tmp_%s/"%(args.inputFile)
    print tmpDir
    ensure_dir(tmpDir)
    Threads = []
    listOfFiles = getList(path=args.inputFile)
    jList = chunks(listOfFiles,args.nThreads)
    for i,c in enumerate(jList):
        Threads.append(threading.Thread(group = None, target = haddF,args=(tmpDir+args.inputFile[:-1]+"_part%i.root"%(i),c)))
    for t in Threads:
        t.start()
    for t in Threads:
        t.join()
    
    
    partList = getList(tmpDir)
    haddF("./"+args.inputFile+".root",partList)










if __name__ == "__main__":
    main()




