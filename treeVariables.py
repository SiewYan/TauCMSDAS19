'''
In this file you can define the branch to be included in the flat ntuple.
You can find some basic quantities here, expand with more specific observables,
such as isolation etc...

Check NanoAOD content here
https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau
'''
import numpy as np
import struct # convert packed formats to native python https://docs.python.org/2/library/struct.html#struct-format-strings

class Variable(object):
    
    def __init__(self, name, getter):
        self._name   = name
        self._getter = getter
    
    def name(self):
        return self._name
    
    def value(self, event):
        return self._getter(event)


def prepareBranches(values):
    new_values = []
    for ivalue in values:
        if isinstance(ivalue, long):
            ivalue = long(ivalue)
        if isinstance(ivalue, bool):
            ivalue = int(ivalue)
        if isinstance(ivalue, str):
            ivalue = np.log2(struct.unpack('B', ivalue)[0] + 1)
        new_values.append(ivalue)
    return new_values
 

branches_event = [
    Variable('run'                         , lambda ev : ev.run                         ),
    Variable('lumi'                        , lambda ev : ev.luminosityBlock             ),
    Variable('event'                       , lambda ev : ev.event                       ),
    Variable('ngvtx'                       , lambda ev : ev.PV_npvsGood                 ),
    Variable('rho'                         , lambda ev : ev.fixedGridRhoFastjetAll      ),
]

branches_tau = [
    Variable('tau_pt'                      , lambda ev : ev.Tau_pt                      ),
    Variable('tau_eta'                     , lambda ev : ev.Tau_eta                     ),
    Variable('tau_phi'                     , lambda ev : ev.Tau_phi                     ),
    Variable('tau_mass'                    , lambda ev : ev.Tau_mass                    ),
    Variable('tau_dxy'                     , lambda ev : ev.Tau_dxy                     ),
    Variable('tau_dz'                      , lambda ev : ev.Tau_dz                      ),
    Variable('tau_charge'                  , lambda ev : ev.Tau_charge                  ),
    Variable('tau_decayMode'               , lambda ev : ev.Tau_decayMode               ),
    Variable('tau_chargedIso'              , lambda ev : ev.Tau_chargedIso              ),
    Variable('tau_leadTkDeltaEta'          , lambda ev : ev.Tau_leadTkDeltaEta          ),
    Variable('tau_leadTkDeltaPhi'          , lambda ev : ev.Tau_leadTkDeltaPhi          ),
    Variable('tau_leadTkPtOverTauPt'       , lambda ev : ev.Tau_leadTkPtOverTauPt       ),
    Variable('tau_neutralIso'              , lambda ev : ev.Tau_neutralIso              ),
    Variable('tau_photonsOutsideSignalCone', lambda ev : ev.Tau_photonsOutsideSignalCone),
    Variable('tau_puCorr'                  , lambda ev : ev.Tau_puCorr                  ),
    Variable('tau_rawAntiEle'              , lambda ev : ev.Tau_rawAntiEle              ),
    Variable('tau_rawIso'                  , lambda ev : ev.Tau_rawIso                  ),
    Variable('tau_rawMVAnewDM2017v2'       , lambda ev : ev.Tau_rawMVAnewDM2017v2       ),
    Variable('tau_rawAntiEleCat'           , lambda ev : ev.Tau_rawAntiEleCat           ),
    Variable('tau_idAntiEle'               , lambda ev : ev.Tau_idAntiEle               ),
    Variable('tau_idAntiMu'                , lambda ev : ev.Tau_idAntiMu                ),
    Variable('tau_idMVAnewDM2017v2'        , lambda ev : ev.Tau_idMVAnewDM2017v2        ),
    Variable('tau_genPartIdx'              , lambda ev : ev.Tau_genPartIdx              ),
    Variable('tau_genPartFlav'             , lambda ev : ev.Tau_genPartFlav             ),
]

##########################################################################################
# Add more branches, most of them are not recommended isolation discriminators
# branches_tau += [
#     Variable('tau_jetIdx'                  , lambda ev : ev.Tau_jetIdx                  ),
#     Variable('tau_rawIsodR03'              , lambda ev : ev.Tau_rawIsodR03              ),
#     Variable('tau_rawMVAoldDM'             , lambda ev : ev.Tau_rawMVAoldDM             ),
#     Variable('tau_rawMVAoldDM2017v1'       , lambda ev : ev.Tau_rawMVAoldDM2017v1       ),
#     Variable('tau_rawMVAoldDM2017v2'       , lambda ev : ev.Tau_rawMVAoldDM2017v2       ),
#     Variable('tau_rawMVAoldDMdR032017v2'   , lambda ev : ev.Tau_rawMVAoldDMdR032017v2   ),
#     Variable('tau_idDecayMode'             , lambda ev : ev.Tau_idDecayMode             ),
#     Variable('tau_idDecayModeNewDMs'       , lambda ev : ev.Tau_idDecayModeNewDMs       ),
#     Variable('tau_idMVAoldDM'              , lambda ev : ev.Tau_idMVAoldDM              ),
#     Variable('tau_idMVAoldDM2017v1'        , lambda ev : ev.Tau_idMVAoldDM2017v1        ),
#     Variable('tau_idMVAoldDM2017v2'        , lambda ev : ev.Tau_idMVAoldDM2017v2        ),
#     Variable('tau_idMVAoldDMdR032017v2'    , lambda ev : ev.Tau_idMVAoldDMdR032017v2    ),
# ] 

branches_gen = [
    Variable('tau_gen_pt'                  , lambda ev : ev.GenVisTau_pt                ),
    Variable('tau_gen_eta'                 , lambda ev : ev.GenVisTau_eta               ),
    Variable('tau_gen_phi'                 , lambda ev : ev.GenVisTau_phi               ),
    Variable('tau_gen_mass'                , lambda ev : ev.GenVisTau_mass              ),
    Variable('tau_gen_charge'              , lambda ev : ev.GenVisTau_charge            ),
    Variable('tau_gen_decayMode'           , lambda ev : ev.GenVisTau_status            ),
]        

branches_jet = [
    Variable('tau_jet_pt'                  , lambda ev : ev.Jet_pt                      ),
    Variable('tau_jet_eta'                 , lambda ev : ev.Jet_eta                     ),
    Variable('tau_jet_phi'                 , lambda ev : ev.Jet_phi                     ),
    Variable('tau_jet_mass'                , lambda ev : ev.Jet_mass                    ),
]

branches_all = branches_event + branches_tau + branches_gen + branches_jet
