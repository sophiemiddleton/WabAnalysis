from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('signal')
p.maxTriesPerEvent = 10000
p.maxEvents = 10000

import sys
lheLib = sys.argv[1]
detector = 'ldmx-det-v14-8gev'

import os
def is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    prefix = os.path.commonprefix([abs_directory, abs_target])
    return prefix == abs_directory


def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")
    tar.extractall(path, members, numeric_owner=numeric_owner)


import tarfile
with tarfile.open(lheLib,"r:gz") as ar :
    safe_extract(ar)


lib_parameters = os.path.basename(lheLib).replace('.tar.gz','').split('_')
ap_mass = float(lib_parameters[lib_parameters.index('mA')+1])*1000.
p.run = int(lib_parameters[lib_parameters.index('run')+1])
timestamp = lib_parameters[lib_parameters.index('run')+2]
unpacked_lib = os.path.basename(lheLib).replace(f'_{timestamp}.tar.gz','')

from LDMX.Biasing import target
mySim = target.dark_brem(ap_mass, unpacked_lib, detector)

p.sequence = [ mySim ]

import os
import sys

p.outputFiles = ['simoutput.root']

import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
import LDMX.Hcal.hcal_hardcoded_conditions
import LDMX.Ecal.digi as ecal_digi
import LDMX.Ecal.vetos as ecal_vetos
import LDMX.Hcal.digi as hcal_digi
from LDMX.Hcal import hcal as hcal
from LDMX.DetDescr.HcalGeometry import HcalGeometry
from LDMX.Hcal import HcalGeometry
from LDMX.TrigScint.trigScint import TrigScintDigiProducer
from LDMX.TrigScint.trigScint import TrigScintClusterProducer
from LDMX.TrigScint.trigScint import trigScintTrack

ts_digis = [
        TrigScintDigiProducer.pad1(),
        TrigScintDigiProducer.pad2(),
        TrigScintDigiProducer.pad3(),
        ]
for d in ts_digis :
    d.randomSeed = 1

from LDMX.Recon.electronCounter import ElectronCounter
from LDMX.Recon.simpleTrigger import TriggerProcessor

count = ElectronCounter(1,'ElectronCounter')
count.input_pass_name = ''
from LDMX.DQM import dqm

geom = HcalGeometry.HcalGeometryProvider.getInstance()

p.sequence.extend([
        ecal_digi.EcalDigiProducer(si_thickness = 0.5),
        ecal_digi.EcalRecProducer(),
        ecal_vetos.EcalVetoProcessor(),
        hcal_digi.HcalDigiProducer(),
        hcal_digi.HcalRecProducer(),
        hcal.HcalClusterProducer(),
        hcal.HcalVetoProcessor('hcalVeto'),
        *ts_digis,
        TrigScintClusterProducer.pad1(),
        TrigScintClusterProducer.pad2(),
        TrigScintClusterProducer.pad3(),
        trigScintTrack,
        count, TriggerProcessor('trigger',8000.),
        ])

if True: #False:
    p.setCompression(2, level=9) # LZMA
    from LDMX.Recon import pfReco
    ecalPF = pfReco.pfEcalClusterProducer()
    hcalPF = pfReco.pfHcalClusterProducer()
    trackPF = pfReco.pfTrackProducer()
    truthPF = pfReco.pfTruthProducer()


    # configure clustering options
    ecalPF.doSingleCluster = False
    ecalPF.logEnergyWeight = True

    hcalPF.doSingleCluster = False
    hcalPF.clusterHitDist = 200. # mm
    hcalPF.logEnergyWeight = True
    hcalPF.minHitEnergy = 0.1
    hcalPF.minClusterHitMult = 5

    ecalPF_simple = pfReco.pfEcalClusterProducer()
    ecalPF_simple.clusterCollName += "Simple"
    ecalPF_simple.doSingleCluster = True
    hcalPF_simple = pfReco.pfHcalClusterProducer()
    hcalPF_simple.clusterCollName += "Simple"
    hcalPF_simple.doSingleCluster = True

    p.sequence.extend([
        ecalPF, hcalPF, trackPF,
        pfReco.pfProducer(),
        truthPF,
        #ecalPF_simple, hcalPF_simple
    ])
