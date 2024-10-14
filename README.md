## Study of WAB and Signal Tracks at 8GeV ##

# The LHE files are stored:

/Users/sophie/LDMX/old-ldmx/ldmx-files/8GeV for WABs

and

/Users/sophie/LDMX/old-ldmx/LDMX-Nov2023/8GeV_signal/ for A' signals of various masses

# Generator analysis

- The LHEs can be read using the standard lhereader.py script
- The wabana.py script can be used to plot important features from the LHE files

# reconstruction

- The script labelled "WABGun" fires WAB LHEs and stores most data products including the veto output and clusters. To use:

-- ldmx fire WABGun.py

# tracking

To create tracking output you first need to store just the hits:

-- ldmx fire WABHits.py

The run the tracking (edit the script to use the right input .root):

-- ldmx fire WABTracking.py (MakeTracks.py)

# analysis

For general analysis use ...

For tracking analysis:

-- ldmx python3 ExtractTracks.py --ifile1 WAB-tracking/roots/WABTrack/WAB_FF2_8GEV_Track.root

this produces an ntuple of track parameters

# signals at 8GeV_signal

To create general sims:

Go inside: /Users/sophie/LDMX/software/8GeV_signal/Ap1MeV
-- ldmx fire target_dark_brem_1e_8gev.py LDMX_W_UndecayedAP_mA_0.001_run_245_t1695393040.tar.gz

this produces everything you need in terms of reconstruction

To produce tracks:

pass this into MakeTracks.py (ldmx fire MakeTracks.py) and run analysis as before


# WAB Veto analysis

To fully veto WABs we need to combine information into the Veto, this includes:

- ECAL Rec hits
- HCAL Rec hits
- HCAL clusters (using old algorithm)
- 
