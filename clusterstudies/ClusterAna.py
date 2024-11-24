#!/usr/bin/python
# use as:
# - make a list of files "ls *.root &> file.list"
# - "ldmx python3 example.py --ifile file.list"
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch, TFile, TChain
import os
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from array import array
from optparse import OptionParser
import csv

sys.path.insert(0, '../')
#branchname = "_PF"
libpath="/Users/sophie/LDMX/software/NewClone/ldmx-sw/install/lib/" #FIXME - change to your path here
ROOT.gSystem.Load(str(libpath)+"libFramework.so");

class MyEvent:
    def __init__(self, fn1, branchname ):

        self.fin = ROOT.TFile(fn1);
        self.tin = self.fin.Get("LDMX_Events")
        # Access the Data:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.hcalHits      = ROOT.std.vector('ldmx::HcalHit')()
        self.ecalHits      = ROOT.std.vector('ldmx::EcalHit')()
        #self.hcalClusters = ROOT.std.vector('ldmx::HcalCluster')();
        self.pfhcalClusters = ROOT.std.vector('ldmx::CaloCluster')();
        #self.hcalNewClusters = ROOT.std.vector('ldmx::HcalCluster')();

        # Store Branch Address:
        self.tin.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin.SetBranchAddress("HcalRecHits"+str(branchname), ROOT.AddressOf( self.hcalHits ));
        self.tin.SetBranchAddress("EcalRecHits"+str(branchname), ROOT.AddressOf( self.ecalHits ));
        #self.tin.SetBranchAddress("HcalNewClusters"+str(branchname),  ROOT.AddressOf( self.hcalClusters ))
        self.tin.SetBranchAddress("PFHcalClusters"+str(branchname),  ROOT.AddressOf( self.pfhcalClusters ))
        #self.tin.SetBranchAddress("HcalNewClusters"+str(branchname),  ROOT.AddressOf( self.hcalNewClusters ))

    def loop(self, nclusters_all, nhits_all, Etot_all, Elead_all):
        nentries = self.tin.GetEntries()
        nHits = []
        nClusters = []
        totalEs = []
        mostEs = []
        nHasClusters = 0.
        nNoClusters = 0.
        for i in range(nentries):
            ent = self.tin.GetEntry(i);
            total_E = 0.
            Most_E = 0.
            # extract HCAL hits
            nClusters.append(len(self.pfhcalClusters))
            if len(self.pfhcalClusters) > 0:
                nHasClusters += 1
            else:
                nNoClusters += 1
            for hit in self.pfhcalClusters:
                hits = hit.getNHits()
                total_E += hit.getEnergy()
                if hit.getEnergy() > Most_E:
                    Most_E = hit.getEnergy()
                nHits.append(hits)
                mostEs.append(Most_E/total_E)
            totalEs.append(total_E)
        nclusters_all.append(nClusters)
        nhits_all.append(nHits)
        Etot_all.append(totalEs)
        Elead_all.append(mostEs)

        print("hasCluster", nHasClusters, "noCluster", nNoClusters)


def main(options,args) :

    nclusters_all = []
    nhits_all = []
    totE_all = []
    Elead_all = []
    names = []
    with open(options.ifile, 'r') as file:
        csv_reader = csv.reader(file)
        for i, line in enumerate(csv_reader):
            print(line)
            #for i, line in enumerate(file):
            #    print(line)
            sc = MyEvent(line[0], line[1]) ;
            names.append(str(line[0]))
            sc.loop(nclusters_all, nhits_all, totE_all, Elead_all);
            # now make some plots of things you find interesting

    fig, ax = plt.subplots(1,1)
    for i, j in enumerate(nclusters_all):
        n, bins, patches = ax.hist(nclusters_all[i], bins=10, histtype='step', range=(0,10),label=names[i])
        mean = np.mean(nclusters_all[i])
        print(mean)
    plt.legend()
    plt.xlabel('NClusters/event')
    ax.set_yscale('log')
    plt.savefig("ncluster.pdf")

    fig, ax = plt.subplots(1,1)
    for i, j in enumerate(nclusters_all):
        n, bins, patches = ax.hist(nhits_all[i], bins=10, histtype='step',  label=names[i])
    plt.legend()
    plt.legend()
    plt.xlabel('Nhits/cluster')
    ax.set_yscale('log')
    plt.savefig("nhits.pdf")

    fig, ax = plt.subplots(1,1)
    for i, j in enumerate(totE_all):
        n, bins, patches = ax.hist(totE_all[i], bins=100, histtype='step', label=names[i])
    plt.legend()
    plt.xlabel('total E')
    ax.set_yscale('log')
    plt.savefig("totE.pdf")

    fig, ax = plt.subplots(1,1)
    for i, j in enumerate(Elead_all):
        n, bins, patches = ax.hist(Elead_all[i], bins=50, histtype='step', range=(0,1), label=names[i])
    plt.legend(loc='upper left')
    ax.set_yscale('log')
    plt.xlabel('frac. in lead')
    plt.savefig("fracE.pdf")

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--ifile', dest='ifile', default = 'file.root',help='directory with data1', metavar='idir1')

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
