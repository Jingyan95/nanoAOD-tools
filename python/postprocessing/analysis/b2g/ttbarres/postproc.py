#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.b2g.ttbarres.TTbarResAnaHadronic import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.examples.puWeightProducer import *

#files=["root://cms-xrd-global.cern.ch//store/user/arizzi/NanoTestProd006/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X-NanoCrabProd006/171006_144159/0000/nanolzma_1.root"]
#files=["lzma_1.root"]
#files=["root://cms-xrd-global.cern.ch://store/user/arizzi/NanoTestProd004/WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8/NanoCrabProd004/171002_120520/0000/lzma_1.root"]
files=["/data/NanoAOD/test94X_NANO.root"]
#files=["root://cms-xrd-global.cern.ch://store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/NanoCrabProd004/171002_120644/0000/lzma_1.root"]
#files=["root://cms-xrd-global.cern.ch://store/user/arizzi/NanoTestProd004/ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/NanoCrabProd004/171002_122256/0000/lzma_1.root"]
#files=["root://cms-xrd-global.cern.ch://store/user/arizzi/NanoTestProd004/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/NanoCrabProd004/171002_122221/0000/lzma_1.root"]


import random
random.seed(12345)

#p=PostProcessor(".",files,selection.replace('\n',' '),"keep_and_drop.txt",[btagSFProducer("cmva"),jecUncertAll_cppOut(),ttbarres()],provenance=True)
#p1=PostProcessor(".",files,'',"keep_and_drop.txt",[puWeight(),jetmetUncertainties(),TTbarResAnaHadronic(writePredDist=True)],provenance=False, noOut=True,histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')
p1=PostProcessor(".",files,'',"keep_and_drop.txt",[puWeight(),TTbarResAnaHadronic(writePredDist=True)],provenance=False, histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')


#p2=PostProcessor(".",['test94X_NANO_addPU.root'],'',"keep_and_drop.txt",[TTbarResAnaHadronic()],provenance=False, noOut=True,histFileName='hists.root', histDirName='ttbarres', postfix='predread')

p1.run()
#p2.run()