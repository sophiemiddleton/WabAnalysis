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
        self.tin.SetBranchAddress("SimParticles_PF", ROOT.AddressOf( self.simParticles ));
        self.tin.SetBranchAddress("HcalRecHits_PF", ROOT.AddressOf( self.hcalHits ));
        self.tin.SetBranchAddress("EcalRecHits_PF", ROOT.AddressOf( self.ecalHits ));
        self.tin.SetBranchAddress("HcalClusters_PF",  ROOT.AddressOf( self.hcalClusters ));
        self.tin.SetBranchAddress("HcalScoringPlaneHits_PF", ROOT.AddressOf( self.hcalSPHits ));
        self.tin.SetBranchAddress("EcalScoringPlaneHits_PF", ROOT.AddressOf( self.ecalSPHits ));
        self.tin.SetBranchAddress("TargetScoringPlaneHits_PF", ROOT.AddressOf( self.targetSPHits ));
        self.tin.SetBranchAddress("RecoilSimHits_PF", ROOT.AddressOf( self.recoilSimHits ));
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
        TrueParticles = TTree( 'TrueParticles', 'Information about SimParticles' )
        Clusters= TTree( 'Clusters', 'Information about Clusters Events' )
        EventLoop = TTree( 'EventLoops', 'Information about one-per Events' )
        ScoringPlanes = TTree( 'ScoringPlanes', 'Information about one-per ScoringPlanes' )
        TargetScoringPlanes = TTree( 'TargetScoringPlanes', 'Information about one-per Target ScoringPlanes' )
        Background = TTree( 'Background', 'Information about one-per Event' )
        ScoringBackground = TTree( 'ScoringBackground', 'Information about one-per Event' )
        RecoilTracker = TTree( 'RecoilTracker', 'Information about one-per Event' )
        ECALRecHits = TTree( 'ECALRecHits', 'Information about one-per ECAL event' )
        ECALBDT = TTree( 'ECALBDT', 'Information about one-per  event' )
        HcalVetoTree = TTree( 'HcalVetoTree', 'Information about one-per  event' )
        HcalTree = TTree( 'HcalTree', 'Information about HCal Event' )
        HCALRecHits = TTree( 'HCALRecHits', 'Information about HCAL REC HITS' )
        # Make Floats for branch:

        # BDT_BKG
        BDTScore = array('d',[0])
        BDTBKG = array('i',[0])
        HcalVetoPass = array('i',[0])
        VetoBKG = array('i',[0])

        # SimPart
        """
        q_squared = array('d',[0])
        PartMom = array('d',[0])
        PartID = array('d',[0])

        PartnElecDaughters  =   array('d',[0])
        """
        ElecEnergy = array('d',[0])
        ElecPosX = array('d',[0])
        ElecPosY = array('d',[0])
        ElecPosZ = array('d',[0])
        PhotEnergy = array('d',[0])
        PhotPosX = array('d',[0])
        PhotPosY = array('d',[0])
        PhotPosZ = array('d',[0])

        PartBKG =   array('i',[0])

        # Target Scoring Planes
        ElecTargetMom = array('d',[0])
        PhotTargetMom = array('d',[0])
        EnergyDepInTarget = array('d',[0])
        PhotTargetEnergy = array('d',[0])
        OtherTargetMom = array('d',[0])
        ElecTargetEnergy = array('d',[0])
        TargetPDG = array('d',[0])

        # Recoil Tracker
        TotalRecoilEnergy = array('d',[0])
        RecoilPDG = array('d',[0])
        ElecRecoilEnergy = array('d',[0])
        ElecRecoilPosX = array('d',[0])
        ElecRecoilPosY = array('d',[0])
        ElecRecoilMomX = array('d',[0])
        ElecRecoilMomY = array('d',[0])
        ElecRecoilPathLength = array('d',[0])
        PhotRecoilEnergy = array('d',[0])
        PhotRecoilPosX = array('d',[0])
        PhotRecoilPosY = array('d',[0])
        PhotRecoilMomX = array('d',[0])
        PhotRecoilMomY = array('d',[0])
        PhotRecoilPathLength = array('d',[0])

        #Clusters
        nClusters = array('d',[0])
        Cluster_nHits  = array('d',[0])
        Cluster_Energy = array('d',[0])
        Cluster_time = array('d',[0])
        Cluster_x = array('d',[0])
        Cluster_y = array('d',[0])

        #Bkg
        Cluster_nHits_inBKG  = array('d',[0])
        Cluster_Energy_inBKG = array('d',[0])
        Cluster_x_inBKG = array('d',[0])
        Cluster_y_inBKG = array('d',[0])
        Cluster_theta_inBKG = array('d',[0])
        Cluster_mom_inBKG = array('d',[0])
        ElectronTargetAngle_BKG = array('d',[0])
        ElectronTargetAngle = array('d',[0])

        #Event
        EventNumber = array('d',[0])
        Cluster_MeanEnergy = array('d',[0])
        Cluster_RMSEnergy = array('d',[0])
        Cluster_Mean_nHits = array('d',[0])
        Cluster_RMS_nHits = array('d',[0])
        Cluster_Mean_x = array('d',[0])
        Cluster_RMS_x = array('d',[0])
        Cluster_Mean_y = array('d',[0])
        Cluster_RMS_y = array('d',[0])
        sumHcalPE  = array('d',[0])
        sumEcalPE = array('d',[0])
        sumHcalPE_momCut  = array('d',[0])
        sumEcalPE_momCut = array('d',[0])
        nPhotons_HCAL = array('d',[0])
        nElectrons_HCAL = array('d',[0])
        nPhotons_ECAL = array('d',[0])
        nElectrons_ECAL = array('d',[0])
        TargetPlaneElecEnergyDep = array('d',[0])
        TargetPlaneOtherEnergyDep = array('d',[0])
        TargetPlanePhotEnergyDep = array('d',[0])

        # HCAL Hits
        HCAL_Posx =  array('d',[0])
        HCAL_Posy =  array('d',[0])
        HCAL_Posz =  array('d',[0])
        HCAL_EDep =  array('d',[0])

        #SP:
        ScoringPlane_mom =  array('d',[0])
        ScoringPlane_theta =  array('d',[0])
        ScoringPlane_x = array('d',[0])
        ScoringPlane_y =  array('d',[0])
        HCAL_Elec_Anglex =  array('d',[0])
        HCAL_Elec_Angley =  array('d',[0])
        HCAL_Phot_Anglex =  array('d',[0])
        HCAL_Phot_Angley =  array('d',[0])
        HCAL_Elec_Posx =  array('d',[0])
        HCAL_Elec_Posy =  array('d',[0])
        HCAL_Other_Posx =  array('d',[0])
        HCAL_Other_Posy =  array('d',[0])
        HCAL_Phot_Posx =  array('d',[0])
        HCAL_Phot_Posy =  array('d',[0])

        #ScoringBKG:
        ScoringPlane_y_inBKG =  array('d',[0])
        ScoringPlane_x_inBKG =  array('d',[0])
        ScoringPlane_mom_inBKG =  array('d',[0])

        ScoringPlanesBKG =  array('i',[0])
        EventLoopBKG =  array('i',[0])
        RecoilTrackerBKG =  array('i',[0])
        TargetScoringPlanesisBKG =  array('i',[0])
        ClustersisBKG =  array('i',[0])

        #ECAL Rec Hits:
        ECALEDep  =  array('d',[0])
        ECALnHits =  array('i',[0])
        EcalRecHitsisBKG =  array('i',[0])

        # Create Trees:
        ECALBDT.Branch("BDTScore",  BDTScore,  'BDTScore/D')
        ECALBDT.Branch("BDTBKG",  BDTBKG,  'BDTBKG/I')
        HcalVetoTree.Branch("HcalVetoPass",  HcalVetoPass,  'HcalVetoPass/I')
        HcalVetoTree.Branch("VetoBKG",  VetoBKG,  'VetoBKG/I')

        #HCALRecHits.Branch("HCAL_Posx",HCAL_Posx,'HCAL_Posx/D')
        #HCALRecHits.Branch("HCAL_Posy",HCAL_Posy,'HCAL_Posy/D')
        #HCALRecHits.Branch("HCAL_Posz",HCAL_Posz,'HCAL_Posz/D')
        HCALRecHits.Branch("HCAL_EDep",HCAL_EDep,'HCAL_EDep/D')

        ECALRecHits.Branch("ECALEDep",  ECALEDep,  'ECALEDep/D')
        ECALRecHits.Branch("ECALnHits",  ECALnHits,  'ECALnHits/D')
        ECALRecHits.Branch("EcalRecHitsisBKG",  EcalRecHitsisBKG ,  'EcalRecHitsisBKG/D')
        """
        TrueParticles.Branch("q_squared",  q_squared,  'q_squared/D')
        TrueParticles.Branch("PartMom",  PartMom,  'PartMom/D')
        TrueParticles.Branch("PartID",  PartID,  'PartID/D')
        TrueParticles.Branch("PartBKG",  PartBKG,  'PartBKG/I')
        TrueParticles.Branch("PartnElecDaughters",PartnElecDaughters,'PartnElecDaughters/D')
        """
        TrueParticles.Branch("ElecEnergy",  ElecEnergy,  'ElecEnergy/D')
        TrueParticles.Branch("ElecPosX",  ElecPosX,  'ElecPosXy/D')
        TrueParticles.Branch("ElecPosY",  ElecPosY,  'ElecPosY/D')
        TrueParticles.Branch("ElecPosZ",  ElecPosZ,  'ElecPosZ/D')
        TrueParticles.Branch("PhotEnergy",  PhotEnergy,  'PhotEnergy/D')
        TrueParticles.Branch("PhotPosX",  PhotPosX,  'PhotPosX/D')
        TrueParticles.Branch("PhotPosY",  PhotPosY,  'PhotPosY/D')
        TrueParticles.Branch("PhotPosZ",  PhotPosZ,  'PhotPosZ/D')

        Clusters.Branch("Cluster_nHits",  Cluster_nHits,  'Cluster_nHits/D')
        Clusters.Branch("Cluster_Energy", Cluster_Energy, 'Cluster_Energy/D')
        Clusters.Branch("Cluster_y", Cluster_y, 'Cluster_y/D')
        Clusters.Branch("Cluster_x", Cluster_x, 'Cluster_x/D')
        Clusters.Branch("Cluster_time", Cluster_time, 'Cluster_time/D')
        Clusters.Branch("ClustersisBKG", ClustersisBKG, 'ClustersisBKG/I')

        TargetScoringPlanes.Branch("ElecTargetMom", ElecTargetMom, 'ElecTargetMom/D')
        TargetScoringPlanes.Branch("PhotTargetMom", PhotTargetMom, 'PhotTargetMom/D')
        TargetScoringPlanes.Branch("EnergyDepInTarget", EnergyDepInTarget, 'EnergyDepInTarget/D')
        TargetScoringPlanes.Branch("ElecTargetEnergy", ElecTargetEnergy, 'ElecTargetEnergy/D')
        TargetScoringPlanes.Branch("PhotTargetEnergy", PhotTargetEnergy, 'PhotTargetEnergy/D')
        TargetScoringPlanes.Branch("OtherTargetMom", OtherTargetMom, 'OtherTargetMom/D')
        TargetScoringPlanes.Branch("TargetPDG", TargetPDG, 'TargetPDG/D')
        TargetScoringPlanes.Branch("ElectronTargetAngle", ElectronTargetAngle, 'ElectronTargetAngle/D')
        TargetScoringPlanes.Branch("TargetScoringPlanesisBKG", TargetScoringPlanesisBKG, 'TargetScoringPlanesisBKG/I')

        RecoilTracker.Branch("TotalRecoilEnergy", TotalRecoilEnergy, 'TotalRecoilEnergy/D')
        RecoilTracker.Branch("RecoilPDG", RecoilPDG, 'RecoilPDG/D')
        RecoilTracker.Branch("RecoilTrackerBKG", RecoilTrackerBKG, 'RecoilTrackerBKG/I')
        RecoilTracker.Branch("ElecRecoilEnergy", ElecRecoilEnergy, 'ElecRecoilEnergy/D')
        RecoilTracker.Branch("ElecRecoilPosX", ElecRecoilPosX, 'ElecRecoilPosX/D')
        RecoilTracker.Branch("ElecRecoilPosY", ElecRecoilPosY, 'ElecRecoilPosY/D')
        RecoilTracker.Branch("ElecRecoilMomX", ElecRecoilMomX, 'ElecRecoilMomX/D')
        RecoilTracker.Branch("ElecRecoilMomY", ElecRecoilMomY, 'ElecRecoilMomY/D')
        RecoilTracker.Branch("ElecRecoilPathLength", ElecRecoilPathLength, 'ElecRecoilPathLength/D')
        RecoilTracker.Branch("PhotRecoilPosX", PhotRecoilPosX, 'PhotRecoilPosX/D')
        RecoilTracker.Branch("PhotRecoilPosY", PhotRecoilPosY, 'PhotRecoilPosY/D')
        RecoilTracker.Branch("PhotRecoilMomX", PhotRecoilMomX, 'PhotRecoilMomX/D')
        RecoilTracker.Branch("PhotRecoilMomY", PhotRecoilMomY, 'PhotRecoilMomY/D')
        RecoilTracker.Branch("PhotRecoilPathLength", PhotRecoilPathLength, 'PhotRecoilPathLength/D')


        EventLoop.Branch("EventNumber", EventNumber, 'EventNumber/D')
        EventLoop.Branch("nClusters", nClusters, 'nClusters/D')
        EventLoop.Branch("sumHcalPE",  sumHcalPE,  'sumHcalPE/D')
        EventLoop.Branch("sumEcalPE", sumEcalPE, 'sumEcalPE/D')
        EventLoop.Branch("sumHcalPE_momCut",  sumHcalPE_momCut,  'sumHcalPE_momCut/D')
        EventLoop.Branch("sumEcalPE_momCut", sumEcalPE_momCut, 'sumEcalPE_momCut/D')
        EventLoop.Branch("Cluster_MeanEnergy", Cluster_MeanEnergy, 'Cluster_MeanEnergy/D')
        EventLoop.Branch("Cluster_RMSEnergy", Cluster_RMSEnergy, 'Cluster_RMSEnergy/D')
        EventLoop.Branch("Cluster_Mean_nHits", Cluster_Mean_nHits, 'Cluster_Mean_nHits/D')
        EventLoop.Branch("Cluster_RMS_nHits", Cluster_RMS_nHits, 'Cluster_RMS_nHits/D')
        EventLoop.Branch("Cluster_Mean_x", Cluster_Mean_x, 'Cluster_Mean_x/D')
        EventLoop.Branch("Cluster_RMS_x", Cluster_RMS_x, 'Cluster_RMS_x/D')
        EventLoop.Branch("Cluster_Mean_y", Cluster_Mean_y, 'Cluster_Mean_y/D')
        EventLoop.Branch("Cluster_RMS_y", Cluster_RMS_y, 'Cluster_RMS_y/D')
        EventLoop.Branch("nPhotons_HCAL", nPhotons_HCAL, 'nPhotons_HCAL/D')
        EventLoop.Branch("nElectrons_HCAL", nElectrons_HCAL, 'nElectrons_HCAL/D')
        EventLoop.Branch("nPhotons_ECAL", nPhotons_ECAL, 'nPhotons_ECAL/D')
        EventLoop.Branch("nElectrons_ECAL", nElectrons_ECAL, 'nElectrons_ECAL/D')
        EventLoop.Branch("TargetPlaneElecEnergyDep", TargetPlaneElecEnergyDep, 'TargetPlaneElecEnergyDep/D')
        EventLoop.Branch("TargetPlaneOtherEnergyDep", TargetPlaneOtherEnergyDep, 'TargetPlaneOtherEnergyDep/D')
        EventLoop.Branch("TargetPlanePhotEnergyDep", TargetPlanePhotEnergyDep, 'TargetPlanePhotEnergyDep/D')
        EventLoop.Branch("EventLoopBKG", EventLoopBKG, 'EventLoopBKG/I')

        ScoringPlanes.Branch("ScoringPlane_mom", ScoringPlane_mom , 'ScoringPlane_mom/D')
        ScoringPlanes.Branch("ScoringPlane_theta", ScoringPlane_theta , 'ScoringPlane_theta/D')
        ScoringPlanes.Branch("ScoringPlane_x", ScoringPlane_x , 'ScoringPlane_x/D')
        ScoringPlanes.Branch("ScoringPlane_y", ScoringPlane_y , 'ScoringPlane_y/D')
        ScoringPlanes.Branch("ScoringPlanesBKG", ScoringPlanesBKG, 'ScoringPlanesBKG/I')
        ScoringPlanes.Branch("ScoringPlanesElecAngleX",HCAL_Elec_Anglex, 'HCAL_Elec_Anglex/D')
        ScoringPlanes.Branch("ScoringPlanesElecAngleY",HCAL_Elec_Angley, 'HCAL_Elec_Angley/D')
        ScoringPlanes.Branch("ScoringPlanesPhotAngleX",HCAL_Phot_Anglex, 'HCAL_Phot_Anglex/D')
        ScoringPlanes.Branch("ScoringPlanesPhotAngleY",HCAL_Phot_Angley, 'HCAL_Phot_Angley/D')
        ScoringPlanes.Branch("ScoringPlanesElecPosX",HCAL_Elec_Posx, 'HCAL_Elec_Posx/D')
        ScoringPlanes.Branch("ScoringPlanesElecPosY",HCAL_Elec_Posy, 'HCAL_Elec_Posy/D')
        ScoringPlanes.Branch("ScoringPlanesOtherPosX",HCAL_Other_Posx, 'HCAL_Other_Posx/D')
        ScoringPlanes.Branch("ScoringPlanesOtherPosY",HCAL_Other_Posy, 'HCAL_Other_Posy/D')
        ScoringPlanes.Branch("ScoringPlanesPhotPosX",HCAL_Phot_Posx, 'HCAL_Phot_Posx/D')
        ScoringPlanes.Branch("ScoringPlanesPhotPosY",HCAL_Phot_Posy, 'HCAL_Phot_Posy/D')

        Background.Branch("Cluster_nHits_inBKG",  Cluster_nHits_inBKG,  'Cluster_nHits_inBKG/D')
        Background.Branch("Cluster_Energy_inBKG", Cluster_Energy_inBKG, 'Cluster_Energy_inBKG/D')
        Background.Branch("Cluster_x_inBKG", Cluster_x_inBKG, 'Cluster_x_inBKG/D')
        Background.Branch("Cluster_y_inBKG", Cluster_y_inBKG, 'Cluster_y_inBKG/D')
        Background.Branch("Cluster_theta_inBKG", Cluster_theta_inBKG, 'Cluster_theta_inBKG/D')
        Background.Branch("ElectronTargetAngle_BKG",  ElectronTargetAngle_BKG,  'ElectronTargetAngle_BKG/D')

        ScoringBackground.Branch("ScoringPlane_y_inBKG",  ScoringPlane_y_inBKG,  'ScoringPlane_y_inBKG/D')
        ScoringBackground.Branch("ScoringPlane_x_inBKG",  ScoringPlane_x_inBKG,  'ScoringPlane_x_inBKG/D')
        ScoringBackground.Branch("ScoringPlane_mom_inBKG",  ScoringPlane_mom_inBKG,  'ScoringPlane_mom_inBKG/D')
        nBKG = 0.

        """
        has_electron_and_photon_fid = 0
        has_electron_and_photon_nofid = 0
        has_electron_fid_photon_nofid = 0
        has_electron_nofid_photon_fid = 0
        has_elec = 0
        has_phot = 0
        has_neither_particle = 0
        """
        for i in range(nentries):
            """
            has_electron_fid = 0
            has_photon_fid = 0
            has_electron_nofid = 0
            has_photon_nofid = 0
            has_both_nofid = 0
            has_both_fid = 0
            has_elec_in_event = 0
            has_phot_in_event = 0
            """

            tot_track_momentum=0
            #print(i)
            nElectrons_HCAL[0] = 0
            nPhotons_HCAL[0] = 0
            nOther_HCAL = 0
            nElectrons_ECAL[0] = 0
            nPhotons_ECAL[0] = 0
            ECALEDep[0] = 0.
            HCAL_EDep[0] = 0.
            ECALnHits[0] = 0
            nClusters[0] = 0.
            hasEventinSig = False
            ScoringPlanesBKG[0] = False
            EventLoopBKG[0] = False
            RecoilTrackerBKG[0] = False
            TargetScoringPlanesisBKG[0] =  False
            EcalRecHitsisBKG[0] = False
            ClustersisBKG[0] = False
            PartBKG[0] = False
            BDTBKG[0] = False
            VetoBKG[0] = False
            energy = []
            nHits = []
            clusterx = []
            clustery = []
            self.tin.GetEntry(i);

            # veto


            # ECAL Rec HGits
            sumEcal = 0.;
            for hit in self.ecalHits:
                ECALnHits[0]+=1
                ECALEDep[0] += hit.getEnergy()
                if (hit.isNoise()==0):
                    sumEcal += hit.getEnergy()


            # HCAL RecHits
            sumHcal = 0.;
            for hit in self.hcalHits:
                HCAL_EDep[0] += hit.getEnergy()
                if (hit.isNoise()==0):
                    sumHcal += hit.getPE()
                    #HCAL_Posx[0] = hit.getPosition()[0]
                    #HCAL_Posy[0] = hit.getPosition()[1]
                    #HCAL_Posz[0] = hit.getPosition()[2]
            HCALRecHits.Fill()
            HcalTree.Fill()
            sumEcalPE[0] = sumEcal;
            sumHcalPE[0] = sumHcal;



            # ECAL SP :
            for hit in (self.ecalSPHits):
                j = hit.getID() & 0xFFF;

                if j==34 and hit.getTrackID()==1:
                    nElectrons_ECAL[0] += 1
                if j==34 and hit.getTrackID()==2:
                    nPhotons_ECAL[0] += 1

            #print("ECAL SP", nElectrons_ECAL[0],nPhotons_ECAL[0] )
            # Target Planes
            EnergyDepInTarget[0] = 0
            for ih,hit in enumerate(self.targetSPHits):
                EnergyDepInTarget[0] +=  hit.getEnergy()
                TargetPDG[0] = hit.getPdgID()
                i = hit.getID() & 0xFFF ;
                if(len(hit.getMomentum()) == 0 ): continue
                if i ==1 and hit.getTrackID()!=1 and hit.getTrackID()!=2:
                    OtherTargetMom[0] = math.sqrt(hit.getMomentum()[0]*hit.getMomentum()[0]
                    + hit.getMomentum()[1]*hit.getMomentum()[1]
                    +hit.getMomentum()[2]*hit.getMomentum()[2]);
                if i ==1 and hit.getTrackID()==1: # elec
                    ElecTargetMom[0] = math.sqrt(hit.getMomentum()[0]*hit.getMomentum()[0]
                    + hit.getMomentum()[1]*hit.getMomentum()[1]
                    +hit.getMomentum()[2]*hit.getMomentum()[2]);
                    ElecTargetEnergy[0] = hit.getEdep()
                    ElectronTargetAngle_BKG[0] = self.polar(hit.getMomentum())*180/3.1415
                    ElectronTargetAngle[0] = self.polar(hit.getMomentum())*180/3.1415
                if(event_type == "was"):
                    PhotTargetEnergy[0] = 0
                if(event_type != "was"):
                    if i ==1 and hit.getTrackID()==2: # phot
                        PhotTargetMom[0] = math.sqrt(hit.getMomentum()[0]*hit.getMomentum()[0]
                        + hit.getMomentum()[1]*hit.getMomentum()[1]
                        + hit.getMomentum()[2]*hit.getMomentum()[2]);
                        PhotTargetEnergy[0] = hit.getEdep()
            EnergyDepInTarget[0] = EnergyDepInTarget[0]#4000 - ElecTargetEnergy[0] - PhotTargetEnergy[0]
            #print("energy in target", EnergyDepInTarget[0])
            TargetScoringPlanes.Fill()


            # HCAL Cluster Loop
            for ic, cluster in enumerate(self.hcalClusters):
                Cluster_Energy[0] = cluster.getEnergy()
                energy.append(cluster.getEnergy())
                Cluster_nHits[0] = cluster.getNHits();
                nHits.append(cluster.getNHits())
                Cluster_x[0] = cluster.getCentroidX()
                clusterx.append(cluster.getCentroidX())
                Cluster_y[0] = cluster.getCentroidY()
                clustery.append(cluster.getCentroidX())
                Cluster_time[0] = cluster.getTime()

                nClusters[0] +=1;
                Clusters.Fill();
                #Background.Fill()
            Cluster_MeanEnergy[0] = round(np.mean(energy),2)
            Cluster_RMSEnergy[0] = round(np.std(energy),2)
            Cluster_Mean_nHits[0] = round(np.mean(nHits),2)
            Cluster_RMS_nHits[0] = round(np.std(nHits),2)
            Cluster_Mean_x[0] = round(np.mean(clusterx),2)
            Cluster_RMS_x[0] = round(np.std(clusterx),2)
            Cluster_Mean_y[0] = round(np.mean(clustery),2)
            Cluster_RMS_y[0] = round(np.std(clustery),2)

            for ih, hit in enumerate(self.recoilSimHits):
                i = hit.getID() & 0xFFF ;
                if i==1 :
                    tot_track_momentum = math.sqrt(hit.getMomentum()[0]*hit.getMomentum()[0]
                    + hit.getMomentum()[1]*hit.getMomentum()[1]
                    + hit.getMomentum()[2]*hit.getMomentum()[2])
            #print("total energy",sumHcalPE[0] + sumEcalPE[0])
            if (sumHcalPE[0] + sumEcalPE[0] < 2000 and nClusters[0] < 6 and  Cluster_MeanEnergy[0] < 5 and Cluster_Mean_nHits[0]<3):# and ElectronTargetAngle[0]<35: tot_track_momentum < 1200  and
                nBKG += 1
                hasEventinSig = True
                ScoringPlanesBKG[0] = True
                EventLoopBKG[0] = True
                RecoilTrackerBKG[0] = True
                TargetScoringPlanesisBKG[0] =  True
                EcalRecHitsisBKG[0] =  True
                ClustersisBKG[0] =True
                PartBKG[0] = True
                BDTBKG[0] = True
                VetoBKG[0] = True
                #print(tot_track_momentum)
                #print("background",nBKG)
            ECALRecHits.Fill()
            #BDTScore[0] = self.ecalVeto.getDisc()
            ECALBDT.Fill()

            #HcalVetoPass[0] = self.hcalVeto.passesVeto()
            HcalVetoTree.Fill()

            for hit in self.hcalSPHits:
                j = hit.getID() & 0xFFF;

                if (hit.getPdgID() == 622): continue;

                if j==41  :
                    if hit.getTrackID()==1:
                        print("electron",hit.getPdgID())
                        anglex = math.atan(hit.getPosition()[0]/hit.getPosition()[2]);
                        angley = math.atan(hit.getPosition()[1]/hit.getPosition()[2]);
                        HCAL_Elec_Anglex[0] = anglex
                        HCAL_Elec_Angley[0] = angley
                        HCAL_Elec_Posx[0] = hit.getPosition()[0]
                        HCAL_Elec_Posy[0] = hit.getPosition()[1]
                        """
                        has_elec +=1
                        has_elec_in_event +=1
                        if (anglex) > 0.5 or (angley) > 0.5:
                            has_electron_nofid +=1
                            has_both_nofid +=1


                        if (anglex) <= 0.5 and (angley) <= 0.5:
                            has_electron_fid +=1
                            has_both_fid +=1
                        """

                    if hit.getTrackID()==2:
                        #print("photon",hit.getPdgID())
                        anglex = math.atan(hit.getPosition()[0]/hit.getPosition()[2]);
                        angley = math.atan(hit.getPosition()[1]/hit.getPosition()[2]);
                        HCAL_Phot_Anglex[0] = anglex
                        HCAL_Phot_Angley[0] = angley
                        HCAL_Phot_Posx[0] = hit.getPosition()[0]
                        HCAL_Phot_Posy[0] = hit.getPosition()[1]
                        """
                        has_phot +=1
                        has_phot_in_event+=1
                        if (anglex) > 0.5 or (angley) > 0.5:
                            has_photon_nofid +=1
                            has_both_nofid +=1

                        if (anglex) <= 0.5 and (angley) <= 0.5:
                            has_photon_fid +=1
                            has_both_fid +=1

                        """
                    if hit.getTrackID()!=1 and hit.getTrackID()!=2:
                        #print("other",hit.getPdgID())
                        HCAL_Other_Posx[0] = hit.getPosition()[0]
                        HCAL_Other_Posy[0] = hit.getPosition()[1]
            """
            if has_both_nofid ==2:
                has_electron_and_photon_nofid +=1 #all events
            if has_both_fid==2:
                has_electron_and_photon_fid +=1 #all events
            if has_electron_fid==1 and has_photon_nofid == 1: #all events
                has_electron_fid_photon_nofid +=1
            if has_electron_nofid==1 and has_photon_fid == 1:
                has_electron_nofid_photon_fid +=1 #all events
            if has_elec_in_event==0 and has_phot_in_event==0:
                has_neither_particle +=1
            #print(" events with e at HCAL", has_elec, " events with phot at HCAL",has_phot, "event has enither", has_neither_particle,  "Has Both in fid",
            #has_electron_and_photon_fid, "Has Electron at fid  photon nofid",has_electron_fid_photon_nofid ,
            #"has e and photon no fid", has_electron_and_photon_nofid, "events with photon fi, electon no fid" , has_electron_nofid_photon_fid)
            """

            for hit in self.hcalSPHits:
                if (hit.getPdgID() == 622): continue;
                j = hit.getID() & 0xFFF;

                if j==41 and hit.getTrackID()==1 and hit.getPdgID()==11:
                    nElectrons_HCAL[0] +=1

                if j==41 and hit.getTrackID()==2 and hit.getPdgID()==22:
                    nPhotons_HCAL[0] +=1
                #print("track ID ",hit.getTrackID())
                momvec = hit.getMomentum()
                ScoringPlane_mom[0]    = (momvec[0]*momvec[0]+momvec[1]*momvec[1]+momvec[2]*momvec[2])**0.5
                if(math.sqrt(momvec[0]*momvec[0]+momvec[1]*momvec[1]+momvec[2]*momvec[2]) != 0):
                    ScoringPlane_theta[0]  = math.acos(momvec[2]/math.sqrt(momvec[0]*momvec[0]+momvec[1]*momvec[1]+momvec[2]*momvec[2]))*180/3.1415;
                    ScoringPlane_x[0] = hit.getPosition()[0]
                    ScoringPlane_y[0] = hit.getPosition()[1]
                if (ScoringPlane_mom[0] > 500) :
                    sumHcalPE_momCut[0] = sumHcal;
                    sumEcalPE_momCut[0] = sumEcal;
                ScoringPlanes.Fill();
            #print("HCAL scoring plane ", nElectrons_HCAL[0], nPhotons_HCAL[0])
                # ECAL SP :
            for hit in (self.ecalSPHits):
                j = hit.getID() & 0xFFF;

                if j==34 and hit.getTrackID()==1:
                    nElectrons_ECAL[0] += 1
                if j==34 and hit.getTrackID()==2:
                    nPhotons_ECAL[0] += 1



                # SimPart
            for p, part in enumerate(self.simParticles):
                if part.second.getPdgID() == 11 and part.second.getProcessType() == 13:
                    ElecEnergy[0] = part.second.getEnergy()
                    ElecPosX[0] = part.second.getEndPoint()[0]
                    ElecPosY[0] = part.second.getEndPoint()[1]
                    ElecPosZ[0] = part.second.getEndPoint()[2]
                if part.second.getPdgID() == 22 and part.second.getProcessType() == 13:
                    PhotEnergy[0] = part.second.getEnergy()
                    PhotPosX[0] = part.second.getEndPoint()[0]
                    PhotPosY[0] = part.second.getEndPoint()[1]
                    PhotPosZ[0] = part.second.getEndPoint()[2]
                #PartID[0] =  part.second.getPdgID()
                #PartMom[0] =  part.second.getEnergy()
                #PartnElecDaughters[0] = 0
                #for i,j in enumerate(part.second.getDaughters()):
                #    PartnElecDaughters[0] +=1
                    #print("parents ",part.second.getPdgID(), i, j)

                #print("sim part ", part.second.getEnergy(), part.second.getPdgID())
            TrueParticles.Fill()

            # HCAL Cluster Loop
            for ic, cluster in enumerate(self.hcalClusters):
                if (sumHcalPE[0] + sumEcalPE[0] < 2000 and nClusters[0] < 6 and  Cluster_MeanEnergy[0] < 6 and Cluster_Mean_nHits[0]<3):
                    Cluster_Energy_inBKG[0] = cluster.getEnergy()
                    Cluster_nHits_inBKG[0] = cluster.getNHits();
                    Cluster_x_inBKG[0] = cluster.getCentroidX()
                    Cluster_y_inBKG[0] = cluster.getCentroidY()
                    Background.Fill()

            #### HCAL SP SECTION
            for hit in self.hcalSPHits:
                if (hit.getPdgID() == 622): continue;
                if hasEventinSig == True:
                    momvec = hit.getMomentum()
                    ScoringPlane_mom_inBKG[0]    = (momvec[0]*momvec[0]+momvec[1]*momvec[1]+momvec[2]*momvec[2])**0.5
                    ScoringPlane_x_inBKG[0] = hit.getPosition()[0]
                    ScoringPlane_y_inBKG[0] = hit.getPosition()[1]
                ScoringBackground.Fill();

            #print("In BKG", nBKG)
            """
            for ih,hit in enumerate(self.targetSPHits):
                i = hit.getID() & 0xFFF ;
                if(i ==1 and hit.getTrackID()!=1 and hit.getTrackID()!=2):
                    TargetPlaneOtherEnergyDep[0] = hit.getEdep()
                if i ==1 and hit.getTrackID()==1:
                    TargetPlaneElecEnergyDep[0] = hit.getEdep()

                 #search for photon, if remains -1 if the photon has converted for now
                if i ==1 and hit.getTrackID()==2:
                    TargetPlanePhotEnergyDep[0] = hit.getEdep()

            """
        #print("Backgrounds", nBKG)
        f.Write();
        f.Close();



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

    main(options,args);
