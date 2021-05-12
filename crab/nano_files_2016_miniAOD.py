import sys
import os
import subprocess
import readline
import string

data2016_samples = {}
mc2016_samples = {}
#data2016_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw']

#2016 MC
mc2016_samples['2016_DYM10to50'] = [['/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'], 'mc','','2016', '','18610','35.92','68733117']
mc2016_samples['2016_DYM50'] = [['/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'], 'mc','','2016', '','5765.4','35.92','120777245']
mc2016_samples['2016_TTTo2L2Nu'] = [['/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'], 'mc','','2016', '','87.31','35.92','79140880']
mc2016_samples['2016_ST_tW'] = [['/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'], 'mc','','2016', '','19.47','35.92','5424845']
mc2016_samples['2016_ST_atW'] = [['/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'], 'mc','','2016', '','19.47','35.92','5665802']
mc2016_samples['2016_WWTo2L2Nu'] = [['/WWTo2L2Nu_13TeV-powheg/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM '], 'mc','','2016', '','12.178','35.92','1999000']
mc2016_samples['2016_ZZTo4L'] = [['/ZZTo4L_13TeV_powheg_pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'], 'mc','','2016', '','1.212','35.92','6669988']
mc2016_samples['2016_WZTo2L2Q'] = [['/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'], 'mc','','2016', '','5.595','35.92','26517272']
mc2016_samples['2016_WJetsToLNu'] = [['/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM'], 'mc','','2016', '','61526.7','35.92','57402435']
mc2016_samples['2016_TTWJetsToLNu'] = [['/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'], 'mc','','2016', '','0.2043','35.92','3120397']
mc2016_samples['2016_TTZToLLNuNu'] = [['/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'], 'mc','','2016', '','0.2529','35.92','7324824']
mc2016_samples['2016_TTZToQQ'] = [['/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/schoef-TopNanoAODv6-1-2-2_2016-88146d75cb10601530484643de5f7795/USER','/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'], 'mc','','2016', '','0.5297','35.92','749400']



data2016_samples['2016_B_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016B_ver2-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016B-17Jul2018_ver2-v1/MINIAOD'], 'data','MuonEG','2016', 'B','1','1','1']
data2016_samples['2016_C_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016C-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016C-17Jul2018-v1/MINIAOD'], 'data','MuonEG','2016', 'C','1','1','1']
data2016_samples['2016_E_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016E-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016E-17Jul2018-v2/MINIAOD'], 'data','MuonEG','2016', 'E','1','1','1']
data2016_samples['2016_F_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016F-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016F-17Jul2018-v1/MINIAOD'], 'data','MuonEG','2016', 'F','1','1','1']
data2016_samples['2016_G_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016G-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016G-17Jul2018-v1/MINIAOD'], 'data','MuonEG','2016', 'G','1','1','1']
data2016_samples['2016_H_MuonEG'] = [['/MuonEG/schoef-TopNanoAODv6-1-2-4_MuonEG_Run2016H-ba7e3129b1ff910ad1abce6981b33804/USER','/MuonEG/Run2016H-17Jul2018-v1/MINIAOD'], 'data','MuonEG','2016', 'H','1','1','1']


data2016_samples['2016_B_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016B_ver2-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD'], 'data','SingleMuon','2016', 'B','1','1','1']
data2016_samples['2016_C_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016C-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD'], 'data','SingleMuon','2016', 'C','1','1','1']
data2016_samples['2016_D_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016D-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD'], 'data','SingleMuon','2016', 'D','1','1','1']
data2016_samples['2016_E_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016E-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD'], 'data','SingleMuon','2016', 'E','1','1','1']
data2016_samples['2016_G_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016G-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD'], 'data','SingleMuon','2016', 'G','1','1','1']
data2016_samples['2016_H_SingleMuon'] = [['/SingleMuon/schoef-TopNanoAODv6-1-2-4_SingleMuon_Run2016H-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD'], 'data','SingleMuon','2016', 'H','1','1','1']


data2016_samples['2016_C_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016C-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD'], 'data','SingleElectron','2016', 'C','1','1','1']
data2016_samples['2016_D_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016D-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD'], 'data','SingleElectron','2016', 'D','1','1','1']
data2016_samples['2016_E_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016E-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD'], 'data','SingleElectron','2016', 'E','1','1','1']
data2016_samples['2016_F_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016F-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD'], 'data','SingleElectron','2016', 'F','1','1','1']
data2016_samples['2016_G_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016G-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD'], 'data','SingleElectron','2016', 'G','1','1','1']
data2016_samples['2016_H_SingleElectron'] = [['/SingleElectron/schoef-TopNanoAODv6-1-2-4_SingleElectron_Run2016H-ba7e3129b1ff910ad1abce6981b33804/USER','/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD '], 'data','SingleElectron','2016', 'H','1','1','1']


data2016_samples['2016_B_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016B_ver2-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016B-17Jul2018_ver2-v1/MINIAOD'], 'data','DoubleEG','2016', 'B','1','1','1']
data2016_samples['2016_C_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016C-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016C-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'C','1','1','1']
data2016_samples['2016_D_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016D-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016D-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'D','1','1','1']
data2016_samples['2016_E_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016E-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016E-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'E','1','1','1']
data2016_samples['2016_F_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016F-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016F-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'F','1','1','1']
data2016_samples['2016_G_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016G-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016G-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'G','1','1','1']
data2016_samples['2016_H_DoubleEG'] = [['/DoubleEG/schoef-TopNanoAODv6-1-2-4_DoubleEG_Run2016H-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleEG/Run2016H-17Jul2018-v1/MINIAOD'], 'data','DoubleEG','2016', 'H','1','1','1']


data2016_samples['2016_B_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016B_ver2-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD'], 'data','DoubleMu','2016', 'B','1','1','1']
data2016_samples['2016_C_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016C-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016C-17Jul2018-v1/MINIAOD'], 'data','DoubleMu','2016', 'C','1','1','1']
data2016_samples['2016_D_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016D-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016D-17Jul2018-v1/MINIAOD'], 'data','DoubleMu','2016', 'D','1','1','1']
data2016_samples['2016_F_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016F-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016F-17Jul2018-v1/MINIAOD'], 'data','DoubleMu','2016', 'F','1','1','1']
data2016_samples['2016_G_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016G-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016G-17Jul2018-v1/MINIAOD'], 'data','DoubleMu','2016', 'G','1','1','1']
data2016_samples['2016_H_DoubleMu'] = [['/DoubleMuon/schoef-TopNanoAODv6-1-2-4_DoubleMuon_Run2016H-ba7e3129b1ff910ad1abce6981b33804/USER','/DoubleMuon/Run2016H-17Jul2018-v1/MINIAOD '], 'data','DoubleMu','2016', 'H','1','1','1']
