from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math
data03 =readLHEF('/Users/sophie/LDMX/old-analysis/FFop3_cuts/30_001.lhe')
data04 =readLHEF('/Users/sophie/LDMX/old-analysis/FFop3_cuts/30_01.lhe')
data05 =readLHEF('/Users/sophie/LDMX/old-analysis/FFop3_cuts/30_1.lhe')
data06 =readLHEF('/Users/sophie/LDMX/old-analysis/FFop4_cuts/30deg.lhe')

Lumi = 0.22
ProtonsPerN = 74
Factor001=0.3678*Lumi*ProtonsPerN
Factor01=0.2651*Lumi*ProtonsPerN
Factor1=0.12*Lumi*ProtonsPerN

electrons03=data03.getParticlesByIDs([9000002,-9000002])
electrons04=data04.getParticlesByIDs([9000002,-9000002])
electrons05=data05.getParticlesByIDs([9000002,-9000002])
electrons06=data06.getParticlesByIDs([9000002,-9000002])

c1=TCanvas()

outgoing_values_p_opt3_001 = []
incoming_values_p_opt3_001 = []

outgoing_values_p_opt3_01 = []
incoming_values_p_opt3_01 = []

outgoing_values_p_opt3_1 = []
incoming_values_p_opt3_1 = []


for i, e in enumerate(electrons03):
    incoming = TLorentzVector()
    outgoing = TLorentzVector()

    if e.status is -1 :
        incoming.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        incoming_values_p_opt3_001.append(incoming)
    if e.status is 1:
        outgoing.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        outgoing_values_p_opt3_001.append(outgoing)

hist_4mom_diff_opt3_001 = []
hist_4mom_diff_opt3_001_weight = []

for j, event in enumerate(incoming_values_p_opt3_001):
    qdiff = TLorentzVector()
    qdiff = outgoing_values_p_opt3_001[j] - incoming_values_p_opt3_001[j]
    hist_4mom_diff_opt3_001.append(qdiff.M2())
    hist_4mom_diff_opt3_001_weight.append(Factor001)

for i, e in enumerate(electrons06):
    incoming = TLorentzVector()
    outgoing = TLorentzVector()

    if e.status is -1 :
        incoming.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        incoming_values_p_opt4_001.append(incoming)
    if e.status is 1:
        outgoing.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        outgoing_values_p_opt4_001.append(outgoing)

for i, e in enumerate(electrons04):
    incoming = TLorentzVector()
    outgoing = TLorentzVector()

    if e.status is -1 :
        incoming.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        incoming_values_p_opt3_01.append(incoming)
    if e.status is 1:
        outgoing.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        outgoing_values_p_opt3_01.append(outgoing)

hist_4mom_diff_opt3_01 = []
hist_4mom_diff_opt3_01_weight = []
for j, event in enumerate(incoming_values_p_opt3_01):
    qdiff = TLorentzVector()
    qdiff = outgoing_values_p_opt3_01[j] - incoming_values_p_opt3_01[j]
    hist_4mom_diff_opt3_01.append(qdiff.M2())
    hist_4mom_diff_opt3_01_weight.append(Factor01)

for i, e in enumerate(electrons06):
    incoming = TLorentzVector()
    outgoing = TLorentzVector()

    if e.status is -1 :
        incoming.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        incoming_values_p_opt4_01.append(incoming)
    if e.status is 1:
        outgoing.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        outgoing_values_p_opt4_01.append(outgoing)


for i, e in enumerate(electrons05):
    incoming = TLorentzVector()
    outgoing = TLorentzVector()

    if e.status is -1 :
        incoming.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        incoming_values_p_opt3_1.append(incoming)
    if e.status is 1:
        outgoing.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
        outgoing_values_p_opt3_1.append(outgoing)

hist_4mom_diff_opt3_1 = []
hist_4mom_diff_opt3_1_weight = []

for j, event in enumerate(incoming_values_p_opt3_1):
    qdiff = TLorentzVector()
    qdiff = outgoing_values_p_opt3_1[j] - incoming_values_p_opt3_1[j]
    hist_4mom_diff_opt3_1.append(qdiff.M2())
    hist_4mom_diff_opt3_1_weight.append(Factor1)


fig, ax = plt.subplots(1,1)
n, bins, patches = ax.hist(hist_4mom_diff_opt3_1,
                           bins=50,
                           range=(-10,0),  histtype='step',
                           label="$P^{\gamma}_{lab} > $1 GeV", weights = hist_4mom_diff_opt3_1_weight)
n, bins, patches = ax.hist(hist_4mom_diff_opt3_01,
                           bins=50,
                           range=(-10,0),  histtype='step',
                           label="$P^{\gamma}_{lab} > $0.1 GeV", weights = hist_4mom_diff_opt3_01_weight)
n, bins, patches = ax.hist(hist_4mom_diff_opt3_001,
                           bins=50,
                           range=(-10,0),  histtype='step',
                           label="$P^{\gamma}_{lab} > $0.01 GeV", weights = hist_4mom_diff_opt3_001_weight)
ax.set_xlabel('$\Delta q^{2}$')
ax.legend(prop={'size': 10})
#ax.set_yscale('log')
ax.legend(prop={'size': 10})
fig.show()
fig.savefig("QSquared.pdf")
