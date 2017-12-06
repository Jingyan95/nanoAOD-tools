import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TTbarResAna(Module):
    def __init__(self):
        pass
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)
        self.addObject( ROOT.TH1F('h_vpt',   'h_vpt',   100, 0, 1000) )
        self.addObject( ROOT.TH1F('h_ak4pt', 'h_ak4pt', 100, 0, 1000) )
        self.addObject( ROOT.TH1F('h_ak4ht', 'h_ak4ht', 100, 0, 1000) )        
    def endJob(self):
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = list(Collection(event, "Jet"))
        fatjets = list(Collection(event, "FatJet"))
        met = Object(event, "MET")
      
        Vtype = -1

        wElectrons = [x for x in electrons if x.mvaSpring16GP_WP80 and x.pt > 25 ]      
        wMuons = [x for x in muons if x.pt > 25 and x.tightId >= 1 ]

        wMuons.sort(key=lambda x:x.pt,reverse=True)
        wElectrons.sort(key=lambda x:x.pt,reverse=True)

        vLeptons = [] # decay products of V
        if len(wElectrons) + len(wMuons) == 1:
            if len(wMuons) == 1:
                Vtype = 0
                vLeptons = [wMuons[0]]
            if len(wElectrons) == 1:
                Vtype=1
                vLeptons = [wElectrons[0]]

        ## add branches for some basic V kinematics
        V = ROOT.TLorentzVector()
        for vLepton in vLeptons:
            vLepton_4vec = ROOT.TLorentzVector()
            vLepton_4vec.SetPtEtaPhiM(vLepton.pt,vLepton.eta,vLepton.phi,vLepton.mass)
            V = V + vLepton_4vec
        self.h_vpt.Fill( V.Perp() )

        # Get the AK4 jets that pass the selection, and HT
        passedjets = [x for x in jets if x.jetId>0 and x.pt>20 and abs(x.eta)<2.5]
        ht = sum( [ j.pt for j in passedjets ] )
        self.h_ak4ht.Fill( ht )
        if len(passedjets) < 1 : return False
            
        for jet in passedjets:
            self.h_ak4pt.Fill( jet.pt )

        return True
                

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbarres = lambda : TTbarResAna() 
