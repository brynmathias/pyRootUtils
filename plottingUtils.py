#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Bryn Mathias on 2011-09-30.
Copyright (c) 2011 Imperial College. All rights reserved.
"""

import sys
import os
import unittest
import ROOT as r

#!/usr/bin/env python

'''Created by Bryn Mathias
bryn.mathias@cern.ch
'''
import errno

import ROOT as r
import math
from time import strftime
import os, commands
import array
def ensure_dir(path):
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST:
        pass
      else: raise

# r.gROOT.SetStyle("Plain") #To set plain bkgds for slides
r.gStyle.SetTitleBorderSize(0)
r.gStyle.SetCanvasBorderMode(0)
r.gStyle.SetCanvasColor(0)#Sets canvas colour white
r.gStyle.SetOptStat(1110)#set no title on Stat box
r.gStyle.SetLabelOffset(0.001)
r.gStyle.SetLabelSize(0.003)
r.gStyle.SetLabelSize(0.005,"Y")#Y axis
r.gStyle.SetLabelSize(0.1,"X")#Y axis
r.gStyle.SetTitleSize(0.06)
r.gStyle.SetTitleW(0.7)
r.gStyle.SetTitleH(0.07)
r.gStyle.SetOptTitle(1)
r.gStyle.SetOptStat(0)
r.gStyle.SetOptFit(1)
r.gStyle.SetAxisColor(1, "XYZ");
r.gStyle.SetStripDecimals(r.kTRUE);
r.gStyle.SetTickLength(0.03, "XYZ");
r.gStyle.SetNdivisions(510, "XYZ");
r.gStyle.SetPadTickX(1);
r.gStyle.SetPadTickY(1);
r.gStyle.SetLabelColor(1, "XYZ");
r.gStyle.SetLabelFont(42, "XYZ");
r.gStyle.SetLabelOffset(0.01, "XYZ");
r.gStyle.SetLabelSize(0.05, "XYZ");
r.gStyle.SetHatchesLineWidth(2)
# from PlottingFunctions import *
# r.gROOT.SetBatch(True) # suppress the creation of canvases on the screen.. much much faster if over a remote connection
# r.gROOT.SetStyle("Plain") #To set plain bkgds for slides
# r.gROOT.ProcessLine(".L ./Jets30/tdrstyle.C+")
r.gStyle.SetPalette(1)

def SetBatch():
  """docstring for SetBatch"""
  return r.gROOT.SetBatch(True)

class GetSumHist(object):
  def __init__(self, File = None, Directories = None, Hist = None, Col = r.kBlack, Norm = None, LegendText = None):
    super(GetSumHist, self).__init__()
    object.__init__(self)
    self.files = File
    self.directories = Directories
    self.hist = Hist
    self.col = Col
    self.norm = Norm
    self.legendText = LegendText
    self.isData = False
    self.hObj = None
    self.returnHist()
  """docstring for GetSumHist"""
  def returnHist(self):
    """docstring for returnHist"""
    if self.files is None: return self.hObj
    for f in self.files:
      a = r.TFile.Open(f)
      # Get The first hist in the list and clone it.
      for Dir in self.directories:
        hf = a.Get(Dir)
        if not hf: print "Subdirectory %s does not exist"%(Dir)
        h = hf.Get(self.hist)
        if self.hObj is None:
          self.hObj = h.Clone()
        else: self.hObj.Add(h)
        # Set Colours
    self.hObj.SetLineColor(self.col)
    self.hObj.SetMarkerColor(self.col)
    # Set the last bin to show how many events in the over flow as well
    if self.norm is not None:
      self.hObj.Scale(self.norm/100.)
    return self.hObj

  def HideOverFlow(self):
    """docstring for HideOverFlow"""
    self.hObj.SetBinContent(self.hObj.GetNbinsX() ,self.hObj.GetBinContent(self.hObj.GetNbinsX())+self.hObj.GetBinContent(self.hObj.GetNbinsX()+1))
    self.hObj.SetBinError(self.hObj.GetNbinsX() ,math.sqrt((self.hObj.GetBinError(self.hObj.GetNbinsX()))**2 + (self.hObj.GetBinError(self.hObj.GetNbinsX()+1))**2))
    self.hObj.SetBinContent(self.hObj.GetNbinsX()+1,0)

  def Draw(self,options):
    """docstring for Draw"""
    self.hObj.Draw(options)

  def SetRange(self,axis,axis1,axis2):
    """docstring for SetRange"""
    if axis is "x": self.hObj.GetXaxis().SetRangeUser(axis1,axis2)
    if axis is "y": self.hObj.GetYaxis().SetRangeUser(axis1,axis2)
    pass



  def Integral(self,val1,val2):
    """docstring for Integral"""
    bin1 = self.hObj.FindBin(val1)
    bin2 = self.hObj.FindBin(val2)
    return self.hObj.Integral(bin1,bin2)
    pass

  def Rebin(self,nbins,binList):
    """docstring for Rebin"""
    bins = array.array('d',binList)
    tmp = self.hObj.Rebin(nbins,"tmp",bins)
    self.hObj = tmp

  def Help(self):
    print "====================================================================================================================="
    print "Usage is GetSumHist(File = None, Directories = None, Hist = None, Col = r.kBlack, Norm = None, LegendText = None)"
    print "Methods are:"
    print "\t HideOverFlow() -- Adds the over flow bin to the last bin of the histogram and computes errors for this bin"
    print "\t SetRange(\'axis\',start,end)"
    print "\t Draw() -- Use ROOT's draw method, has to wrap classInstance.hObj.Draw()"
    print "====================================================================================================================="



class printPDF(object):
  """docstring for printPDF"""
  def __init__(self, Fname):
    super(printPDF, self).__init__()
    self.canvas = r.TCanvas()
    self.fname = Fname
    self.pageCounter = 1


  def cd(self):
    """docstring for cd"""
    self.canvas.cd()
    pass

  def open(self):
    """docstring for open"""
    self.canvas.Print(self.fname+"[")
    pass


  def close(self):
    """docstring for close"""
    self.canvas.Print(self.fname+"]")
    pass


  def Clear(self):
    """docstring for Clear"""
    self.canvas.Clear()
    pass

  def SetLog(self,axis,BOOL):
    """docstring for SetLog"""
    if axis == 'x':
      if BOOL:
        self.canvas.SetLogx()
      else:
        self.canvas.SetLogx(r.kFALSE)
    if axis == 'y':
      if BOOL:
        self.canvas.SetLogy()
      else:
        self.canvas.SetLogy(r.kFALSE)
    pass


  def Print(self):
    """docstring for Print"""
    num = r.TLatex(0.95,0.01,"%d"%(self.pageCounter))
    num.SetNDC()
    num.Draw("same")
    self.canvas.Print(self.fname)
    self.pageCounter += 1
    pass


class TurnOn(object):
  """docstring for TurnOn"""
  def __init__(self, Numerator, Denominator):
    self.nom = Numerator
    self.denom = Denominator
    self.Title = None
    self.xaxisTitle = None
    self.yaxisTitle = None
    self.TGraph = r.TGraphAsymmErrors()
    self.xmin = None
    self.ymin = -0.2
    self.xmax = None
    self.ymax = 1.2
    self.nomClone  = None
    self.denomClone = None
    self.newBins = None
    self.text90 = None
    self.text95 = None
    self.text99 = None


  def setRange(self,x1,x2):
    """docstring for SetRange"""
    self.xmin = x1
    self.xmax = x2
    pass

  def DifferentialTurnOn(self):
    """docstring for DifferentialTurnOn"""
    self.TGraph.Divide(self.nom.hObj,self.denom.hObj)
    self.TGraph.GetXaxis().SetTitle(self.nom.hObj.GetXaxis().GetTitle())
    self.TGraph.GetXaxis().SetTitleSize(0.05)
    self.TGraph.GetYaxis().SetTitle("Efficiency")
    self.TGraph.GetXaxis().SetRangeUser(self.xmin,self.xmax)
    self.TGraph.GetYaxis().SetRangeUser(self.ymin,self.ymax)
    self.TGraph.SetTitle("Differential turn on for %s, from file: %s"%(self.nom.directories,self.nom.files))
    return self.TGraph

  def CumulativeTurnOn(self,Bins):
    """docstring for CumulativeTurnOn"""
    self.TGraph = r.TGraphAsymmErrors()
    self.newBins = array.array('d',Bins)
    self.nomClone  = self.nom
    self.denomClone = self.denom
    self.nomClone.Rebin(  len(Bins)-1, self.newBins)
    self.denomClone.Rebin(len(Bins)-1, self.newBins)
    self.TGraph.Divide(self.nomClone.hObj,self.denomClone.hObj)
    yval = r.Double(0)
    xval = r.Double(0)
    self.TGraph.GetPoint(1,xval,yval)
    self.TGraph.SetTitle("Cumulative turn on for above plot, with a cut of %f, Efficiency is %f + %f - %f"%(Bins[1],yval,self.TGraph.GetErrorYhigh(1),self.TGraph.GetErrorYlow(1)))
    self.TGraph.GetYaxis().SetRangeUser(self.ymin,self.ymax)
    return self.TGraph

  def logEffs(self):
    """docstring for logEffs"""
    yval = r.Double(0)
    xval = r.Double(0)
    self.text90 = r.TLatex(0.01,0.75,"")
    self.text95 = r.TLatex(0.01,0.80,"")
    self.text99 =  r.TLatex(0.01,0.80,"")
    maxBinEdge = self.nom.hObj.GetBinLowEdge(self.nom.hObj.GetNbinsX())
    for bin in range(1,self.nom.hObj.GetNbinsX()):
      TGraph = r.TGraphAsymmErrors()
      newBinEdge = self.nom.hObj.GetBinWidth(bin) * bin
      nomClone = self.nom.hObj.Rebin(2,"nomClone",array.array('d',[0.,newBinEdge,maxBinEdge]))
      denomClone = self.denom.hObj.Rebin(2,"denomClone",array.array('d',[0.,newBinEdge,maxBinEdge]))
      TGraph.Divide(nomClone,denomClone)
      TGraph.GetPoint(1,xval,yval)
      # print "approx %f efficient at a cut of %f"%(yval,newBinEdge)
      if yval > 0.90 and yval < 0.95: self.text90 = r.TLatex(0.01,0.75,"%s is approx 90%% efficient at a cut of %f"%(self.nom.hist.split("_")[0],newBinEdge))
      if yval > 0.95:
        self.text95 = r.TLatex(0.01,0.80,"%s is approx 95%% efficient at a cut of %f"%(self.nom.hist.split("_")[0],newBinEdge))
        if yval > 0.99:
          self.text99 = r.TLatex(0.01,0.85,"%s is >= 99%% efficient  at a cut of %f"%(self.nom.hist.split("_")[0],newBinEdge))
          break
    return [self.text90,self.text95,self.text99]
    pass

class TurnOnPrefs(object):
  """docstring for TurnOnPrefs"""
  def __init__(self,File = None, NomFile = None,DenomFile = None,Variables = None,AxisRanges = None,CumCut = None):
    self.file = File
    self.nomFile = NomFile
    self.denomFile = DenomFile
    self.variables = Variables
    self.AxisRange = AxisRanges
    self.cutList = CumCut

def AddHistos(List):
  """docstring for AddHistos"""
  hist = None
  for H in List:
    if hist is None:
      hist = H.hObj.Clone()
    else:
      hist.Add(H.hOjb)
  return hist
  pass

def Legend():
  """docstring for Legend"""
  leg = r.TLegend(0.5, 0.6, 0.8, 0.8)
  leg.SetShadowColor(0)
  leg.SetBorderSize(0)
  leg.SetFillStyle(4100)
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.SetShadowColor(0)
  leg.SetBorderSize(0)
  leg.SetFillStyle(4100)
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  return leg



prelim = r.TLatex(0.15,0.92,"#scale[0.8]{CMS}")
prelim.SetNDC()
lumi = r.TLatex(0.45,.82,"#scale[0.8]{#int L dt = 35 pb^{-1}, #sqrt{s} = 7 TeV}")
lumi.SetNDC()
c1 = r.TCanvas()

def errorFun(x, par):
  return 0.5*par[0]*(1. + r.TMath.Erf( (x[0] - par[1]) / (math.sqrt(2.)*par[2]) ))



def reBiner(Hist,minimum):
  """docstring for reBiner"""
  upArray = []
  nBins = -1
  for bin in range(0,Hist.GetNbinsX()):
    binC = 0
    n = Hist.GetBinContent(bin)
    e = Hist.GetBinError(bin)
    if e < 1: e = 1
    if (n*n)/(e*e) > minimum:
      upArray.append(Hist.GetBinLowEdge(bin+1))
      nBins+=1
    else:
      binC += (n*n)/(e*e)
      if binC > minimum:
        upArray.append(Hist.GetBinLowEdge(bin+1))
        nBins+=1
        binC = 0
  upArray.append(Hist.GetBinLowEdge(Hist.GetNbinsX()))
  nBins+=1
  rebinList = array.array('d',upArray)
  return (nBins,rebinList)
