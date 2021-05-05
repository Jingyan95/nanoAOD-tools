import sys
import os
import subprocess
import readline
import string

data2018_samples = {}
mc2018_samples = {}
#data2018_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw']

mc2018_samples['2018_DYM10to50'] = [['/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2018/200612_143346/0000/'], 'mc','','2018', '','18610','59.97','39392062' ]  #'79058069' ] #39521230'] ## '78,994,955' ## <-  is event number from miniaod, we must be missing an extension

mc2018_samples['2018_DYM50'] = [['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2018/200612_144037/0000/'], 'mc','','2018', '','5765.4','59.97','997561']

## example nanoAOD datset on DAS where I got number of events from
## https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fphys03&input=dataset+%3D+%2FTTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8%2Fpalencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc%2FUSER
mc2018_samples['2018_TTTo2L2Nu'] = [['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2018/200610_155014/0000/'], 'mc','','2018', '','87.31','59.97', '64310000' ] ##'8926992'] what is going on with number of events?

mc2018_samples['2018_ST_tW'] = [['/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2018/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2018/200610_154723/0000/'], 'mc','','2018', '','19.47','59.97','7636887']

mc2018_samples['2018_ST_atW'] = [['/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2018/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2018/200610_154501/0000/'], 'mc','','2018', '','19.47','59.97','5823328']

mc2018_samples['2018_WWTo2L2Nu'] = [['/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2018/200612_152152/0000/'], 'mc','','2018', '','12.178','59.97','7758900']

mc2018_samples['2018_ZZTo2L2Nu'] = [['/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2018/200612_153300/0000/'], 'mc','','2018', '','0.564','59.97','8382600']

mc2018_samples['2018_ZZTo4L'] = [['/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2018/200612_153449/0000/'], 'mc','','2018', '','1.212','59.97','6689900']

mc2018_samples['2018_WZTo2L2Q'] = [['/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2018/200612_152539/0000/'], 'mc','','2018', '','5.595','59.97','28193648']

#This NanoAOD dataset has two parent datasets. The dataset name is used to locate samples.
#mc2018_samples['2018_WZTo3LNu'] = [['/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2018/200612_152609/0000/','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2018/200612_152635/0000/'], 'mc','','2018', '','4.43','59.97','21997587']

mc2018_samples['2018_WZTo3LNu'] = [['/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2018/200612_152609/0000/'], 'mc','','2018', '','4.43','59.97','21997587']

mc2018_samples['2018_WJetsToLNu'] = [['/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2018/200612_152023/0000/'], 'mc','','2018', '','61526.7','59.97','71026861']

mc2018_samples['2018_TTWJetsToQQ'] = [['/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2018/200612_151146/0000/'], 'mc','','2018', '','0.4062','59.97','835296']

mc2018_samples['2018_TTWJetsToLNu'] = [['/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2018/200612_151120/0000/'], 'mc','','2018', '','0.2043','59.97', '4911941' ] #'9920372']  #'4925829']

mc2018_samples['2018_TTZToLLNuNu'] = [['/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2018/200612_151317/0000/' ], 'mc','','2018', '','0.2529','59.97','13280000']

mc2018_samples['2018_TTZToQQ'] = [['/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/balvarez-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc/USER','/store/user/balvarez/topNanoAOD/v6-1-1/2018/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2018/200612_151411/0000/' ], 'mc','','2018', '','0.5297','59.97', '750000']


#For NanoAOD 2018 datasets, run A-C are combined into one single dataset. For now we ignore the era information and use dataset name to locate samples.
#data2018_samples['2018_A_MuonEG'] = [['/MuonEG/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/MuonEG/TopNanoAODv6-1-2_2018/200624_140935/0000/'], 'data','MuonEG','2018', 'A','1','1','1']
#data2018_samples['2018_B_MuonEG'] = [['/MuonEG/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/MuonEG/TopNanoAODv6-1-2_2018/200624_141001/0000/'], 'data','MuonEG','2018', 'B','1','1','1']
#data2018_samples['2018_C_MuonEG'] = [['/MuonEG/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/MuonEG/TopNanoAODv6-1-2_2018/200624_141030/0000/'], 'data','MuonEG','2018', 'C','1','1','1']
data2018_samples['2018_A_MuonEG'] = [['/MuonEG/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/MuonEG/TopNanoAODv6-1-2_2018/200624_140935/0000/'], 'data','MuonEG','2018', 'ABC','1','1','1']
data2018_samples['2018_D_MuonEG'] = [['/MuonEG/palencia-TopNanoAODv6-1-2_2018-831765d0aa9cd559fee11ff659127d4e/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/MuonEG/TopNanoAODv6-1-2_2018/200624_141057/0000/'], 'data','MuonEG','2018', 'D','1','1','1']


#data2018_samples['2018_A_SingleMuon'] = [['/SingleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/SingleMuon/TopNanoAODv6-1-2_2018/200624_141127/0000/'], 'data','SingleMuon','2018', 'A','1','1','1']
#data2018_samples['2018_B_SingleMuon'] = [['/SingleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/SingleMuon/TopNanoAODv6-1-2_2018/200624_141153/0000/'], 'data','SingleMuon','2018', 'B','1','1','1']
#data2018_samples['2018_C_SingleMuon'] = [['/SingleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/SingleMuon/TopNanoAODv6-1-2_2018/200624_141221/0000/'], 'data','SingleMuon','2018', 'C','1','1','1']
data2018_samples['2018_A_SingleMuon'] = [['/SingleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/SingleMuon/TopNanoAODv6-1-2_2018/200624_141127/0000/'], 'data','SingleMuon','2018', 'ABC','1','1','1']
data2018_samples['2018_D_SingleMuon'] = [['/SingleMuon/palencia-TopNanoAODv6-1-2_2018-831765d0aa9cd559fee11ff659127d4e/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/SingleMuon/TopNanoAODv6-1-2_2018/200624_141247/0000/'], 'data','SingleMuon','2018', 'D','1','1','1']


#data2018_samples['2018_A_EGamma'] = [['/EGamma/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/EGamma/TopNanoAODv6-1-2_2018/200624_140405/0000/'], 'data','EGamma','2018', 'A','1','1','1']
#data2018_samples['2018_B_EGamma'] = [['/EGamma/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/EGamma/TopNanoAODv6-1-2_2018/200624_140434/0000/'], 'data','EGamma','2018', 'B','1','1','1']
#data2018_samples['2018_C_EGamma'] = [['/EGamma/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/EGamma/TopNanoAODv6-1-2_2018/200624_140502/0000/'], 'data','EGamma','2018', 'C','1','1','1']
data2018_samples['2018_A_EGamma'] = [['/EGamma/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/EGamma/TopNanoAODv6-1-2_2018/200624_140405/0000/'], 'data','EGamma','2018', 'ABC','1','1','1']
data2018_samples['2018_D_EGamma'] = [['/EGamma/palencia-TopNanoAODv6-1-2_2018-831765d0aa9cd559fee11ff659127d4e/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/EGamma/TopNanoAODv6-1-2_2018/200624_140530/0000/'], 'data','EGamma','2018', 'D','1','1','1']


#data2018_samples['2018_A_DoubleMu'] = [['/DoubleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/DoubleMuon/TopNanoAODv6-1-2_2018/200624_140222/0000/'], 'data','DoubleMu','2018', 'A','1','1','1']
#data2018_samples['2018_B_DoubleMu'] = [['/DoubleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/DoubleMuon/TopNanoAODv6-1-2_2018/200624_140247/0000/'], 'data','DoubleMu','2018', 'B','1','1','1']
#data2018_samples['2018_C_DoubleMu'] = [['/DoubleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/DoubleMuon/TopNanoAODv6-1-2_2018/200624_140313/0000/'], 'data','DoubleMu','2018', 'C','1','1','1']
data2018_samples['2018_A_DoubleMu'] = [['/DoubleMuon/palencia-TopNanoAODv6-1-2_2018-2667fe41f354e79b08df8a25806ccf17/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/DoubleMuon/TopNanoAODv6-1-2_2018/200624_140222/0000/'], 'data','DoubleMu','2018', 'ABC','1','1','1']
data2018_samples['2018_D_DoubleMu'] = [['/DoubleMuon/palencia-TopNanoAODv6-1-2_2018-831765d0aa9cd559fee11ff659127d4e/USER','/store/group/phys_top/topNanoAOD/v6-1-2/2018/DoubleMuon/TopNanoAODv6-1-2_2018/200624_140340/0000/'], 'data','DoubleMu','2018', 'D','1','1','1']


## Vector-like signal
mc2018_samples['2018_LFVStVecC'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210504_095637/0000/'], 'mc','','2018', '','0.0512','59.97','500000']
mc2018_samples['2018_LFVStVecU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_121320/0000/'], 'mc','','2018', '','0.515','59.97','500000']
mc2018_samples['2018_LFVTtVecC'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_122034/0000/'], 'mc','','2018', '','0.032','59.97','500000']
mc2018_samples['2018_LFVTtVecU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210504_070719/0000/'], 'mc','','2018', '','0.032','59.97','500000']

## Scalar-like signal
mc2018_samples['2018_LFVStScalarC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210428_182921/0000/'], 'mc','','2018', '','0.008' ,'59.97','500000']
mc2018_samples['2018_LFVStScalarU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210505_091252/0000/'], 'mc','','2018', '','0.102' ,'59.97','500000']
mc2018_samples['2018_LFVTtScalarC'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_121911/0000/'], 'mc','','2018', '','0.004' ,'59.97','500000']
mc2018_samples['2018_LFVTtScalarU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_122205/0000/'], 'mc','','2018', '','0.004' ,'59.97','500000']

## Tensor-like signal
mc2018_samples['2018_LFVStTensorC'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_121608/0000/'], 'mc','','2018', '','0.187' ,'59.97','500000']
mc2018_samples['2018_LFVStTensorU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_122128/0000/'], 'mc','','2018', '','1.900' ,'59.97','500000']
mc2018_samples['2018_LFVTtTensorC'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210505_090452/0000/'], 'mc','','2018', '','0.1876','59.97','500000']
mc2018_samples['2018_LFVTtTensorU'] = [['/eos/user/a/asparker/TopLFV_nanoAOD/v6-1-1/2018/CRAB_UserFiles/TopNanoAODv6-1-1_2018/210430_121500/0000/'], 'mc','','2018', '','0.1876','59.97','500000']


