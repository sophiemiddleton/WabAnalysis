from LDMX.Framework import ldmxcfg
# create my process object
p = ldmxcfg.Process( "test" )
# how many events to process?
import sys
nEv = 10000
p.maxEvents = nEv
if len(sys.argv) > 1 :
    p.maxEvents = int(sys.argv[1])
# we want to see every event
p.logFrequency = nEv+1
p.termLogLevel = 0
# Set a run number
p.run = 9001
# we also only have an output file
p.outputFiles = [ "WASB_FF3_8GEV_Hits.root" ]
from LDMX.SimCore import simulator as sim
import LDMX.Ecal.EcalGeometry
import LDMX.Hcal.HcalGeometry
mySim = sim.simulator( "mySim" )
mySim.setDetector( 'ldmx-det-v14-8gev' , True )
# Get a pre-written generator
from LDMX.SimCore import generators as gen
mySim.generators.append(gen.lhe( "Signal Generator", ("WASB_FF3_8GEV.lhe" )))

# add your configured simulation to the sequence
mySim.description = 'Basic test Simulation'
# simulate:
p.sequence = [ mySim]


""" reconstruction: """
## TS:
from LDMX.TrigScint.trigScint import TrigScintDigiProducer
from LDMX.TrigScint.trigScint import TrigScintClusterProducer
### add TS to stream:
#p.sequence.extend([ TrigScintDigiProducer.pad1() , TrigScintDigiProducer.pad2() , TrigScintDigiProducer.pad3() ])
#p.sequence.extend([ TrigScintClusterProducer.pad1() , TrigScintClusterProducer.pad2(), TrigScintClusterProducer.pad3() ])
## Ecal
from LDMX.Ecal import digi as ecaldigi
from LDMX.Ecal import EcalGeometry
from LDMX.Ecal import ecal_hardcoded_conditions
from LDMX.DetDescr.EcalGeometry import EcalGeometry as EcalHexReadoutGeometry
geom = EcalGeometry.EcalGeometryProvider.getInstance()

ecalDigis = ecaldigi.EcalDigiProducer()
ecalRec = ecaldigi.EcalRecProducer()

### add ecal to stream:
#p.sequence.extend([ecalDigis , ecalRec ])

p.keep = [
    "keep .*.*"
    ]
