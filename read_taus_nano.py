'''
Loops on the events and operates the matching between reconstructed and generated taus
as well as reconstructed tau and seeding jet (geometrically closest to the tau).
It produces a flat ntuple with one with an entry for each reconstructed tau.

Launch with, e.g.
ipython -i -- read_taus_nano.py --qcd --maxevents 1000000 --logfreq 1000

Tau recommendations
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV

NanoAOD
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

A description of the NanoAOD branch content is given in branches.txt and
https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
'''
import ROOT
from time import time
from datetime import datetime, timedelta
from array import array
from collections import OrderedDict
from deltar import deltaR, deltaPhi

# here the ntuple branches, and how to get the quantities stored in such branches, are defined
from treeVariables import branches_event, branches_tau, branches_gen, branches_jet, branches_all, prepareBranches
from files import dy_files, qcd_files

##########################################################################################
# Argument Parser to manage options
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dy'       , dest='genuine_taus', action='store_true'  , help='Process on DY->LL sample. This option, or --qcd, needs to be always specified')
parser.add_argument('--qcd'      , dest='genuine_taus', action='store_false' , help='Process on QCD multijet sample. This option, or --dy, needs to be always specified')
parser.add_argument('--maxevents', dest='maxevents'   , default=-1 , type=int, help='Events to process. Default = -1 --> process all events')
parser.add_argument('--filename' , dest='filename'    , default=''           , help='Specify the output ntuple name. Default dy_ntuple.root if --dy is chosen, else qcd_tuple.root --qcd is chosen')
parser.add_argument('--logfreq'  , dest='logfreq'     , default=100, type=int, help='Print processing status every N events. Default N = 100')

args = parser.parse_args() 

genuine_taus = args.genuine_taus
maxevents    = args.maxevents
filename     = args.filename
logfreq      = args.logfreq

files = dy_files if genuine_taus else qcd_files
   
if len(filename)==0:
    filename = 'dy_tuple.root' if genuine_taus else 'qcd_tuple.root'

##########################################################################################
# initialise output files to save the flat ntuples
outfile_tau = ROOT.TFile(filename, 'recreate')
branches_all_names = [br.name() for br in branches_all]
ntuple_tau = ROOT.TNtuple('tree', 'tree', ':'.join(branches_all_names))
tofill_tau = OrderedDict(zip(branches_all_names, [-99.]*len(branches_all_names))) # initialise all branches to unphysical -99       

##########################################################################################
# Get ahold of the events
events = ROOT.TChain('Events')
for ifile in files:
    events.Add(ifile)
maxevents = maxevents if maxevents>=0 else events.GetEntries() # total number of events in the files

##########################################################################################
# start looping on the events
start = time()
for i, ev in enumerate(events):
    
    ######################################################################################
    # controls on the events being processed
    if maxevents>0 and i>maxevents:
        break
        
    if i%logfreq==0:
        percentage = float(i)/maxevents*100.
        speed = float(i)/(time()-start)
        eta = datetime.now() + timedelta(seconds=(maxevents-i) / max(0.1, speed))
        print '===> processing %d / %d event \t completed %.1f%s \t %.1f ev/s \t ETA %s s' %(i, maxevents, percentage, '%', speed, eta.strftime('%Y-%m-%d %H:%M:%S'))

    ######################################################################################
    # fill the ntuple: each reco tau makes an entry
    for itau in range(ev.nTau):
        for k, v in tofill_tau.iteritems(): tofill_tau[k] = -99. # initialise before filling

        # per event quantities
        for ibranch in branches_event:
            tofill_tau[ibranch.name()] = ibranch.value(ev)

        # per tau quantities
        for ibranch in branches_tau:
            tofill_tau[ibranch.name()] = ibranch.value(ev)[itau]

        # per gen tau quantities, find the gen visible tau that matches best (if any)
        best_match_idx = -1
        dRmax = 0.3
        for igen in range(ev.nGenVisTau): 
            dR = deltaR(ev.Tau_eta[itau], ev.Tau_phi[itau], ev.GenVisTau_eta[igen], ev.GenVisTau_phi[igen])
            if dR > dRmax: continue
            dRmax = dR
            best_match_idx = igen
        if best_match_idx>=0:
            for ibranch in branches_gen:
                tofill_tau[ibranch.name()] = ibranch.value(ev)[best_match_idx]
 
        # per jet quantities, find the reco jet that matches best, aka tau seed (if any)
        best_match_idx = -1
        dRmax = 0.5
        for ijet in range(ev.nJet): 
            dR = deltaR(ev.Tau_eta[itau], ev.Tau_phi[itau], ev.Jet_eta[ijet], ev.Jet_phi[ijet])
            if dR > dRmax: continue
            dRmax = dR
            best_match_idx = ijet
        if best_match_idx>=0:
            for ibranch in branches_jet:
                tofill_tau[ibranch.name()] = ibranch.value(ev)[best_match_idx]

        # fill the tree
        ntuple_tau.Fill(array('f', prepareBranches(tofill_tau.values())))

##########################################################################################
# write the ntuples and close the files
outfile_tau.cd()
ntuple_tau .Write()
outfile_tau.Close()

