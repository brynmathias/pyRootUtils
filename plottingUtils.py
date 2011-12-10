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
    self.cumulativeHist = None
    self.checkErrors = False


    if self.checkErrors:
      self.CheckErrors()
  """docstring for GetSumHist"""
  def returnHist(self):
    """docstring for returnHist"""
    eh = [1.15, 1.36, 1.53, 1.73, 1.98, 2.21, 2.42, 2.61, 2.80, 3.00 ]
    el = [0.00, 1.00, 2.00, 2.14, 2.30, 2.49, 2.68, 2.86, 3.03, 3.19 ]
    if self.files is None: return self.hObj
    for f in self.files:
      a = r.TFile.Open(f)
      # Get The first hist in the list and clone it.
      if self.norm is None or len(self.norm) is 1:
        for Dir in self.directories:
          hf = a.Get(Dir)
          if not hf: print "Subdirectory %s does not exist"%(Dir)
          h = hf.Get(self.hist)
          if self.hObj is None:
            self.hObj = h.Clone()
          else: self.hObj.Add(h)
      if self.norm != None and len(self.norm) != 1:
        for Dir,weight in zip(self.directories,self.norm):
          weight = int(1./weight)
          hf = a.Get(Dir)
          if not hf: print "Subdirectory %s does not exist"%(Dir)
          h = hf.Get(self.hist)
          if self.hObj is None:
            self.hObj = h.Clone()
            self.hObj.Scale(weight)
          else:
            self.hObj.Add(h,weight)
    self.hObj.SetLineColor(self.col)
    self.hObj.SetMarkerColor(self.col)
    # Set the last bin to show how many events in the over flow as well
    if self.norm is not None and len(self.norm) is 1:
      self.hObj.Scale(self.norm[0])
    return self.hObj


  def CheckErrors(self):
    """docstring for CheckErrors"""
    eh =  [1.15, 1.36, 1.53, 1.73, 1.98, 2.21, 2.42, 2.61, 2.80, 3.00 ]
    el =  [0.00, 1.00, 2.00, 2.14, 2.30, 2.49, 2.68, 2.86, 3.03, 3.19 ]
    for bin in range(self.hObj.GetNbinsX()):
        if self.hObj.GetBinContent(bin) < 10.:
          n = int(self.hObj.GetBinContent(bin))
          # print "BinContent is %f, New Error is %f, DataSet is %s, Bin LowEdge is: %f"%(n,eh[n]*newWeight,DataSetName,Hist.GetBinLowEdge(bin))
          self.hObj.SetBinError(bin,eh[n])
    pass


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


  def CumulativeHist(self):
    """docstring for cumulativeHist"""
    self.cumulativeHist = self.hObj.Clone()
    maxbin = self.hObj.GetNbinsX()
    for bin in range(0,maxbin):
      err = r.Double(0)
      val = self.hObj.IntegralAndError(bin, maxbin+1, err)
      self.cumulativeHist.SetBinContent(bin,val)
      self.cumulativeHist.SetBinError(bin,err)
    return self.cumulativeHist


  def Rebin(self,nbins,binList):
    """docstring for Rebin"""
    if binList != None:
      bins = array.array('d',binList)
      tmp = self.hObj.Rebin(nbins,"tmp",bins)
      self.hObj = tmp
    else:
      self.hObj.Rebin(nbins)


  def Help(self):
    print "====================================================================================================================="
    print "Usage is GetSumHist(File = None, Directories = None, Hist = None, Col = r.kBlack, Norm = None, LegendText = None)"
    print "Methods are:"
    print "\t HideOverFlow() -- Adds the over flow bin to the last bin of the histogram and computes errors for this bin"
    print "\t SetRange(\'axis\',start,end)"
    print "\t Draw() -- Use ROOT's draw method, has to wrap classInstance.hObj.Draw()"
    print "====================================================================================================================="



class Print(object):
  """docstring for printPDF"""
  def __init__(self, Fname):
    super(Print, self).__init__()
    self.canvas = r.TCanvas()

    self.fname = Fname
    self.rfile = r.TFile(self.fname[:-4]+".root",'RECREATE')
    self.pageCounter = 1



  def toFile(self,ob,title):
    """docstring for toFile"""
    self.rfile.cd()
    ob.SetName(title)
    ob.SetTitle(title)
    ob.Write()
    ob = None
    pass

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
    self.rfile.Write()
    self.rfile.Close()
    self.canvas.Print(self.fname+"]")
    pass


  def Clear(self):
    """docstring for Clear"""
    self.canvas.Clear()
    pass

  def SetLog(self,axis,BOOL):
    """docstring for SetLog"""
    if 'x' in axis:
      if BOOL:
        self.canvas.SetLogx()
      else:
        self.canvas.SetLogx(r.kFALSE)
    if 'y' in axis:
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
    self.canvas.SetGridx()
    self.canvas.SetGridy()
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
    self.leg = Legend()
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
    self.mg = r.TMultiGraph()
    self.tgraphlist = []
    self.nomClones = []
    self.denomClones = []
    self.finalGraph = None
    self.x = []
    self.y = []
    self.errxup = []
    self.errxlow = []
    self.erryup = []
    self.errylow = []
    self.Hist = r.TH1D()#Numerator.hObj.Clone()
    # self.DivHist = Denominator.hObj.Clone()
    self.UseTgraph = True

  def setRange(self,x1,x2):
    """docstring for SetRange"""
    self.xmin = x1
    self.xmax = x2
    pass

  def DifferentialTurnOn(self):
    if self.UseTgraph == True:
      """docstring for DifferentialTurnOn"""
      self.TGraph.Divide(self.nom.hObj,self.denom.hObj)
      self.TGraph.GetXaxis().SetTitle(self.nom.hObj.GetXaxis().GetTitle())
      self.TGraph.GetXaxis().SetTitleSize(0.05)
      self.TGraph.GetYaxis().SetTitle("Efficiency")
      self.TGraph.GetXaxis().SetRangeUser(self.xmin,self.xmax)
      self.TGraph.GetYaxis().SetRangeUser(self.ymin,self.ymax)
      self.TGraph.SetTitle("Differential turn on for %s, from file: %s"%(self.nom.directories,self.nom.files))
      self.TGraph.SetName("Differential turn on for %s, from file: %s"%(self.nom.directories,self.nom.files))
      return self.TGraph
    if self.UseTgraph == False:
      # self.Hist = self.nom.hObj.Clone()
      # self.Hist.Scale(self.nom.norm[0])
      self.Hist.Divide(self.nom.hObj,self.denom.hObj,self.nom.norm[0], 1.0,"")
      self.Hist.GetXaxis().SetTitleSize(0.05)
      self.Hist.GetYaxis().SetTitle("Efficiency")
      # self.Hist.GetXaxis().SetRangeUser(self.xmin,self.xmax)
      # self.Hist.GetYaxis().SetRangeUser(self.ymin,self.ymax)
      self.Hist.SetTitle("Differential turn on for %s, from file: %s"%(self.nom.directories,self.nom.files))
      self.Hist.SetName("Differential turn on for %s, from file: %s"%(self.nom.directories,self.nom.files))
      return self.Hist
  def setGraph(self,sethist_):
    """docstring for setType"""
    self.UseTgraph = sethist_
    pass

  def RobPlot(self):
    def binomialErr(nom,denom):
      p = 0.5
      q = 1 - p
      nk = math.factorial(denom)/(math.factorial(nom) * math.factorial( denom - nom))
      print pow(p,nom) , pow(q,(denom - nom)), nk
      if pow(p,nom) == 0 or pow(q,(denom - nom)) == 0.: return 0
      pHat = nk * pow(p,nom) * (pow(q,(denom - nom)))
      return 1.96*math.sqrt((pHat*(1-pHat))/denom)
      pass
    """docstring for RobPlot"""
    self.tgraphlist = []
    binWidth = self.nom.hObj.GetBinWidth(1)
    maxi = self.nom.hObj.GetBinWidth(1) *self.nom.hObj.GetNbinsX()
    maxbin = self.nom.hObj.GetNbinsX()
    for bin in range(1,self.nom.hObj.GetNbinsX()):
      if bin * binWidth > maxi: continue
      nomErr = r.Double(0)
      denomErr = r.Double(0)
      binNom =  self.nom.hObj.IntegralAndError(bin, maxbin, nomErr)
      binDenom =  self.denom.hObj.IntegralAndError(bin, maxbin, denomErr)
      if binDenom != 0:
        print "Bin Center = %f , Efficiency = %f"%(self.nom.hObj.GetBinCenter(bin),binNom/binDenom)
        self.x.append(self.nom.hObj.GetBinCenter(bin))
        self.y.append(binNom/binDenom)
        self.errxup.append((binWidth/2.))
        self.errxlow.append(-(binWidth/2.))
        self.erryup.append(0)
        self.errylow.append(binomialErr(binNom,binDenom))
    self.finalGraph =   r.TGraphAsymmErrors(len(self.x)-1, array.array('d',self.x), array.array('d',self.y), array.array('d',self.errxlow), array.array('d',self.errxup), array.array('d',self.errylow), array.array('d',self.erryup))
    self.finalGraph.SetMarkerStyle(20)
    self.finalGraph.SetMarkerSize(0.5)
    self.finalGraph.SetTitle("%s (pre = %s) from  %s (pre = %s) "%((self.nom.hist.split("_")[2]),(self.nom.hist.split("_")[4]),(self.nom.hist.split("_")[6]),(self.nom.hist.split("_")[-1])))
    return self.finalGraph





  def CumuMultiGraph(self):
    """docstring for CumuMultiGraph"""
    triggerExpected = float((self.nom.directories[0].split("_")[1])[2:])
    print triggerExpected
    binWidth = self.nom.hObj.GetBinWidth(1)
    self.tgraphlist = []
    maxi = self.nom.hObj.GetNbinsX() * binWidth
    for bin in range(0,50):
      self.nomClones.append(self.nom.hObj.Clone())
      self.denomClones.append(self.denom.hObj.Clone())

      print self.newBins

      a = r.TGraphAsymmErrors()
      self.tgraphlist.append(a)
      self.tgraphlist[bin].SetName("i")
      self.tgraphlist[bin].Divide(self.nomClones[bin].Rebin(  len(self.newBins)-1,"a"+str(bin), self.newBins),self.denomClones[bin].Rebin(len(self.newBins)-1,"b"+str(bin), self.newBins))
      # a.GetXaxis().SetRangeUser()
      self.tgraphlist[bin].SetLineColor(bin+1)
      self.tgraphlist[bin].SetMarkerColor(bin+1)
      # self.tgraphlist.append(a)
      xval = r.Double(0)
      yval = r.Double(0)
      self.tgraphlist[bin].GetPoint(1,xval,yval)
      self.tgraphlist[bin].SetTitle("%f"%(triggerExpected + (bin * binWidth)))
      self.tgraphlist[bin].SetTitle("%f , %f"%(triggerExpected + (bin * binWidth),yval))
      print "yval = %f, bin = %d, bin lowEdge = %d"%(yval,bin,triggerExpected + (bin * binWidth))
      self.leg.AddEntry(self.tgraphlist[bin],"Eff = %f, Cut = %f"%(yval,triggerExpected + (bin * binWidth)),"l")
      print self.nom.hist
      if yval == 1.0:
        self.mg.SetTitle("%s (pre = %s) from  %s (pre = %s) "%((self.nom.hist.split("_")[2]),(self.nom.hist.split("_")[4]),(self.nom.hist.split("_")[6]),(self.nom.hist.split("_")[-1])))
        break

    for graph in self.tgraphlist:
      self.mg.Add(graph)
    return (self.mg , self.leg)
    pass


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
    self.TGraph.GetXaxis().SetTitle(self.nom.hObj.GetXaxis().GetTitle())
    self.TGraph.GetXaxis().SetTitleSize(0.05)
    return self.TGraph

  def logEffs(self):
    """docstring for logEffs"""
    yval = r.Double(0)
    xval = r.Double(0)
    self.text90 = r.TLatex(0.01,0.75,"")
    self.text95 = r.TLatex(0.01,0.80,"")
    self.text99 =  r.TLatex(0.01,0.80,"")
    maxBinEdge = self.nom.hObj.GetBinLowEdge(self.nom.hObj.GetNbinsX())
    for bin in range(1,self.nom.hObj.GetNbinsX()-1):
      TGraph = r.TGraphAsymmErrors()
      newBinEdge = self.nom.hObj.GetBinWidth(1) * bin
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
  leg = r.TLegend(0.5, 0.4, 0.8, 0.6)
  leg.SetShadowColor(0)
  leg.SetBorderSize(0)
  # leg.SetFillStyle(4100)
  # leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.SetShadowColor(0)
  leg.SetBorderSize(0)
  # leg.SetFillStyle(4100)
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
