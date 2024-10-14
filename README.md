## Study of WAB and Signal Tracks at 8GeV ##

# The LHE files are stored:

8GeV LHE samples for WAB, WASB and WAS made using the MadGraph generator with a model stored in:  /nfs/slac/g/ldmx/users/smidd/MG5_aMC_v2_7_3

There are some issues with large errors on FF4 of the WAB and WASB, more to follow.

# Generator analysis

Within the generator directory are scripts to read the LHE files and plot generator level momentum and angular features of the electrons and photons.

- The LHEs can be read using the standard lhereader.py script
- The wabana.py script can be used to plot important features from the LHE files

# Hit and Cluster Reconstruction

- The script labelled "WABGun.py" fires WAB LHEs and stores most data products including the veto output and clusters. To use:

-- ldmx fire WABGun.py

The output will be in the format of a .root file containing LDMX products. Further analysis is required to use these products i.e. ntupling. The .root should have information from ECal and HCal rec hits and HCal clusters. The traditional HCalVeto is also ran for comparrison.

# Tracking

To create tracking output you first need to store just the hits:

-- ldmx fire WABHits.py

The run the tracking (edit the script to use the right input .root):

-- ldmx fire WABTracking.py

This produces a .root file with the track products for the Recoil Tracker (Tagger is optional). Further Ntupling is needed for analysis.

# Analysis

For general analysis use the WABAna.py. This produces an NTuple containing useful features for hits, clusters and tracks as input to the veto:

-- ldmx python3 WABAna.py --ifile1 WAB-tracking/roots/WABTrack/WAB_FF2_8GEV_all.root (output of WABGun)

For tracking analysis:

-- ldmx python3 ExtractTracks.py --ifile1 WAB-tracking/roots/WABTrack/WAB_FF2_8GEV_Track.root (output of WABTracking)

this produces an ntuple of track parameters

# signals at 8GeV_signal

To create general sims:

Go inside: /Users/sophie/LDMX/software/8GeV_signal/Ap1MeV:

-- ldmx fire target_dark_brem_1e_8gev.py LDMX_W_UndecayedAP_mA_0.001_run_245_t1695393040.tar.gz

this produces everything you need in terms of reconstruction (hits, clusters and proto-tracks)

To produce tracks in the Recoil Tracker:

pass this into MakeTracks.py (ldmx fire MakeTracks.py) and run analysis as above to get ntuples.


# WAB Veto analysis

To fully veto WABs we need to combine information into the Veto, this includes:

- Energy deposited in ECAL .v. HCAL (2D cut)
- Cluster information from Hcal
- Track parameters

The combination of this information allows for complete discrimination of WAB/WASB and WAS
