'''
Loops on the events and operates the matching between reconstructed and generated taus.
It produces two flat ntuples:
    - one with an entry for each gen tau (useful for efficiencies)
    - one with an entry for each reconstructed tau (useful for fake studies)
'''
import ROOT
from time import time
from array import array
from objects import createGenVisTau, GenVisTau, Particle, GenParticle
from collections import OrderedDict
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

# here the ntuple branches, and how to get the quantities stored in such branches, are defined
from treeVariables import branches_event, branches_tau, branches_gen, branches_jet, branches_all, prepareBranches
from files import dy_files as files

##########################################################################################
# initialise output files to save the flat ntuples
outfile_tau = ROOT.TFile('tau_tuple.root', 'recreate')
branches_all_names = [br.name() for br in branches_all]
ntuple_tau = ROOT.TNtuple('tree', 'tree', ':'.join(branches_all_names))
tofill_tau = OrderedDict(zip(branches_all_names, [-99.]*len(branches_all_names))) # initialise all branches to unphysical -99       

##########################################################################################
# Get ahold of the events
events = ROOT.TChain('Events')
for ifile in files:
    events.Add(ifile)
maxevents = 10000 # max events to process
totevents = events.GetEntries() if maxevents>=0 else events.GetEntries() # total number of events in the files

##########################################################################################
# start looping on the events
start = time()
for i, ev in enumerate(events):
    
    ######################################################################################
    # controls on the events being processed
    if maxevents>0 and i>maxevents:
        break
        
    if i%100==0:
        print '===> processing %d / %d event \t completed %.1f%s \t %.1f ev/s' %(i, maxevents, float(i)/maxevents*100., '%', float(i)/(time()-start))

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


#         if ev.nGenVisTau>0:
#             print '=========RECO TAU========='
#             print '\t reco had tau index %d' %itau
#             print '\t\t pt         \t%.2f' %ev.Tau_pt         [itau]
#             print '\t\t eta        \t%.2f' %ev.Tau_eta        [itau]
#             print '\t\t phi        \t%.2f' %ev.Tau_phi        [itau]
#             print '\t\t mass       \t%.2f' %ev.Tau_mass       [itau]
#             print '\t\t decay mode \t%.2f' %ev.Tau_decayMode  [itau]
#             print '\t\t charge     \t%d'   %ev.Tau_charge     [itau]
#             print '\t\t genp index \t%d'   %ev.Tau_genPartIdx [itau]
#             print '\t\t genp flavo \t%d'   %struct.unpack('B', ev.Tau_genPartFlav[itau])[0]
#             print ''
#             print '=========GEN TAU========='
#             for igen in range(ev.nGenVisTau): 
#                 print '\t gen had tau index %d' %igen
#                 print '\t\t pt         \t%.2f' %ev.GenVisTau_pt              [igen]
#                 print '\t\t eta        \t%.2f' %ev.GenVisTau_eta             [igen]
#                 print '\t\t phi        \t%.2f' %ev.GenVisTau_phi             [igen]
#                 print '\t\t mass       \t%.2f' %ev.GenVisTau_mass            [igen]
#                 print '\t\t charge     \t%d'   %ev.GenVisTau_charge          [igen]
#                 print '\t\t genp index \t%d'   %ev.GenVisTau_genPartIdxMother[igen]
#                 print '\t\t decayMode  \t%d'   %ev.GenVisTau_status          [igen]
#             import pdb ; pdb.set_trace()

