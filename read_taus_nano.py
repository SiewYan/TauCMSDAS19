'''
Loops on the events and operates the matching between reconstructed and generated taus.
It produces two flat ntuples:
    - one with an entry for each gen tau (useful for efficiencies)
    - one with an entry for each reconstructed tau (useful for fake studies)
'''
import ROOT
import struct # convert packed formats to native python https://docs.python.org/2/library/struct.html#struct-format-strings
from array import array
from collections import OrderedDict
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

from treeVariables import branches # here the ntuple branches are defined
from utils import isGenHadTau, finalDaughters, printer # utility functions

##########################################################################################
# initialise output files to save the flat ntuples
outfile_gen = ROOT.TFile('gen_tuple.root', 'recreate')
ntuple_gen = ROOT.TNtuple('tree', 'tree', ':'.join(branches))
tofill_gen = OrderedDict(zip(branches, [-99.]*len(branches))) # initialise all branches to unphysical -99       

outfile_tau = ROOT.TFile('tau_tuple.root', 'recreate')
ntuple_tau = ROOT.TNtuple('tree', 'tree', ':'.join(branches))
tofill_tau = OrderedDict(zip(branches, [-99.]*len(branches))) # initialise all branches to unphysical -99       

# outfile_jet = ROOT.TFile('jet_tuple.root', 'recreate')
# ntuple_jet = ROOT.TNtuple('tree', 'tree', ':'.join(branches))
# tofill_jet = OrderedDict(zip(branches, [-99.]*len(branches))) # initialise all branches to unphysical -99       

##########################################################################################
# Get ahold of the events
events = ROOT.TChain('Events')
events.Add('root://xrootd-cms.infn.it//store/group/phys_tau/ProdNanoAODv4Priv/16dec18/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4Priv-from_102X_upgrade2018_realistic_v15_ver1/181216_125011/0000/myNanoRunMc2018_NANO_99.root') # make sure this corresponds to your file name!
# events.Add('myNanoRunMc2018_NANO_99.root') # make sure this corresponds to your file name!
maxevents = 30000 # max events to process
totevents = min(maxevents, events.GetEntries()) # total number of events in the files

##########################################################################################
# start looping on the events
for i, ev in enumerate(events):
    
    ######################################################################################
    # controls on the events being processed
    if maxevents>0 and i>maxevents:
        break
        
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)

    ######################################################################################
    # fill the ntuple: each gen tau makes an entry
    for igen in range(ev.nGenVisTau):
        for k, v in tofill_gen.iteritems(): tofill_gen[k] = -99. # initialise before filling

        # per event quantities
        tofill_gen['run'  ] = ev.run      
        tofill_gen['lumi' ] = ev.luminosityBlock
        tofill_gen['event'] = ev.event    
        tofill_gen['nvtx' ] = ev.PV_npvsGood

        tofill_gen['gen_vis_tau_eta'             ] = ev.GenVisTau_eta             [igen]
        tofill_gen['gen_vis_tau_mass'            ] = ev.GenVisTau_mass            [igen]
        tofill_gen['gen_vis_tau_phi'             ] = ev.GenVisTau_phi             [igen]
        tofill_gen['gen_vis_tau_pt'              ] = ev.GenVisTau_pt              [igen]
        tofill_gen['gen_vis_tau_charge'          ] = ev.GenVisTau_charge          [igen]
        tofill_gen['gen_vis_tau_genPartIdxMother'] = ev.GenVisTau_genPartIdxMother[igen]
        tofill_gen['gen_vis_tau_status'          ] = ev.GenVisTau_status          [igen]

        # fill the tree
        ntuple_gen.Fill(array('f',tofill_gen.values()))
    
    ######################################################################################
    # fill the ntuple: each gen tau makes an entry
    for itau in range(ev.nTau):
        for k, v in tofill_tau.iteritems(): tofill_tau[k] = -99. # initialise before filling

        # per event quantities
        tofill_tau['run'  ] = ev.run      
        tofill_tau['lumi' ] = ev.luminosityBlock
        tofill_tau['event'] = ev.event    
        tofill_tau['nvtx' ] = ev.PV_npvsGood

        # per tau quantities
        tofill_tau['tau_reco_chargedIso'              ] =                    ev.Tau_chargedIso              [itau]
        tofill_tau['tau_reco_dxy'                     ] =                    ev.Tau_dxy                     [itau]
        tofill_tau['tau_reco_dz'                      ] =                    ev.Tau_dz                      [itau]
        tofill_tau['tau_reco_eta'                     ] =                    ev.Tau_eta                     [itau]
        tofill_tau['tau_reco_leadTkDeltaEta'          ] =                    ev.Tau_leadTkDeltaEta          [itau]
        tofill_tau['tau_reco_leadTkDeltaPhi'          ] =                    ev.Tau_leadTkDeltaPhi          [itau]
        tofill_tau['tau_reco_leadTkPtOverTauPt'       ] =                    ev.Tau_leadTkPtOverTauPt       [itau]
        tofill_tau['tau_reco_mass'                    ] =                    ev.Tau_mass                    [itau]
        tofill_tau['tau_reco_neutralIso'              ] =                    ev.Tau_neutralIso              [itau]
        tofill_tau['tau_reco_phi'                     ] =                    ev.Tau_phi                     [itau]
        tofill_tau['tau_reco_photonsOutsideSignalCone'] =                    ev.Tau_photonsOutsideSignalCone[itau]
        tofill_tau['tau_reco_pt'                      ] =                    ev.Tau_pt                      [itau]
        tofill_tau['tau_reco_puCorr'                  ] =                    ev.Tau_puCorr                  [itau]
        tofill_tau['tau_reco_rawAntiEle'              ] =                    ev.Tau_rawAntiEle              [itau]
        tofill_tau['tau_reco_rawIso'                  ] =                    ev.Tau_rawIso                  [itau]
        tofill_tau['tau_reco_rawIsodR03'              ] =                    ev.Tau_rawIsodR03              [itau]
        tofill_tau['tau_reco_rawMVAnewDM2017v2'       ] =                    ev.Tau_rawMVAnewDM2017v2       [itau]
        tofill_tau['tau_reco_rawMVAoldDM'             ] =                    ev.Tau_rawMVAoldDM             [itau]
        tofill_tau['tau_reco_rawMVAoldDM2017v1'       ] =                    ev.Tau_rawMVAoldDM2017v1       [itau]
        tofill_tau['tau_reco_rawMVAoldDM2017v2'       ] =                    ev.Tau_rawMVAoldDM2017v2       [itau]
        tofill_tau['tau_reco_rawMVAoldDMdR032017v2'   ] =                    ev.Tau_rawMVAoldDMdR032017v2   [itau]
        tofill_tau['tau_reco_charge'                  ] =                    ev.Tau_charge                  [itau]
        tofill_tau['tau_reco_decayMode'               ] =                    ev.Tau_decayMode               [itau]
        tofill_tau['tau_reco_jetIdx'                  ] =                    ev.Tau_jetIdx                  [itau]
        tofill_tau['tau_reco_rawAntiEleCat'           ] =                    ev.Tau_rawAntiEleCat           [itau]
        tofill_tau['tau_reco_idAntiEle'               ] = struct.unpack('B', ev.Tau_idAntiEle               [itau])[0]
        tofill_tau['tau_reco_idAntiMu'                ] = struct.unpack('B', ev.Tau_idAntiMu                [itau])[0]
        tofill_tau['tau_reco_idDecayMode'             ] =                    ev.Tau_idDecayMode             [itau]
        tofill_tau['tau_reco_idDecayModeNewDMs'       ] =                    ev.Tau_idDecayModeNewDMs       [itau]
        tofill_tau['tau_reco_idMVAnewDM2017v2'        ] = struct.unpack('B', ev.Tau_idMVAnewDM2017v2        [itau])[0]
        tofill_tau['tau_reco_idMVAoldDM'              ] = struct.unpack('B', ev.Tau_idMVAoldDM              [itau])[0]
        tofill_tau['tau_reco_idMVAoldDM2017v1'        ] = struct.unpack('B', ev.Tau_idMVAoldDM2017v1        [itau])[0]
        tofill_tau['tau_reco_idMVAoldDM2017v2'        ] = struct.unpack('B', ev.Tau_idMVAoldDM2017v2        [itau])[0]
        tofill_tau['tau_reco_idMVAoldDMdR032017v2'    ] = struct.unpack('B', ev.Tau_idMVAoldDMdR032017v2    [itau])[0]
        tofill_tau['tau_reco_idMVAoldDM2017v2'        ] = struct.unpack('B', ev.Tau_idMVAoldDM2017v2        [itau])[0]
        tofill_tau['tau_reco_idMVAoldDM2017v2'        ] = struct.unpack('B', ev.Tau_idMVAoldDM2017v2        [itau])[0]
        
        tofill_tau['tau_reco_genPartIdx'              ] =                    ev.Tau_genPartIdx              [itau]
        tofill_tau['tau_reco_genPartFlav'             ] = struct.unpack('B', ev.Tau_genPartFlav             [itau])[0]
                
        # fill the tree
        ntuple_tau.Fill(array('f',tofill_tau.values()))


##########################################################################################
# write the ntuples and close the files
outfile_gen.cd()
ntuple_gen .Write()
outfile_gen.Close()

outfile_tau.cd()
ntuple_tau .Write()
outfile_tau.Close()

# outfile_jet.cd()
# ntuple_jet .Write()
# outfile_jet.Close()

