#!/usr/bin/env python
import sys,os
import argparse
import glob
import subprocess


    
    
parser = argparse.ArgumentParser(description = "Hadd files in a directory (in batches if wanted)")
parser.add_argument("-directory",type=str,help="Directory files are in")
parser.add_argument("-nFiles",type=int,help="how many files to hadd at a time",default = 0)
parser.add_argument("-out",type=str,help="outfile",default = "out.root")
args = parser.parse_args()
print args.directory


def hadd(out,infiles):
    cmd=["hadd",out,infiles]
    subprocess.call(cmd)



files = glob.glob(args.directory+"/*")
newfiles = []
for f in files: 
  if "root" in f: 
    newfiles.append(f)
print newfiles
# newfiles = set(newfiles)
noPasses = -1
if args.nFiles != -1:
  noPasses = int(len(newfiles)/args.nFiles)
print noPasses

for i in range(len(newfiles)):
  if len(newfiles) < i*noPasses: continue
  thisPass = newfiles[i*noPasses:noPasses*(1+i)]
  print thisPass
  string = ""
  for thing in thisPass: string += (thing+" ")
  hadd("%d_%s"%(i,args.out), "%s"%(string))
  print "hadd %d_%s %s"%(i,args.out,string)
  
  
  
  


