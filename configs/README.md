## Study of WAB and Signal Tracks at 8GeV ##

# Generator analysis

- The LHEs can be read using the standard lhereader.py script
- The wabana.py script can be used to plot important features from the LHE files

# reconstruction

- The script labelled "WABGun" fires WAB LHEs and stores most data products including the veto output and clusters. To use:

-- ldmx fire WABGun.py

For PF clustering:

-- ldmx fire PFWAB.py

# tracking

The run the tracking (edit the script to use the right input .root):

-- ldmx fire MakeTracks.py

passing the output of WABGun into here

# analysis

For tracking analysis:

-- ldmx python3 EventAna.py --ifile1 WAB_FF2_8GEV_Track.root

this produces an ntuple of event parameters. A similar analyzer is built for Calo infor: CalAna.py

For studies of how many hits in each detector:

-- ldmx python3 HitCount.py

For study of side HCAL size:

-- ldmx python3 SideHCAL.py

# signals at 8GeV_signal

To create general sims:

Go inside: /Users/sophie/LDMX/software/8GeV_signal/Ap1MeV
-- ldmx fire target_dark_brem_1e_8gev.py LDMX_W_UndecayedAP_mA_0.001_run_245_t1695393040.tar.gz

this produces everything you need in terms of reconstruction

To produce tracks:

pass this into MakeTracks.py (ldmx fire MakeTracks.py) and run analysis as before
