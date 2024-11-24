# Study of WAB and Signal Tracks at 8GeV ##

### LHE

8GeV LHE samples for WAB, WASB and WAS made using the MadGraph generator with a model stored in:  /nfs/slac/g/ldmx/users/smidd/MG5_aMC_v2_7_3

In 2024, a new set of samples were made with a new model, these are _corr in the LHE files.


### Generator analysis

Within the generator directory are scripts to read the LHE files and plot generator level momentum and angular features of the electrons and photons.

- The LHEs can be read using the standard lhereader.py script
- The wabana.py script can be used to plot important features from the LHE files

### WAB samples

The config directory contains information on how to make reconstructed WAB samples. The current chain:

PFWAB --> MakeTracks --> EventAna (or CalAna).

There are also several configs for specific studies.

MakeDiscriminator is a multi-purpose debugging analyzer.

### Tracking

The run the tracking (edit the script to use the right input .root):

-- ldmx fire MakeTracks.py

This produces a .root file with the track products for the Recoil Tracker (Tagger is optional).

### Analysis

For general analysis use the WABAna.py. This produces an NTuple containing useful features for hits, clusters and tracks as input to the veto:

-- ldmx python3 EventAna.py --ifile1 WAB-tracking/roots/WABTrack/WAB_FF2_8GEV_all.root (output of WABGun)

this produces an ntuple of event level parameters

### signals at 8GeV_signal

To create general sims:

Go inside: /Users/sophie/LDMX/software/8GeV_signal/Ap1MeV:

-- ldmx fire target_dark_brem_1e_8gev.py LDMX_W_UndecayedAP_mA_0.001_run_245_t1695393040.tar.gz

this produces everything you need in terms of reconstruction (hits, clusters and proto-tracks)

To produce tracks in the Recoil Tracker:

pass this into MakeTracks.py (ldmx fire MakeTracks.py) and run analysis as above to get ntuples.


### WAB Veto analysis

A simple cut and count is available in CalAna. The BDT directory contains the more sophisticated BDT scripts.

-- incBDT: assumes training on inclusive samples 
-- appBDT: apply BDT
-- WASBDT: for training on just WAS background
-- calBDT: uses just calo features
