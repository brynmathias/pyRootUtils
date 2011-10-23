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

r.gROOT.SetStyle("Plain") #To set plain bkgds for slides
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
  r.gROOT.SetBatch(True)
  return True

class GetSumHist(object):
  def __init__(self, File = None, Directories = None, Hist = None, Col = r.kBlack, Norm = None, LegendText = None):
    # super(GetSumHist, self).__init__()
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
  def setCanvas(self,canvas):
    """docstring for setCanvas"""
    canvas.cd()
    pass
  def setRange(self,x1,x2):
    """docstring for SetRange"""
    self.xmin = x1
    self.xmax = x2
    pass

  def DifferentialTurnOn(self):
    """docstring for DifferentialTurnOn"""
    self.TGraph.Divide(self.nom.hObj,self.denom.hObj)
    self.TGraph.GetXaxis().SetTitle(self.nom.hObj.GetTitle())
    self.TGraph.GetYaxis().SetTitle("Efficiency")
    self.TGraph.GetXaxis().SetRangeUser(self.xmin,self.xmax)
    self.TGraph.GetYaxis().SetRangeUser(self.ymin,self.ymax)
    self.TGraph.SetTitle("Differential turn on for %s"%(self.nom.directories))
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
    self.TGraph.SetTitle("Cumulative turn on for %s, with a cut of %f, Efficiency is %f + %f - %f"%(self.nom.directories,Bins[1],yval,self.TGraph.GetErrorYhigh(1),self.TGraph.GetErrorYlow(1)))
    self.TGraph.GetYaxis().SetRangeUser(self.ymin,self.ymax)
    return self.TGraph




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



def GetHist(DataSetName = None,folder = None,hist = None ,col = r.kBlack,norm = None,Legend = None):
    a = r.TFile.Open(DataSetName) #open the file
    # closeList.append(a) # append the file to the close list
    if folder is none:
      Hist = a.Get(hist)
    if folder is not None:
      b = a.Get(folder) #open the directory in the root file
      Hist = b.Get(hist) # get your histogram by name
    if Hist == None : Hist = r.TH1D()
    if Legend != 0:
      leg.AddEntry(Hist,Legend,"LP") # add a legend entry
    Hist.SetLineWidth(3)
    Hist.SetLineColor(col) #set colour
    # Set the last bin to conain the over flow and sort hObj the errors
    Hist.SetBinContent(Hist.GetNbinsX() ,Hist.GetBinContent(Hist.GetNbinsX())+Hist.GetBinContent(Hist.GetNbinsX()+1))
    Hist.SetBinError(Hist.GetNbinsX() ,math.sqrt((Hist.GetBinError(Hist.GetNbinsX()))**2 + (Hist.GetBinError(Hist.GetNbinsX()+1))**2))
    Hist.SetBinContent(Hist.GetNbinsX()+1,0)
    if norm != 0:
       Hist.Scale(1.) #if not data normilse to the data by lumi, MC is by default weighted to 100pb-1, if you have changed this change here!
    return Hist

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
c1 = r.TCanvas("canvas","canname",1200,1400)


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


# First Make Turn on curves
def MakeTurnOn(CorrHist = None, UnCorrHist = None , BitList = [] ,CorThresholds = [], UnCorThresholds = []):
  hObj = []
  for Trig,Cor,UnCor,Ref in zip(BitList,CorThresholds,UnCorThresholds,RefList):
    Nom = GetHist(CorrHist,"/",Trig,0,0,"PromprReco-v4 Threshold = %f"%(Cor))
    DeNom = GetHist(CorrHist,"/",Ref,0,0,0)
    (i,bins)= reBiner(Nom,10.)
    a = Nom.Rebin(i,"a",bins)
    b = DeNom.Rebin(i,"b",bins)
    mg = r.TMultiGraph()
    TurnOn = r.TGraphAsymmErrors()
    TurnOn.Divide(a,b)
    TurnOn.SetMarkerColor(4)
    TurnOn.SetMarkerStyle(20)
    mg.Add(TurnOn)
    low = 0. if (Cor - 25.) < 0. else Cor - 25.
    high = 1000.
    fermiFunction = r.TF1("fermiFunction",errorFun,low,high,3)
    fermiFunction.SetParameters(1.00,Cor+10.,1.)
    fermiFunction.SetParNames("#epsilon","#mu","#sigma")
    TurnOn.Fit(fermiFunction,"%f"%(Cor),"%f"%(Cor),low,high)
    TurnOn.SetMarkerSize(2)
    fermiFunction.SetLineColor(5)
    hObj.append(TurnOn)
    if UnCorrHist != None:
      Nom = GetHist(UnCorrHist,"/",Trig,0,0,"PF Corrections, Threshold = %d"%(UnCor))
      DeNom = GetHist(UnCorrHist,"/","RefJet",0,0,0)
      TurnOn2 = r.TGraphAsymmErrors()
      (i,bins)= reBiner(Nom,10.)
      c = Nom.Rebin(i,"c",bins)
      d = DeNom.Rebin(i,"d",bins)
      TurnOn2.Divide(c,d)
      # TurnOn.Draw("ap same")
      mg.Add(TurnOn2)
      TurnOn2.SetMarkerColor(6)
      TurnOn2.SetMarkerStyle(22)
      TurnOn2.SetMarkerSize(2)
      # TurnOn2.GetXaxis().SetRangeUser(0.,100.)
      fermiFunction2 = r.TF1("fermiFunction2",errorFun,0.,1000.,3)
      fermiFunction2.SetParameters(1.00,UnCor,1.)
      fermiFunction2.SetParNames("#epsilon","#mu","#sigma")
      # TurnOn2.Fit(fermiFunction2,"%f"%(Cor),"%i"%(int(Cor)),low,high)
      # fermiFunction2.SetLineColor(6)
      # fermiFunction2.Draw("same")
    leg.Clear()
    leg.AddEntry(TurnOn,"PF Corrections, Threshold = %d"%(Cor), "LP")
    if UnCorrHist !=None: leg.AddEntry(TurnOn2,"Piecewise cubic Corrections, Threshold = %d"%(Cor), "LP")
    mg.Draw("ap")
    mg.GetXaxis().SetTitle("P_{T}^{RECO, Corr}")
    mg.GetYaxis().SetTitle("Efficiency")
    mg.GetXaxis().SetTitleSize(0.04)
    mg.GetXaxis().SetTitleOffset(1.17)
    # mg.GetXaxis().SetLabelOffset(1.0)
    mg.GetYaxis().SetTitleOffset(1.15)
    mg.GetYaxis().SetTitleSize(0.04)
    r.gPad.Update()
    fermiFunction.SetLineColor(4)
    fermiFunction.Draw("same")
    # if UnCorrHist !=None: fermiFunction2.Draw("SAME")
    mg.GetXaxis().SetRangeUser(0.,150.)
    if int(Cor) is 128:
      mg.GetXaxis().SetRangeUser(50.,250.)
    mg.GetYaxis().SetRangeUser(0.,1.5)
    leg.Draw("same")
    ensure_dir(CorrHist[0:-5])
    c1.SaveAs(CorrHist[0:-5]+"/TurnOnFor_%d_Jet60_PF.pdf"%(Cor))
    #c1.Clear()
    leg.Clear()
  return hObj
