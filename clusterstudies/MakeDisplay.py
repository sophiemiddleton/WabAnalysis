#!/usr/bin/python

# ldmx python3 MakeRootTree.py --ifile /Users/user/ldmx-sw/ALPSamples/primakoff_rootfiles/ALP_m10.root
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch, TH1F, TFile
libpath="//Users/sophie/LDMX/software/NewClone/ldmx-sw/install/lib/" #FIXME - change to your path here
ROOT.gSystem.Load(str(libpath)+"libFramework.so");
import os
import math
import sys
import csv
import numpy as np
from array import array
from optparse import OptionParser
#sys.path.insert(0, '../')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

filenames = ["WABFF2.root"]
colors = ["cyan"]
bars = ["c."]
nametag= ["WABFF2"]
hitcol=["red","orange","cyan","black","magenta","blue","yellow","green","violet"]
class GetPart:

    def __init__(self, fn1, ofn):

        #input files:
        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")

        # output files:
        self.fn_out = ofn;
        self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #list of branches:
        #self.evHeader1 = ROOT.ldmx.EventHeader()
        self.simParticles = ROOT.std.map(int, 'ldmx::SimParticle')();
        self.hcalRecHits = ROOT.std.vector('ldmx::HcalHit')();
        #self.hcalClusters = ROOT.std.vector('ldmx::HcalCluster')();
        self.pfhcalClusters = ROOT.std.vector('ldmx::CaloCluster')();
        #self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("SimParticles_PF", ROOT.AddressOf( self.simParticles ));
        self.tin1.SetBranchAddress("HcalRecHits_PF",  ROOT.AddressOf( self.hcalRecHits ));
        #self.tin1.SetBranchAddress("HcalNewClusters_PF",  ROOT.AddressOf( self.hcalClusters ));
        self.tin1.SetBranchAddress("PFHcalClusters_PF",  ROOT.AddressOf( self.pfhcalClusters ))
        self.x_positions = []
        self.y_positions = []
        self.z_positions = []
        self.energy = []
        # loop and save:
        self.loop();

    def loop(self):

        nent = self.tin1.GetEntriesFast();

        for i in range(10):#nent):
            self.tin1.GetEntry(i);

            self.ElecPosX = []
            self.ElecPosY = []
            self.ElecPosZ = []

            self.PhotPosX = []
            self.PhotPosY = []
            self.PhotPosZ = []

            self.x_positions_hits = []
            self.y_positions_hits = []
            self.z_positions_hits = []

            self.x_positions_clusters = []
            self.y_positions_clusters= []
            self.z_positions_clusters= []

            self.x_positions_cluhits = []
            self.y_positions_cluhits = []
            self.z_positions_cluhits = []

            self.energy_hits = []
            self.energy_clusters = []
            self.energy_cluhits = []
            colors_hits = []
            colors_clu = []
            names = []
            markers = []
            if (i < 10):
                """
                for ih,hit in enumerate(self.hcalRecHits):
                    self.x_positions_hits.append(hit.getXPos())
                    self.y_positions_hits.append(hit.getYPos())
                    self.z_positions_hits.append(hit.getZPos())
                    self.energy_hits.append(hit.getEnergy())
                    #colors.append("red")
                    names.append("hits")
                    #markers.append(".")
                    #self.energy.append(hit.getEnergy())
                """
                for p, part in enumerate(self.simParticles):
                    if part.second.getPdgID() == 11 and part.second.getProcessType() == 13:
                        #ElecEnergy[0] = part.second.getEnergy()
                        self.ElecPosX.append(part.second.getEndPoint()[0])
                        self.ElecPosY.append(part.second.getEndPoint()[1])
                        self.ElecPosZ.append(part.second.getEndPoint()[2])
                    if part.second.getPdgID() == 22 and part.second.getProcessType() == 13:
                        self.PhotPosX.append(part.second.getEndPoint()[0])
                        self.PhotPosY.append(part.second.getEndPoint()[1])
                        self.PhotPosZ.append(part.second.getEndPoint()[2])
                for ih, cluster in enumerate(self.pfhcalClusters):
                    self.x_positions_clusters.append(cluster.getCentroidX())
                    self.y_positions_clusters.append(cluster.getCentroidY())
                    self.z_positions_clusters.append(cluster.getCentroidZ())
                    colors_clu.append(hitcol[ih])
                    markers.append("X")
                    for jh,hit in enumerate(cluster.getHitX()):
                        self.x_positions_cluhits.append(cluster.getHitX()[jh])
                        self.y_positions_cluhits.append(cluster.getHitY()[jh])
                        self.z_positions_cluhits.append(cluster.getHitZ()[jh])
                        self.energy_cluhits.append(cluster.getHitE()[jh])
                        colors_hits.append(hitcol[ih])
                        markers.append(".")
                    names.append("PF clusters")
                fig2 = plt.figure()
                ax2 = plt.axes(projection='3d')
                ax2.set_ylabel('z [mm]')
                ax2.set_xlabel("x [mm]")
                ax2.set_zlabel("y [mm]")
                #ax2.scatter3D(self.x_positions_hits, self.z_positions_hits, self.y_positions_hits, c="blue", s=self.energy_hits);
                ax2.scatter3D(self.x_positions_clusters, self.z_positions_clusters, self.y_positions_clusters, c=colors_clu, marker="X");
                ax2.scatter3D(self.x_positions_cluhits, self.z_positions_cluhits, self.y_positions_cluhits, c=colors_hits, s=self.energy_cluhits);
                #ax2.scatter3D(self.ElecPosX, self.ElecPosZ, self.ElecPosY, c="cyan", marker="*");
                #ax2.scatter3D(self.PhotPosX, self.PhotPosZ, self.PhotPosY, c="black", marker="*");
                plt.title('event = '+str(i)+' has nclusters ='+str(len(self.pfhcalClusters)))
                #plt.legend(loc="upper right")
                fig2.savefig("Old_Event"+str(i)+'.pdf')
        #f.Write();
        #f.Close();

def main(options,args) :
    sc = GetPart(options.ifile1,options.ofile);

    sc.fout.Close();

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')

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
