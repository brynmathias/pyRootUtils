#!/usr/bin/env python
# encoding: utf-8
"""
testDraw.py

Created by Bryn Mathias on 2011-10-03.
Copyright (c) 2011 Imperial College. All rights reserved.
"""

import sys
import os
from plottingUtils import *
import ROOT as r
# def main():
c1.Print("out.pdf[")
FolderList = ["325","375_475","475_575","575_675","675_775","775_875","875"]
HistList = ["AlphaT_all","Mt2_all","HT_all"]
leg = Legend()
for label in HistList:
  Hists = []

  leg.Clear()
  dataAttrs = {'MarkerStyle':20}
  McAttrs = {"MakerStyle":0}
  data = GetSumHist(File = "./Data.root", Directories = FolderList, Hist = label, Col = r.kBlack, Norm = None, LegendText = "Data")
  data.HideOverFlow()
  data.isData = True
  MC = GetSumHist(File = "./Data.root", Directories = FolderList, Hist = label, Col = r.kRed, Norm = None, LegendText = "MC")
  MC.HideOverFlow()
  Hists.append(data)
  Hists.append(MC)
  print "datatype=",type(data)
  leg = Legend()
  for h in Hists:
    if h.isData:
      h.hObj.SetMarkerStyle(20)
      leg.AddEntry(h.hObj,h.legendText,"P")
      # h.SetRange("x",0.,3.)
      # h.out.setAtt(dataAttrs)
      h.Draw("P")
    else:
      # h.hObj.setAtt(McAttrs)
      leg.AddEntry(h.hObj,h.legendText,"l")
      h.Draw("histsame")
  # Draw Data again to get it on top!
  data.Draw("sameP")
  leg.Draw("same")
  c1.cd()
  c1.SetLogy()
  data.hObj.SetTitle(label)
  c1.Update()
  c1.Print("out.pdf")
c1.Print("out.pdf]")

