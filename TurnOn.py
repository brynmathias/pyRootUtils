#!/usr/bin/env python
# encoding: utf-8
"""
turnOnCurves.py

Created by Bryn Mathias on 2011-12-10.
Copyright (c) 2011 Imperial College. All rights reserved.
"""

import sys
import os
import ROOT as r
import math

class TurnOn(object):
  """Turn on curve producer"""
  def __init__(self, numerator = None, denominator = None):
    super(TurnOn, self).__init__()
    self.denominator = denominator
    self.numerator = numerator
    self.weights = None
    self.listOfTurnOns = []
    self.Approximate = False
    self.finalPlot = None
    self.Debug = True
    self.TotNumerator = None
    self.TotDenominator = None
    self.ListOfTurnOns()
    self.MakeTotalHists()
  def ListOfTurnOns(self):
    """docstring for ListOfTurnOns"""
    i = 0
    for nom,denom in zip(self.numerator,self.denominator):
      if self.Approximate is not True:
        graph = r.TGraphAsymmErrors()
        graph.SetTitle(nom.GetTitle())
        graph.Divide(nom,denom)
        graph.GetYaxis().SetRangeUser(0.,1.1)
        self.listOfTurnOns.append(graph)
      if self.Approximate is True:
        a = nom.Clone()
        if self.weights is not None:
          a.Scale(weights[i])
        a.Divde(denom)
        graph = r.TGraph(a)
        graph.GetYaxis().SetRangeUser(0.,1.1)
        self.listOfTurnOns.append(graph)
      i+=1
    return self.listOfTurnOns
    pass

  def SumOfTurnOns(self):
    """docstring for SumOfTurnOns"""
    self.ListOfTurnOns()
    self.finalPlot = r.TGraphAsymmErrors()
    self.finalPlot.Divide(self.TotNumerator,self.TotDenominator)
    for point in range(self.finalPlot.GetN()):
      sum_w_i = 0.
      sum_w_i_plus = 0.
      sum_w_i_minus = 0.
      sum_eff_times_w_i = 0.
      xVal = r.Double(0)
      tmp = r.Double(0)
      self.finalPlot.GetPoint(point,xVal,tmp)
      bin = self.TotDenominator.FindBin(xVal)
      if self.Debug is True:
        print "="*25
        print "Start Bin %f, %f, binWidth = %f "%(self.TotDenominator.GetBinLowEdge(bin),xVal-(self.TotDenominator.GetBinWidth(1)/2.),self.TotDenominator.GetBinWidth(1) )
        print "="*25


      for TurnOn,denominator in zip(self.listOfTurnOns,self.denominator):
        efficiency = r.Double(0)
        xvalAtPoint = r.Double(0)
        w_i = 0.
        ErrorYhigh = 0.
        ErrorYlow  = 0.
        TurnOn.SetTitle(denominator.GetTitle())
        TurnOn.GetPoint(point,xvalAtPoint,efficiency)
        for p in range(TurnOn.GetN()):
          xvalAtPoint = r.Double(0)            
          TurnOn.GetPoint(p,xvalAtPoint,efficiency)
          # TurnOn.Print()
          # if xvalAtPoint != xVal:
          ErrorYhigh = 0.
          ErrorYlow = 0.
          # print "Eff", efficiency
          # print  "YLow",TurnOn.GetErrorYlow(p)
          # print  "Yhigh",TurnOn.GetErrorYhigh(p)
          # print "Xval",xVal
          # print "xvalAtPoint",xvalAtPoint
          # print "p",p
          # print "TurnOn.GetN()",TurnOn.GetN()
          if xvalAtPoint == xVal:
             ErrorYhigh = TurnOn.GetErrorYhigh(point)
             ErrorYlow = TurnOn.GetErrorYlow(point)
             if ErrorYlow > 1E16 or ErrorYlow < 0.: ErrorYlow = 1.
             if ErrorYhigh > 1E16 or ErrorYhigh < 0.: ErrorYhigh = 1.
             break
        # print "Error ylow = %f, Error yHigh = %f, xVal = %f, xvalAtPoint = %f graphName = %s"%(ErrorYlow,ErrorYhigh, xVal,xvalAtPoint,TurnOn.GetTitle())
        if denominator.GetBinContent(bin) > 0.:
          if self.Debug: print ErrorYhigh, bin, denominator.GetBinLowEdge(bin), denominator.GetBinContent(bin)
          if ErrorYhigh**2 > 0.:w_i_plus = 1./(ErrorYhigh**2)
          else: w_i_plus = 1.
          sum_w_i_plus += w_i_plus
          if ErrorYlow**2 > 0. :w_i_minus = 1./(ErrorYlow**2)              
          else: w_i_minus = 1.
          sum_w_i_minus += w_i_minus
          w_i = max(w_i_minus,w_i_plus)
          sum_w_i += w_i
          sum_eff_times_w_i += (efficiency*w_i)
          if self.Debug is True:
            print " w_i_plus = %f, w_i_minus = %f, sum_w_i %f, Efficiency = %f, efficiency*w_i = %f, at x = %f"%(w_i_plus,w_i_minus,sum_w_i, efficiency, efficiency*w_i, xvalAtPoint)

      if sum_w_i > 0.:
        AvEff = sum_eff_times_w_i/sum_w_i
      else : AvEff = 0.

      if sum_w_i_minus > 0.:
        error_minus = math.sqrt(1./sum_w_i_minus)
      else: error_minus = 0.
      if sum_w_i_plus > 0.:
        error_plus = math.sqrt(1./sum_w_i_plus)
      else: error_plus = 0.

      self.finalPlot.SetPoint(point,xVal,AvEff)
      if AvEff+error_plus > 1.:
        error_plus = 1.-AvEff
      # if AvEff-error_minus < 1.:
      #   error_minus = AvEff - 1
      self.finalPlot.SetPointError(point,self.finalPlot.GetErrorXlow(point),self.finalPlot.GetErrorXhigh(point),error_minus,error_plus )
    self.finalPlot.GetYaxis().SetRangeUser(0.,1.1)
    return self.finalPlot
    pass

  def MakeTotalHists(self):
    """docstring for TotalNumerator"""
    for hist in self.numerator:
      if self.TotNumerator is None:
        self.TotNumerator = hist.Clone()
      else: self.TotNumerator.Add(hist)
    for hist in self.denominator:
      if self.TotDenominator is None:
        self.TotDenominator = hist.Clone()
      else:self.TotDenominator.Add(hist)
    pass





def WeightedSumOfTurnOns(TotDenominator = None,TurnOnHist = None,graphList = None,denominatorList = None ):
  """docstring for WeightedSumOfTurnOns"""
  finalPlot = r.TGraphAsymmErrors(TurnOnHist)
  finalPlot.Draw("ap")
  # raw_input()
  for bin in range(TotDenominator.GetNbinsX()):
    point = bin - 1
    sum_w_i = 0.
    sum_w_i_plus = 0.
    sum_w_i_minus = 0.
    sum_eff_times_w_i = 0.
    xVal = r.Double(0)
    finalPlot.GetPoint(point,xVal,r.Double(0))
    for TurnOn,denominator in zip(graphList,denominatorList):
       efficiency = r.Double(0)
       xvalAtPoint = r.Double(0)
       w_i = 0.
       ErrorYhigh = TurnOn.GetErrorYhigh(point)
       ErrorYlow = TurnOn.GetErrorYlow(point)
       TurnOn.GetPoint(point,xvalAtPoint,efficiency)
       if denominator.GetBinContent(bin) > 0.:
         if ErrorYhigh**2 > 0.:  w_i_plus = 1./(ErrorYhigh**2)
         else: w_i_plus = 0.
         sum_w_i_plus += w_i_plus
         if ErrorYlow**2 > 0. :w_i_minus = 1./(ErrorYlow**2)
         else: w_i_minus = 0.
         sum_w_i_minus += w_i_minus
         w_i = max(w_i_minus,w_i_plus)
         sum_w_i += w_i
         sum_eff_times_w_i += (efficiency*w_i)
         print "w_i_plus = %f, w_i_minus = %f, sum_w_i %f, Efficiency = %f, efficiency*w_i = %f, at x = %f"%(w_i_plus,w_i_minus,sum_w_i, efficiency, efficiency*w_i, xvalAtPoint)
    if sum_w_i > 0.:
      AvEff = sum_eff_times_w_i/sum_w_i
    else : AvEff = 0.
    if sum_w_i_minus > 0.:
      error_minus = math.sqrt(1./sum_w_i_minus)
    else: error_minus = 0.
    if sum_w_i_plus > 0.:
      error_plus = math.sqrt(1./sum_w_i_plus)
    else: error_plus = 0.

    finalPlot.SetPoint(point,xVal,AvEff)
    # if AvEff+error_plus > 1.:
    #   error_plus = 1.-AvEff
    # if AvEff-error_minus < 1.:
    #   error_minus = AvEff - 1
    finalPlot.SetPointError(point,finalPlot.GetErrorXlow(point),finalPlot.GetErrorXhigh(point),error_minus,error_plus )
  return finalPlot









def main():
  pass


if __name__ == '__main__':
  main()

