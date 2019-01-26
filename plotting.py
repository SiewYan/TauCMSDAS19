import ROOT
import numpy as np

ROOT.TH1.SetDefaultSumw2()

# set to True for non graphical mode (useful if the connection is slow
# or you don't want TCanvases popping up all over the place)
ROOT.gROOT.SetBatch(True) 

# dy_file = ROOT.TFile.Open('dy_tree.root', 'read')
dy_file = ROOT.TFile.Open('dy_tuple.root.backup', 'read')
dy_file.cd()
dy_tree = dy_file.Get('tree')

##########################################################################################
# First, let's plot the isolation efficiency for genuine taus
##########################################################################################

# Reconstruct the WP <--> value in the branch correspondance
# may look strange as effect of bitmasking
# can be remapped to 0 - 6 through np.log2((tau_idMVAnewDM2017v2 + 1)>>1)
# idMVAnewDM2017v2 WPs
# 0    not passed
# 1    VVLoose 
# 3    VLoose 
# 7    Loose  
# 15   Medium  
# 31   Tight   
# 63   VTight  
# 127  VVTight 

# choose a variable binning for the pt distribution
# Q: why variable?
pt_binning = np.array([0., 18., 20., 22., 24., 26., 28., 30., 35., 40., 50., 70., 200.])

# Select genuine taus, based on gen level information, 
# that is, if a gen visible tau is matched to the reco tau
true_tau_selection = 'tau_gen_pt>=0' # unmatched taus are set to default -99.

# Define the denominator and numerator selections
# Consider only taus with pt>18 GeV. 
# This is the minimum recommended pt for which the HPS algorithm is guaranteed to work 
den_selection = '&'.join(['tau_pt>18', 'abs(tau_eta)<2.3', true_tau_selection])
# at the numerator, count taus that pass your preferred isolation WP
num_selection = '&'.join([den_selection, 'tau_idMVAnewDM2017v2 >= 63'])

# Define numerator and denominator histograms.
# Nota Bene: they must have the same binning 
histo_iso_pt_den = ROOT.TH1F('iso_pt_den', '', len(pt_binning)-1, pt_binning)
histo_iso_pt_num = ROOT.TH1F('iso_pt_num', '', len(pt_binning)-1, pt_binning)

# Select the events from the tree and draw the histograms
# This method is typically much faster than looping 
dy_tree.Draw('tau_pt >> iso_pt_den', den_selection)
dy_tree.Draw('tau_pt >> iso_pt_num', num_selection)

# Divide num / den
# Prefer using ROOT's TEfficiency
# https://root.cern.ch/doc/master/classTEfficiency.html
iso_efficiency = ROOT.TEfficiency(histo_iso_pt_num, histo_iso_pt_den) # Q: can different constructors be used? Check with ipython: ROOT.TEfficiency?
iso_efficiency.SetLineColor(ROOT.kRed)
iso_efficiency.SetFillColor(0)
iso_efficiency.Draw('apl')
ROOT.gPad.Update()
iso_efficiency.SetTitle('MVA 2017v2; reco #tau p_{T} [GeV]; efficiency') 
iso_efficiency.GetPaintedGraph().GetYaxis().SetRangeUser(0, 1.)
ROOT.gPad.Update()

# be a better person, always add a legend
leg = ROOT.TLegend(.5,.7,.88,.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(iso_efficiency, 'MVA 2017v2 Tau ID - VTight WP')
leg.Draw('same')

ROOT.gPad.SaveAs('tau_iso_eff_pt.pdf')

##########################################################################################
# Now, let's check the PU dependency
##########################################################################################

pu_binning = np.array([0., 10.] + range(12, 46, 2) + [50., 70.])

# Select genuine taus, based on gen level information, 
# that is, if a gen visible tau is matched to the reco tau
true_tau_selection = 'tau_gen_pt>=0' # unmatched taus are set to default -99.

# Define the denominator and numerator selections
# Consider only taus with pt>18 GeV. 
# This is the minimum recommended pt for which the HPS algorithm is guaranteed to work 
den_selection = '&'.join(['tau_pt>18', 'abs(tau_eta)<2.3', true_tau_selection])
# at the numerator, count taus that pass your preferred isolation WP
num_selection = '&'.join([den_selection, 'tau_idMVAnewDM2017v2 >= 63'])

# Define numerator and denominator histograms.
# Nota Bene: they must have the same binning 
histo_iso_pu_den = ROOT.TH1F('iso_pu_den', '', len(pu_binning)-1, pu_binning)
histo_iso_pu_num = ROOT.TH1F('iso_pu_num', '', len(pu_binning)-1, pu_binning)

# Notice that now we plot the number of good vertices!
dy_tree.Draw('ngvtx >> iso_pu_den', den_selection)
dy_tree.Draw('ngvtx >> iso_pu_num', num_selection)

# Divide num / den
# Prefer using ROOT's TEfficiency
# https://root.cern.ch/doc/master/classTEfficiency.html
iso_efficiency = ROOT.TEfficiency(histo_iso_pu_num, histo_iso_pu_den) # Q: can different constructors be used? Check with ipython: ROOT.TEfficiency?
iso_efficiency.SetLineColor(ROOT.kRed)
iso_efficiency.Draw('apl')
iso_efficiency.SetFillColor(0)
ROOT.gPad.Update()
iso_efficiency.SetTitle('MVA 2017v2; number of good PV; efficiency') 
iso_efficiency.GetPaintedGraph().GetYaxis().SetRangeUser(0, 1.)
ROOT.gPad.Update()

# be a better person, always add a legend
leg = ROOT.TLegend(.5,.7,.88,.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(iso_efficiency, 'MVA 2017v2 Tau ID - VTight WP')
leg.Draw('same')

ROOT.gPad.SaveAs('tau_iso_eff_pu.pdf')
