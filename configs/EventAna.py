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
        self.hcalClusters = ROOT.std.vector('ldmx::HcalCluster')();
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("RecoilTracks_TrackerReco",  ROOT.AddressOf( self.recoilTracking ));
        self.tin1.SetBranchAddress("HcalRecHits_v14", ROOT.AddressOf( self.hcalHits ));
        self.tin1.SetBranchAddress("EcalRecHits_v14", ROOT.AddressOf( self.ecalHits ));
        self.tin1.SetBranchAddress("HcalClusters_v14",  ROOT.AddressOf( self.hcalClusters ));
        # loop and save:
        self.loop();


    def loop(self):
        f = TFile( 'trackana.root', 'RECREATE' )
        Features = TTree( 'Features', 'Information about events' )

        NHits = array('f',[0])
        Features.Branch("NHits",  NHits,  'NHits/F')

        Mom = array('f',[0])
        Features.Branch("Mom",  Mom,  'Mom/F')

        D0 = array('f',[0])
        Features.Branch("D0",  D0,  'D0/F')

        Z0 = array('f',[0])
        Features.Branch("Z0", Z0,  'Z0/F')

        Phi = array('f',[0])
        Features.Branch("Phi", Phi,  'Phi/F')

        Theta = array('f',[0])
        Features.Branch("Theta", Theta,  'Theta/F')

        SumECAL = array('f',[0])
        Features.Branch("SumECAL", SumECAL,  'SumECAL/F')

        SumHCAL = array('f',[0])
        Features.Branch("SumHCAL", SumHCAL,  'SumHCAL/F')

        nClusters = array('f',[0])
        Features.Branch("nClusters", nClusters,  'nClusters/F')

        T= array('f',[0])
        Features.Branch("T", T,  'T/F')

        nent = self.tin1.GetEntriesFast();

        for i in range(nent):
            self.tin1.GetEntry(i);
            NHits[0] = 0
            Mom[0] = 0
            D0[0] = 0
            Z0[0] = 0
            Phi[0] = 0
            Theta[0] = 0
            T[0] = 0
            SumECAL[0] = 0
            SumHCAL[0] =0
            nClusters[0] = 0
            #avEClu[0] = 0
            #avNHitsClu[0] = 0
            hasTrack = False
            for ih, track in enumerate(self.recoilTracking):
                NHits[0] = track.getNhits();
                Mom[0] = math.sqrt(track.getMomentum()[0]*track.getMomentum()[0] + track.getMomentum()[1]*track.getMomentum()[1] + track.getMomentum()[2]*track.getMomentum()[2])
                D0[0] = track.getD0()
                Z0[0] = track.getZ0()
                Phi[0] = track.getPhi()
                Theta[0] = track.getTheta()
                T[0] = track.getT()
                hasTrack = True

            for hit in self.hcalHits:
                sumHcal = 0
                if (hit.isNoise()==0):
                    SumHCAL[0] += hit.getPE()
            for hit in self.ecalHits:
                if (hit.isNoise() is False):
                    SumECAL[0] +=  hit.getEnergy()

            #for cluster in self.hcalClusters:
            nClusters[0] = len(self.hcalClusters)

            if hasTrack == True:
                Features.Fill()
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
