# Example of how to use the LHE Reader for an electron scattering example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math

# Extract electrons:
data=[]
data=readLHEF('WAB_FF2_8GEV.lhe')
electrons=data.getParticlesByIDs([11,-11])

# Make ROOT:
c=TCanvas()
c.Divide(2,2)

hist_4in=TH1F("q^{2} in", "Incoming Electron q^{2} ", 100,0,0.00001)
hist_4out=TH1F("q^{2} out", "Outgoing Electron q^{2} ", 100,0,0.00001)

# Loop over Electrons:
for e in electrons:
    # Incoming Electron:
    if e.status == -1 :
        squared_4mom = (-e.px*e.px -e.py*e.py-e.pz*e.pz+e.energy*e.energy)
        hist_4in.Fill(squared_4mom)
    # Outgoing Electron:
    if e.status == 1:
        squared_4mom = (-e.px*e.px-e.py*e.py-e.pz*e.pz+e.energy*e.energy)
        hist_4out.Fill(squared_4mom,(Factor))

c.cd()
hist_4in.GetXaxis().SetTitle("q^{2}_{e_{in}}")
hist_4in.Draw('HIST')
hist_4out.GetXaxis().SetTitle("q^{2}_{e_{out}}")
hist_4out.Draw('HIST')
c.SaveAs("electron_angle_plots_lab_30deg"+str(FF)+".root")
