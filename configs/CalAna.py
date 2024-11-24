#!/usr/bin/python

# ldmx python3 MakeRootTree.py --ifile /Users/user/ldmx-sw/ALPSamples/primakoff_rootfiles/ALP_m10.root
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch, TH1F, TFile

ROOT.gSystem.Load("/Users/sophie/LDMX/software/NewClone/ldmx-sw/install/lib/libFramework.so")	;
import os
import math
import sys
import csv
import numpy as np
from array import array
from optparse import OptionParser
#import matplotlib.pyplot as plt
#sys.path.insert(0, '../')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class GetPart:

    def __init__(self, fn1, ofn, label, mass, tag):

        self.label = label
        self.mass = mass
        #input files:
        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")
        self.tag = int(tag);

        # output files:
        #self.fn_out = ofn;
        #self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #list of branches:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.recoilTracking = ROOT.std.vector('ldmx::Track')();
        self.hcalHits      = ROOT.std.vector('ldmx::HcalHit')()
        self.ecalHits      = ROOT.std.vector('ldmx::EcalHit')()
        #self.hcalClusters = ROOT.std.vector('ldmx::HcalCluster')();
        self.pfhcalClusters = ROOT.std.vector('ldmx::CaloCluster')();
        self.hcalVeto = ROOT.ldmx.HcalVetoResult()
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        #self.tin1.SetBranchAddress("RecoilTracks_TrackerReco",  ROOT.AddressOf( self.recoilTracking ));
        self.tin1.SetBranchAddress("HcalRecHits_PF", ROOT.AddressOf( self.hcalHits ));
        self.tin1.SetBranchAddress("EcalRecHits_PF", ROOT.AddressOf( self.ecalHits ));
        self.tin1.SetBranchAddress("PFHcalClusters_PF",  ROOT.AddressOf( self.pfhcalClusters ));
        self.tin1.SetBranchAddress("HcalVeto_PF", ROOT.AddressOf( self.hcalVeto ))
        # loop and save:
        self.loop();


    def loop(self):
        f = TFile( 'trackana.root', 'RECREATE' )
        Features = TTree( 'Features', 'Information about events' )

        passesVeto = array('i',[0])
        Features.Branch("passesVeto", passesVeto,  'passesVeto/I')

        SumECAL = array('f',[0])
        Features.Branch("SumECAL", SumECAL,  'SumECAL/F')

        SumHCAL = array('f',[0])
        Features.Branch("SumHCAL", SumHCAL,  'SumHCAL/F')

        nClusters = array('f',[0])
        Features.Branch("nClusters", nClusters,  'nClusters/F')

        isSignal = array('i',[0])
        Features.Branch("isSignal", isSignal,  'isSignal/I')

        nHitsPerCluster = array('f',[0])
        Features.Branch("nHitsPerCluster", nHitsPerCluster,  'nHitsPerCluster/F')
        nent = self.tin1.GetEntriesFast();

        nEventsPass = 0
        nEventsPassSide=0
        for i in range(nent):
            self.tin1.GetEntry(i);
            passesVeto[0] = self.hcalVeto.passesVeto()

            SumECAL[0] = 0
            SumHCAL[0] =0
            nClusters[0] = 0
            nHitsPerCluster[0] = 0
            isSignal[0] = 0
            hasSide = False
            nHits = []

            for hit in self.hcalHits:
                sumHcal = 0
                if (hit.isNoise()==0):
                    SumHCAL[0] += hit.getPE()
                if(hit.getSection() !=0):
                    hasSide = True
            for hit in self.ecalHits:
                if (hit.isNoise() is False):
                    SumECAL[0] +=  hit.getEnergy()

            for cluster in self.pfhcalClusters:
                nHits.append(cluster.getNHits())
                nHitsPerCluster[0] = np.mean(nHits)
            #for cluster in self.hcalClusters:
            nClusters[0] = len(self.pfhcalClusters)
            if(passesVeto[0] == 1 and SumECAL[0] < SumHCAL[0]*3 + 3500 and nClusters[0] < 1):
                nEventsPass+=1
            if(hasSide == False):
                nEventsPassSide+=1
            Features.Fill()
        print(nEventsPass,nEventsPassSide, nent)
        f.Write();
        f.Close();

def main(options,args) :
    sc = GetPart(options.ifile1,options.ofile,options.label, options.mass, options.tag);
    #sc.fout.Close();

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
    parser.add_option('--label', dest='label', default = 'primakoff',help='production model', metavar='label')
    parser.add_option('--mass', dest='mass', default = '10',help='mass of ALP', metavar='mass')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()


    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.10)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("1.1f")
    ROOT.gStyle.SetOptFit(0000)
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    main(options,args);
