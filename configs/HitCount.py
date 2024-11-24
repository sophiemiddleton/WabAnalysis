#!/usr/bin/python
import argparse
import importlib
import ROOT
import numpy as np
from ROOT import TTree, TBranch, TFile
ROOT.gSystem.Load("/Users/sophie/LDMX/software/NewClone/ldmx-sw/install/lib/libFramework.so")	;
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
        #self.simParticles = ROOT.std.map(int, 'ldmx::SimParticle')();
        self.hcalHits      = ROOT.std.vector('ldmx::HcalHit')()
        self.ecalHits      = ROOT.std.vector('ldmx::EcalHit')()
        #self.hcalSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        #self.ecalSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        #self.targetSPHits    = ROOT.std.vector('ldmx::SimTrackerHit')()
        #self.recoilSimHits = ROOT.std.vector('ldmx::SimTrackerHit')()
        #self.ecalVeto = ROOT.ldmx.EcalVetoResult()
        #self.hcalVeto = ROOT.ldmx.HcalVetoResult()
        # Store Branch Address:
        #self.tin.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        #self.tin.SetBranchAddress("SimParticles_PF", ROOT.AddressOf( self.simParticles ));
        self.tin.SetBranchAddress("HcalRecHits_PF", ROOT.AddressOf( self.hcalHits ));
        self.tin.SetBranchAddress("EcalRecHits_PF", ROOT.AddressOf( self.ecalHits ));
        #self.tin.SetBranchAddress("HcalClusters_PF",  ROOT.AddressOf( self.hcalClusters ));
        #self.tin.SetBranchAddress("HcalScoringPlaneHits_PF", ROOT.AddressOf( self.hcalSPHits ));
        #self.tin.SetBranchAddress("EcalScoringPlaneHits_PF", ROOT.AddressOf( self.ecalSPHits ));
        #self.tin.SetBranchAddress("TargetScoringPlaneHits_PF", ROOT.AddressOf( self.targetSPHits ));
        #self.tin.SetBranchAddress("RecoilSimHits_PF", ROOT.AddressOf( self.recoilSimHits ));
        #self.tin.SetBranchAddress("EcalVeto_PF", ROOT.AddressOf( self.ecalVeto ));
        #self.tin.SetBranchAddress("HcalVeto_PF", ROOT.AddressOf( self.hcalVeto ));



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

        nentries = self.tin.GetEntriesFast();
        print("Entries", nentries)
         # Make Root File:
        f = TFile( 'WABStudy.root', 'RECREATE' )
        EventLoop = TTree( 'EventLoop', 'Information about Events' )
        HitLoop = TTree( 'HCALHitLoop', 'Information about Hits' )

        # BDT_BKG
        Mom = array('d',[0])
        sumHcalPE  = array('d',[0])
        sumEcalPE = array('d',[0])
        ECALEDep  =  array('d',[0])
        HCAL_Posx  = array('d',[0])
        HCAL_Posy  = array('d',[0])
        HCAL_Posz  = array('d',[0])
        HCAL_E  = array('d',[0])
        # Create Trees:
        EventLoop.Branch("Mom",  Mom,  'Mom/D')
        EventLoop.Branch("sumHcalPE",  sumHcalPE,  'sumHcalPE/D')
        EventLoop.Branch("sumEcalPE", sumEcalPE, 'sumEcalPE/D')

        HitLoop.Branch("HCAL_Posx", HCAL_Posx, 'HCAL_Posx/D')
        HitLoop.Branch("HCAL_Posy", HCAL_Posy, 'HCAL_Posy/D')
        HitLoop.Branch("HCAL_Posz", HCAL_Posz, 'HCAL_Posz/D')
        HitLoop.Branch("HCAL_E", HCAL_E, 'HCAL_E/D')
        nBKG = 0.
        nECAL = 0.
        nHCAL = 0.
        nNoECAL = 0.
        nNoHCAL=0.
        nSideHCAL = 0.
        nNewSize=0.
        nNotSideHCAL = 0.
        nOnlyside = 0.
        nSideAndBack =0.
        nOnlyBack=0.
        for i in range(nentries):
            self.tin.GetEntry(i);
            if len(self.ecalHits)  ==0:
                nNoECAL += 1
            if len(self.ecalHits) > 0:
                nECAL += 1
            if len(self.hcalHits)  ==0:
                nNoHCAL += 1
            if len(self.hcalHits) > 0:
                nHCAL += 1
            Mom[0]=0
            sumHcalPE[0]=0
            sumEcalPE[0]=0
            passesVeto=False

            sumSideHCAL = 0.
            sumNotSideHCAL = 0.
            hasSide = False
            hasBack = False


            sumEcal = 0.;

            for hit in self.ecalHits:
                #ECALnHits[0]+=1
                hitid = hit.getID()
                layer = (hitid >> 17) & 0x3f
                if (hit.isNoise() is False):
                    sumEcal +=  hit.getEnergy()
            sumEcalPE[0] = sumEcal;

            #if self.hcalVeto.passesVeto() == False:
            # HCAL RecHits
            sumHcal = 0.;
            for hit in self.hcalHits:
                HCAL_Posx[0] = 0
                HCAL_Posy[0] = 0
                HCAL_Posz[0] = 0
                HCAL_E[0] = 0
                #print(hit.getSection()) # enum HcalSection { BACK = 0, TOP = 1, BOTTOM = 2, RIGHT = 3, LEFT = 4 };
                if(abs(hit.getSection())!=0):
                    nSideHCAL += 1;
                    sumSideHCAL += hit.getPE()
                    hasSide = True
                else:
                    nNotSideHCAL += 1;
                    sumNotSideHCAL += hit.getPE()
                    hasBack = True
                if (hit.isNoise()==0):
                    sumHcal += hit.getPE()
                    HCAL_E[0] = hit.getPE()
                    HCAL_Posx[0] = hit.getXPos();
                    HCAL_Posy[0] = hit.getYPos();
                    HCAL_Posz[0] = hit.getZPos();
                    HitLoop.Fill()

                sumHcalPE[0] = sumHcal;
                EventLoop.Fill();
            if(hasSide == True and hasBack == False):
                nOnlyside +=1
            if(hasSide == True and hasBack == True):
                nSideAndBack +=1
            if(hasSide == False and hasBack == True):
                nOnlyBack +=1
            # ECAL SP :
            """
            for hit in (self.ecalSPHits):
                j = hit.getID() & 0xFFF;

                if j==34 and hit.getTrackID()==1:
                    nElectrons_ECAL[0] += 1
                if j==34 and hit.getTrackID()==2:
                    nPhotons_ECAL[0] += 1
            """

        print("Backgrounds", nBKG)
        f.Write();
        f.Close();

        print(nECAL,nHCAL)
        print("has something in ECAL ", 100*((nECAL/(nentries))),"%")
        print("nothing in ECAL ", 100*nNoECAL/(nentries),"%")
        print("fraction of hits in side ",  100*nSideHCAL/(nSideHCAL+nNotSideHCAL), "%")
        #print("energy in side ", 100*sumSideHCAL/(sumSideHCAL+sumNotSideHCAL), "%")
        print("has only side ", 100*nOnlyside/nentries, "%")
        print("has both back and side ", 100*nSideAndBack/nentries, "%")
        print("has only back ", 100*nOnlyBack/nentries, "%")
        print("has no HCAL ", 100*nNoHCAL/nentries, "%")


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
