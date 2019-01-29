# Tau POG short exercise @ CMSDAS 2019

The esercise consists of two main parts: first produce flat ntuples containing quantities relevant for tau studies, 
then process these ntuples to produce performance plots.

**You can find the indroductory slides [at this link](https://manzoni.web.cern.ch/manzoni/tau_reconstruction_at_CMSDAS2019.pdf)**

## Outline
* installation
* package content
* how to run the ntupliser on DY and QCD MC
* investigate the ntuples, produce performance plots
* links and references

### Installation

The present package does not depend on `CMSSW`, strictly speaking: basically we only need a working version of `ROOT` and `pyROOT`, plus a
few further python packages. However, `ROOT`is not available as standalone on `gridui{1,2}` therefore it is convenient 
to just rely on `CMSSW`, which comes with everything we need.
In any case, we choose a very recent release CMSSW_10_2_10.

```
cmsrel CMSSW_10_2_10
cd CMSSW_10_2_10/src
cmsenv
git clone git@github.com:rmanzoni/TauCMSDAS19.git
cd TauCMSDAS19
```

If you'd like to contribute to this package (and you're more than welcome to do so!)
you may want to first `fork` this repository, then replace
```
git clone git@github.com:rmanzoni/TauCMSDAS19.git
```
with
```
git clone git@github.com:YOUR_GITHUB_NAME/TauCMSDAS19.git
```
in the instructions above.
You can submit your changes to this package as pull requests.

### Package content

In the `TauCMSDAS19` directory you'll find the following files:
* `read_taus_nano.py` is the ntupliser, you'll have to run this python script to produce your own ntuples (details in the next section)
* `treeVariables.py` where the branches of the output flat ntuples are defined. Here you can adjust the event content to your taste, 
e.g. adding more information into the flat ntuple, as well as you can see how the information is fetched from the original `NanoAOD`
* `files.py` and `deltar.py` are utils to fetch the original `NanoAOD`s and to compute deltaR repectively. Ideally you won't need to touch them at all
* `branches.txt` is a snapshot of the documentation of the `NanoAOD` content. Very useful if you want to know what's what
* `tau_plotting.ipynb` jupyter notebook with step by step comments and code snippets to produce performance plots

### Run the ntupliser

The ntupliser reads `NanoAOD` files stored on the shared file sistem in Pisa 
at `/gpfs/ddn/cms/user/cmsdas/2019/TauExercise/{dy, qcd}` and produces flat ntuples where each reco tau makes 
an entry.  

Side note: these samples are a (partial) local copy of these, normally published and hence accessible from anywhere, [QCD](https://cmsweb.cern.ch/das/request?input=dataset%3D%2FQCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8%2Fmanzoni-RunIIAutumn18NanoAODv4Priv-from_102X_upgrade2018_realistic_v15_ext1_ver1-fef0eb32e058a18d2c275120191b003f%2FUSER&instance=prod/phys03) and [DY](https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8%2Fmanzoni-RunIIAutumn18NanoAODv4Priv-from_102X_upgrade2018_realistic_v15_ver1-fef0eb32e058a18d2c275120191b003f%2FUSER&instance=prod/phys03) samples.

The choice to read off `NanoAOD` is based on different reasons:
* it is a lightweght, centrally produced (and validated) format
* Tau POG is moving towards larger adoption of `NanoAOD`, especially for performance measurements

**Everything is already setup for you and, in principle, you just need to push a button, _however you're encouraged to 
dig into the code_ (it's very straightforward and hopefully well documented) _and try to understand the basics_.**

**In short, this is all you need to produce the ntuple**
```
ipython -i -- read_taus_nano.py --dy --maxevents 1000000 --logfreq 1000
ipython -i -- read_taus_nano.py --qcd --maxevents 1000000 --logfreq 1000
```
Notice that eventually you'll need to produce _two_ ntuples, one from DY, to have a sample of genuine taus, 
and one from QCD, to have a large sample of jets faking taus.

### Performance plots

A jupyter notebook are guided step by step towards producing 
a few performance plots which are typical Tau POG bread 'n' butter: efficiencies, fake rates, ROC curves and more.

You can visualise the content of the jupiter notebook at this link
https://github.com/rmanzoni/TauCMSDAS19/blob/master/tau_plotting.ipynb

The notebook contains comments, questions, instructions _and_ the code to produce the plots.
During the exercise we'll gothrough the notebook together and you'll be encouraged to find your own
code implementation to satisfy the requests.  
You can always look at the official code snippets, they're in the notebook itself, 
but only do it as last resort and give yourself a chance to learn by trying in first person!

### Links and references

**Tau POG on indico**  
https://indico.cern.ch/category/6330/

**Main Tau POG TWiki**  
https://twiki.cern.ch/twiki/bin/view/CMS/Tau

**Recipes and recommendations**  
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV

**Software guide**  
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID

**Tau long exercise at 2017 CMS Physics Object School**  
For a more extensive plunge in Tau realm, including accessing to the information stored in MiniAOD, rerunning the HPS algorithm and more, see:  
https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSPhysicsObjectSchoolBARI2017Tau  
https://github.com/rmanzoni/TauRecoCMSPOS

