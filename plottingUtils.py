#!/usr/bin/env python
# encoding: utf-8
"""
PlottingUtils.py

Created by Bryn Mathias on 2011-09-30.
"""


import sys
import os
import ROOT as r
import math
import array

def MakeCumu(inHist):
    eh =  [1.15, 1.36, 1.53, 1.73, 1.98, 2.21, 2.42, 2.61, 2.80, 3.00 ]
    el =  [0.00, 1.00, 2.00, 2.14, 2.30, 2.49, 2.68, 2.86, 3.03, 3.19 ]
    cumulativeHist = inHist.Clone()
    maxbin = inHist.GetNbinsX()+1
    for bin in range(0,maxbin):
      err = r.Double(0)
      # val = inHist.IntegralAndError(0, bin, err)
      val = inHist.IntegralAndError(bin, maxbin, err)
      err = math.sqrt(val) if val > 9 else max(el[int(val)],eh[int(val)])
      cumulativeHist.SetBinContent(bin,val)
      cumulativeHist.SetBinError(bin,err)
    return cumulativeHist



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


# def MakeCumu(inHist):
#     cumulativeHist = inHist.Clone()
#     maxbin = inHist.GetNbinsX()
#     for bin in range(0,maxbin):
#       err = r.Double(0)
#       val = inHist.IntegralAndError(bin, maxbin, err)
#       cumulativeHist.SetBinContent(bin,val)
#       cumulativeHist.SetBinError(bin,err)
#     return cumulativeHist

def threeToTwo(h3) :
    name = h3.GetName()
    binsz = h3.GetNbinsZ()
    h2 = r.TH2D(name+"_2D",h3.GetTitle(),
                h3.GetNbinsX(), h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax(),
                h3.GetNbinsY(), h3.GetYaxis().GetXmin(), h3.GetYaxis().GetXmax(),
                )
                
    for iX in range(1, 1+h3.GetNbinsX()) :
        for iY in range(1, 1+h3.GetNbinsY()) :
            content = h3.GetBinContent(iX, iY, 1) + h3.GetBinContent(iX, iY, 2)+ h3.GetBinContent(iX, iY, 0)
            h2.SetBinContent(iX, iY, content)
    h2.GetZaxis().SetTitle(h3.GetZaxis().GetTitle())
    return h2


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
    self.checkList()
    self.returnHist()
    self.cumulativeHist = None
    self.checkErrors = False


    if self.checkErrors:
      self.CheckErrors()
  def checkList(self):
      if not isinstance(self.hist,list):
          self.hist = [self.hist]
      else: pass      
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
          if Dir is None:
              self.hObj = a.Get(self.hist)
              self.hObj.SetLineColor(self.col)
              return self.hObj
          try: a.Get(Dir)
          except: "print SubDir does not exist" 
          hf = a.Get(Dir)
          if not hf: 
              print "Subdirectory %s does not exist in %s"%(Dir,f)
              self.hObj = r.TH1D()
              return self.hObj
          for histName in self.hist:
              h = hf.Get(histName)
              if self.hObj is None:
                self.hObj = h.Clone()
              else: self.hObj.Add(h)
      if self.norm != None and len(self.norm) != 1:
        for Dir,weight in zip(self.directories,self.norm):
          weight = int(1./weight)
          hf = a.Get(Dir)
          if not hf: 
              print "Subdirectory %s does not exist in %s"%(Dir,f)
              self.hObj = r.TH1D()
              return self.hObj
          h = hf.Get(self.hist)
          if self.hObj is None:
            self.hObj = h.Clone()
            self.hObj.Scale(weight)
          else:
            self.hObj.Add(h,weight)
      self.hObj.SetDirectory(0)
      a.Close()
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
    self.DoPageNum = True
    self.fname = Fname
    # self.rfile = r.TFile(self.fname[:-4]+".root",'RECREATE')
    self.pageCounter = 1
    self.open()


  def toFile(self,ob,title):
    """docstring for toFile"""
    # self.rfile.cd()
    # ob.SetName(title)
    # ob.SetTitle(title)
    # ob.Write()
    # ob = None
    pass

  def cd(self):
    """docstring for cd"""
    self.canvas.cd()
    pass


  def open(self):
    """docstring for open"""
    self.canvas.Print(self.fname+"[")
    r.gPad.SetRightMargin(0.05)
    r.gPad.SetLeftMargin(0.15)
    r.gPad.SetTopMargin(0.07)
    r.gPad.SetBottomMargin(0.15)
    
    pass


  def close(self):
    """docstring for close"""
    # self.rfile.Write()
    # self.rfile.Close()
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

  def SetGrid(self,BOOL):
    """docstring for SetGrid"""
    if BOOL:
      self.canvas.SetGrid()
    else:
      self.canvas.SetGrid(r.kFALSE)
    pass


  def Print(self):
    """docstring for Print"""
    num = r.TLatex(0.95,0.01,"%d"%(self.pageCounter))
    num.SetNDC()
    if self.DoPageNum: num.Draw("same")
    # self.canvas.SetGridx()
    # self.canvas.SetGridy()
    self.canvas.Print(self.fname)
    self.pageCounter += 1
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

def Legend(x1 = None, y1 = None, x2 = None, y2 = None):
  """docstring for Legend"""
  leg = r.TLegend(x1,y1,x2,y2)
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

def threeToTwo(h3) :
    name = h3.GetName()
    h2 = r.TH2D(name+"_2D",h3.GetTitle(),
                h3.GetNbinsX(), h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax(),
                h3.GetNbinsY(), h3.GetYaxis().GetXmin(), h3.GetYaxis().GetXmax(),
                )

    for iX in range(1, 1+h3.GetNbinsX()) :
        for iY in range(1, 1+h3.GetNbinsY()) :
            content = h3.GetBinContent(iX, iY, 1)
            h2.SetBinContent(iX, iY, content)
    h2.GetZaxis().SetTitle(h3.GetZaxis().GetTitle())
    h2.SetDirectory(0)
    return h2



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
