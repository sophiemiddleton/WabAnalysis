#!/usr/bin/python
import argparse
import importlib
import ROOT
import numpy as np
from ROOT import TTree, TBranch, TFile
ROOT.gSystem.Load("/Users/sophie/LDMX/software/ldmx-sw/install/lib/libFramework.so")	;
ROOT.gSystem.Load("/Users/sophie/LDMX/software/ldmx-sw/install/lib/libEcal.so")	;
import os
import math
import sys
#import numpy as np
import matplotlib.pyplot as plt
from array import array
from optparse import OptionParser
sys.path.insert(0, '../')

layer_weights = ([
    2.312, 4.312, 6.522, 7.490, 8.595, 10.253, 10.915, 10.915, 10.915, 10.915, 10.915,
    10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915,
    10.915, 10.915, 14.783, 18.539, 18.539, 18.539, 18.539, 18.539, 18.539, 18.539,
    18.539, 18.539, 9.938
])
mip_si_energy = 0.130 #MeV - corresponds to ~3.5 eV per e-h pair <- derived from 0.5mm thick Si

class Event():
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.e = []
        self.pid = []

class WabEvent:

    def __init__(self, fn1, ofn, tag, event_type):

        self.fin = ROOT.TFile(fn1);
        self.tin = self.fin.Get("LDMX_Events")

        self.tag = int(tag);

        self.fn_out = ofn;
        self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        # Access the Data:
        #self.evHeader1 = ROOT.ldmx.EventHeader()
        self.simParticles = ROOT.std.map(int, 'ldmx::SimParticle')();
        self.hcalHits      = ROOT.std.vector('ldmx::HcalHit')()
        self.ecalHits      = ROOT.std.vector('ldmx::EcalHit')()
        self.hcalClusters = ROOT.std.vector('ldmx::HcalCluster')();
        self.hcalSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        self.ecalSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        self.targetSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        self.recoilSimHits = ROOT.std.vector('ldmx::SimTrackerHit')()
        self.ecalVeto = ROOT.ldmx.EcalVetoResult()
        self.hcalVeto = ROOT.ldmx.HcalVetoResult()
        # Store Branch Address:
        #self.tin.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin.SetBranchAddress("SimParticles_v14", ROOT.AddressOf( self.simParticles ));
        self.tin.SetBranchAddress("HcalRecHits_v14", ROOT.AddressOf( self.hcalHits ));
        self.tin.SetBranchAddress("EcalRecHits_v14", ROOT.AddressOf( self.ecalHits ));
        #self.tin.SetBranchAddress("HcalClusters_v14",  ROOT.AddressOf( self.hcalClusters ));
        self.tin.SetBranchAddress("HcalScoringPlaneHits_v14", ROOT.AddressOf( self.hcalSPHits ));
        self.tin.SetBranchAddress("EcalScoringPlaneHits_v14", ROOT.AddressOf( self.ecalSPHits ));
        self.tin.SetBranchAddress("TargetScoringPlaneHits_v14", ROOT.AddressOf( self.targetSPHits ));
        self.tin.SetBranchAddress("RecoilSimHits_v14", ROOT.AddressOf( self.recoilSimHits ));
        #self.tin.SetBranchAddress("EcalVeto_v14", ROOT.AddressOf( self.ecalVeto ));
        self.tin.SetBranchAddress("HcalVeto_v14", ROOT.AddressOf( self.hcalVeto ));



        self.loop(event_type);

        self.fout.cd();
        self.fin.Close();

    def polar(self,vec):
            if (self.mag(vec) < 0.001) : return -999;
            return math.acos(vec[2]/math.sqrt(vec[0]*vec[0]+vec[1]*vec[1]+vec[2]*vec[2]));

    def phi(self,vec):
        return math.atan2(vec[1],vec[0]);

    def mag(self,vec):
        return math.sqrt(vec[0]*vec[0]+vec[1]*vec[1]+vec[2]*vec[2]);

    def loop(self, event_type):
        fracs = []
        sizes = []
        nentries = self.tin.GetEntriesFast();
        j = 400
        while( j < 1500):
            nSideHCAL = 0.
            nNewSize=0.
            nNotSideHCAL = 0.
            for i in range(nentries):
                self.tin.GetEntry(i);


                for hit in self.hcalHits:
                    if(abs(hit.getZPos()) < 870 and abs(hit.getXPos()) > 400 and abs(hit.getYPos()) > 400 ):
                        if(abs(hit.getXPos()) < j and abs(hit.getYPos()) < j):
                            nNewSize += 1

                    if(abs(hit.getZPos()) < 870 and abs(hit.getXPos()) > 400 and abs(hit.getYPos()) > 400):
                        nSideHCAL += 1;
                    else:
                        nNotSideHCAL += 1;
            j+= 10
            fracs.append(100*(nSideHCAL - nNewSize)/(nSideHCAL+nNotSideHCAL))
            sizes.append(j)

            print(j, 100*(nSideHCAL - nNewSize)/(nSideHCAL+nNotSideHCAL), "%")
        plt.plot(sizes,fracs)
        plt.xlabel('xy size [mm]')
        plt.ylabel('hits lost [%]')
        plt.savefig("WASFF3_side.pdf")

def main(options,args) :
    sc = WabEvent(options.ifile1, options.ofile,options.tag, options.event_tag) ;
    sc.fout.Close();
    print("finished main")


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    # input data files (4)
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
    parser.add_option('--type', dest='type', default = '1',help='type of process', metavar='type')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')
    parser.add_option('--event_tag', dest='event_tag', default = '1',help='file tag', metavar='event_tag')

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
    # Get the Event library
    ROOT.gSystem.Load("/Users/sophie/LDMX/software/ldmx-sw/install/lib/libFramework.so")	;
    main(options,args);