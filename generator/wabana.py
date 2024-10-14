# Example of how to use the LHE Reader for an electron scattering example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1, TFile, TStyle
import math
import pandas as pd

path = "/Users/sophie/LDMX/old-ldmx/ldmx-files/8GeV/"

# Read specific columns from CSV file
df = pd.read_csv('files.csv')

# make lists for each set of hists
hists_px_e = []
hists_py_e = []
hists_pz_e = []
hists_px_g = []
hists_py_g = []
hists_pz_g = []
hists_theta = []
# for plotting
color=[2,3,4,6,7,8,9,11,20,44,34]

# set to 1 to weight according to Xsec
donormalize=0

for i, filename in enumerate(df['filename']):
    norm = 1 # dont scale unless asked to
    if donormalize==1:
        norm=float(df['normalize'][i])
    data=readLHEF(str(df['filename'][i]))
    electrons=data.getParticlesByIDs([11,-11])
    photons=data.getParticlesByIDs([22])

    hist_e_px_out=TH1F("Electron p_{x} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)
    hist_e_py_out=TH1F("Electron p_{y} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)
    hist_e_pz_out=TH1F("Electron p_{z} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)

    hist_g_px_out=TH1F("Photon p_{x} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)
    hist_g_py_out=TH1F("Photon p_{y} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)
    hist_g_pz_out=TH1F("Photon p_{z} "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-8,8)

    hist_theta=TH1F("theta "+str(df['FF'][i]), str(df['type'][i])+str(df['FF'][i]), 100,-4,4)
    evec = TLorentzVector()
    gvec = TLorentzVector()
    # Loop over Electrons:
    for e in electrons:
        # Outgoing Electron:
        if e.status == 1:
            evec.SetPxPyPzE(e.px,e.py,e.pz,e.energy)
            hist_e_px_out.Fill(e.px,norm)
            hist_e_py_out.Fill(e.py,norm)
            hist_e_pz_out.Fill(e.pz,norm)
    # Loop over Photons:
    for g in photons:
        # Outgoing Photon:
        if g.status == 1:
            gvec.SetPxPyPzE(g.px,g.py,g.pz,g.energy)
            hist_g_px_out.Fill(g.px,norm)
            hist_g_py_out.Fill(g.py,norm)
            hist_g_pz_out.Fill(g.pz,norm)
            theta = evec.Angle(gvec.Vect())
            hist_theta.Fill(theta)
    hists_px_e.append(hist_e_px_out)
    hists_py_e.append(hist_e_py_out)
    hists_pz_e.append(hist_e_pz_out)
    hists_px_g.append(hist_g_px_out)
    hists_py_g.append(hist_g_py_out)
    hists_pz_g.append(hist_g_pz_out)
    hists_theta.append(hist_theta)

MyStyle = TStyle("myStyle","My style");
icol=0;
MyStyle.SetFrameBorderMode(icol);
MyStyle.SetFrameFillColor(icol);
MyStyle.SetCanvasBorderMode(icol);
MyStyle.SetCanvasColor(icol);
MyStyle.SetPadBorderMode(icol);
MyStyle.SetPadColor(icol);
MyStyle.SetStatColor(icol);
MyStyle.SetPadTopMargin(0.05);
MyStyle.SetPadRightMargin(0.05);
MyStyle.SetPadBottomMargin(0.16);
MyStyle.SetPadLeftMargin(0.16);
MyStyle.SetTitleXOffset(1.1);
MyStyle.SetTitleYOffset(1.1);
font=42;
tsize=0.04;
MyStyle.SetTextFont(font);
MyStyle.SetTextSize(tsize);
MyStyle.SetLabelFont(font,"XYZ");
MyStyle.SetTitleFont(font,"XYZ");

MyStyle.SetLabelSize(tsize,"XYZ");
MyStyle.SetTitleSize(tsize,"XYZ");

MyStyle.SetLegendBorderSize(0);
MyStyle.SetLegendTextSize(0.03);
MyStyle.SetLineStyleString(1,"[12 12]");

MyStyle.SetEndErrorSize(0.);

MyStyle.SetOptTitle(0);
MyStyle.SetOptStat("MR");
MyStyle.SetOptStat(0);
MyStyle.SetOptFit(0);

MyStyle.SetPadTickX(1);
MyStyle.SetPadTickY(1);
MyStyle.SetLineWidth(2);
MyStyle.SetHistLineWidth(3);
MyStyle.SetHistLineColor(1);

#MyStyle.SetPalette(8,nullptr);
MyStyle.SetFuncWidth(4);
#MyStyle.SetFuncColor(kGreen);

MyStyle.cd();

c=TCanvas()
for i, hist in enumerate(hists_px_e):
    hist.GetXaxis().SetTitle("p_{x}_{e_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c.SaveAs("elec_px.root")

c1=TCanvas()
for i, hist in enumerate(hists_py_e):
    hist.GetXaxis().SetTitle("p_{y}_{e_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c1.SaveAs("elec_py.root")

c2=TCanvas()
for i, hist in enumerate(hists_pz_e):
    hist.GetXaxis().SetTitle("p_{z}_{e_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c2.SaveAs("elec_pz.root")

c3=TCanvas()
for i, hist in enumerate(hists_px_g):
    hist.GetXaxis().SetTitle("p_{x}_{g_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c3.SaveAs("phot_px.root")

c4=TCanvas()
for i, hist in enumerate(hists_py_g):
    hist.GetXaxis().SetTitle("p_{y}_{g_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c4.SaveAs("phot_py.root")

c5=TCanvas()
for i, hist in enumerate(hists_pz_g):
    hist.GetXaxis().SetTitle("p_{z}_{g_{out}}")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c5.SaveAs("phot_pz.root")

c6=TCanvas()
for i, hist in enumerate(hists_theta):
    hist.GetXaxis().SetTitle("#theta")
    if i == 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HIST')
        hist.SetLineColor(color[i])
    if i > 0:
        hist.Scale(1/hist.Integral())
        hist.Draw('HISTSAME')
        hist.SetLineColor(color[i])
c6.SaveAs("theta.root")
