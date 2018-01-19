import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from xsec import getXsec

import random
import array

class TTbar_SemiLep(Module):
    def __init__(self ):
        self.writeHistFile = True
        self.verbose = False
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)

        self.isttbar = False
        if 'TTJets_' in histFile :
           self.isttbar = True 



        ### Set bins for Pt dependent scale factor calculation    

        self.TopcandPtBins = [[200,300], [300,400], [400,500],[500, -1]]
        # e.g. h_wpt_Tptbin0 is a 1D histogram for W candidate subjets (most massive SD subjet) within Top candidates of pt 200-300 GeV  

        self.WcandPtBins = [[200,300], [300-500], [500, -1]]
        # e.g. h_wpt_ptbin0 1D histogram is for W candidate subjets (most massive SD subjet) with pt 200-300 GeV   

        self.minMupt = 53.
        self.maxMuEta = 2.1
        self.maxRelIso = 0.1
        self.minMuMETPt = 40.

        ### Figure our tree branch for HighPtMuon ???
        #is High Pt


        #remove jet within 0.3
        self.mindRLepJet = 0.3
        #veto:
        # High pT muon ID
        #pT > 20 GeV, eta < 2.4??
        #relIso < 0.1


        self.minElpt = 120.
        self.minElMETPt = 80.
        #self.goodElEta = if eta < 1.44, 1.56 < eta < 2.5
        # HEEP v7 + iso
        #veto
        # HEEP + iso pt > 35 remove ecal crack region eta < 1.44, 1.56 < eta < 2.5
        #

        self.minLepWPt = 200.

        self.minJetPt = 200.
        self.maxJetEta = 2.5
        self.minTopmass = 140.
        self.maxTopmass = 200.

        #>= 1 CSVmedium akt4 jet
        self.minAK4Pt = 30.

        #Angular selection (not used by Thea now):

        #dR( lepton, leading AK8 jet) > pi/2
        #dPhi(leading AK8 jet, MET) > 2
        
        #dPhi (leading AK8 jet, leptonic W) >2
        #self.minDPhiWJet = 2.  

        self.addObject( ROOT.TH1D('h_lep0pt',          'h_lep0pt',        40, 0, 200 ) )
        self.addObject( ROOT.TH1D('h_lep0eta',         'h_lep0eta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_lep0phi',         'h_lep0phi',      100, -5, 5 ) )

        self.addObject( ROOT.TH1D('h_toppt',          'h_toppt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_topeta',         'h_topeta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_topphi',         'h_topphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_topmass',        'h_topmass',      60, 140, 200 ) )

        self.addObject( ROOT.TH1D('h_wpt',          'h_wpt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta',         'h_weta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi',         'h_wphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass',        'h_wmass',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin0',          'h_wpt_ptbin0',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin0',         'h_weta_ptbin0',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin0',         'h_wphi_ptbin0',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin0',        'h_wmass_ptbin0',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin1',          'h_wpt_ptbin1',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin1',         'h_weta_ptbin1',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin1',         'h_wphi_ptbin1',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin1',        'h_wmass_ptbin1',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin2',          'h_wpt_ptbin2',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin2',         'h_weta_ptbin2',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin2',         'h_wphi_ptbin2',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin2',        'h_wmass_ptbin2',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_Tptbin0',          'h_wpt_Tptbin0',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_Tptbin0',         'h_weta_Tptbin0',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_Tptbin0',         'h_wphi_Tptbin0',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_Tptbin0',        'h_wmass_Tptbin0',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_Tptbin1',          'h_wpt_Tptbin1',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_Tptbin1',         'h_weta_Tptbin1',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_Tptbin1',         'h_wphi_Tptbin1',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_Tptbin1',        'h_wmass_Tptbin1',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_Tptbin2',          'h_wpt_Tptbin2',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_Tptbin2',         'h_weta_Tptbin2',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_Tptbin2',         'h_wphi_Tptbin2',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_Tptbin2',        'h_wmass_Tptbin2',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wleppt',          'h_wleppt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_wlepeta',         'h_wlepeta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wlepphi',         'h_wlepphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wlepmass',        'h_wlepmass',      100, 50, 150 ) )


        self.addObject( ROOT.TH1D('h_genjetpt',          'h_genjetpt',   100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_genjeteta',         'h_genjeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_genjetphi',         'h_genjetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_genjetmass',        'h_genjetmass',      300, 0, 300 ) )

        self.addObject( ROOT.TH1D('h_recoAK8jetpt',          'h_recoAK8jetpt',  100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jeteta',         'h_recoAK8jeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jetphi',         'h_recoAK8jetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jetmass',        'h_recoAK8jetmass',      300, 0, 300 ) )

        if self.isttbar :
            self.addObject( ROOT.TH1D('h_matchedAK8jetpt',          'h_matchedAK8jetpt',      100, 0, 500 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jeteta',         'h_matchedAK8jeteta',      48, -3, 3 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jetphi',         'h_matchedAK8jetphi',      100, -5, 5 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jetmass',        'h_matchedAK8jetmass',      300, 0, 300 ) )

            self.addObject( ROOT.TH1D('h_unmatchedAK8jetpt',          'h_unmatchedAK8jetpt',      100, 0, 500 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jeteta',         'h_unmatchedAK8jeteta',      48, -3, 3 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jetphi',         'h_unmatchedAK8jetphi',      100, -5, 5 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jetmass',        'h_unmatchedAK8jetmass',      300, 0, 300 ) )



        self.addObject( ROOT.TH1D('h_drGenReco',    'h_drGenReco',   40, 0, 0.8) )
        self.addObject( ROOT.TH1D('h_drGenGroomed', 'h_drGenGroomed',40, 0, 0.8) )
                            
    def endJob(self):
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # This is a loose selection to select events for T Tbar semileptonic events where 
        # Type 1 and Type 2 events are included in the selection:

        # In SF code the final cuts need to be made to choose either type 1 or type 2 selection:
        # e.g. for type 1 the W leptonic Pt cut should be tightened to 200 GeV and dPhi cuts applied
        # e.g. for type 2 the AK8 Pt cut should be tightened to 400 GeV and dPhi cuts applied

        # Type 1 - martially merged Hadronic Top Quark (W is AK8, b is AK4) 
        #(AK8 Pt > 200 GeV)

        # Type 2 - fully merged Top (Top is AK8, W is most massive SD subjet, b is less massive subjet, require 1 subjet b-tag) 
        #(AK8 Pt > 400 GeV): 




        # selection aligned with previous SF measurement standard selection
        # https://www.evernote.com/shard/s282/sh/7e5d6baa-d100-4025-8bf8-a61bf1adfbc1/f7e86fde2c2a165e
        

        # 1 AK8 Pt > 200 GeV, |eta| < 2.5
        # 1 AK4 Pt > 30 GeV, |eta| < 2.5
        # 1 lepton , mu pt > 53 GeV or el pt > 120 GeV
        # MET Pt > 40(mu) or 80(el) GeV
        #Leptonic W - lepton + MET has Pt > 150 GeV 


        self.out.branch("LeptonIsMu",  "F")
        self.out.branch("Lepton_pt",  "F")
        self.out.branch("Lepton_eta",  "F")
        self.out.branch("Lepton_phi",  "F")               
        self.out.branch("Lepton_mass",  "F")

        '''
        self.out.branch("genLeptonIsMu",  "F")
        self.out.branch("genLepton_pt",  "F")
        self.out.branch("genLepton_eta",  "F")
        self.out.branch("genLepton_phi",  "F")               
        self.out.branch("genLepton_mass",  "F")
        '''
        self.out.branch("PuppiMET",  "F")

        self.out.branch("genMET",  "F")

        self.out.branch("AK4nearLep_pt",  "F")
        self.out.branch("AK4nearLep_eta",  "F")
        self.out.branch("AK4nearLep_phi",  "F")               
        self.out.branch("AK4nearLep_mass",  "F")


        self.out.branch("dr_LepJet",  "F")
        self.out.branch("dphi_LepJet",  "F")
        self.out.branch("dphi_MetJet",  "F")
        self.out.branch("dphi_WJet"  ,  "F")
        self.out.branch("FatJet_isW",  "F")
        self.out.branch("FatJet_softDrop_mass",  "F")
        self.out.branch("FatJet_tau21",  "F")
        self.out.branch("FatJet_tau21_ddt",  "F")
        self.out.branch("FatJet_tau21_ddt_retune",  "F")
        self.out.branch("FatJet_tau32",  "F")
        self.out.branch("FatJet_tau32_ddt",  "F")
        self.out.branch("FatJet_tau32_ddt_retune",  "F")

        self.out.branch("W_type",  "F")
        self.out.branch("W_pt",  "F")
        self.out.branch("MET",  "F")
        self.out.branch("xsec",  "F")
        xsec = getXsec(inputFile.GetName())
        print inputFile.GetName()
        print xsec
        self.out.fillBranch("xsec",xsec)

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def getSubjets(self, p4, subjets, dRmax=0.8):
        ret = []
        for subjet in subjets :
            if p4.DeltaR(subjet.p4()) < dRmax and len(ret) < 2 :
                ret.append(subjet.p4())
        return ret

    def printP4( self, c ):
        if hasattr( c, "p4"):
            s = ' %6.2f %5.2f %5.2f %6.2f ' % ( c.p4().Perp(), c.p4().Eta(), c.p4().Phi(), c.p4().M() )
        else :
            s = ' %6.2f %5.2f %5.2f %6.2f ' % ( c.Perp(), c.Eta(), c.Phi(), c.M() )
        return s
    def printCollection(self,coll):
        for ic,c in enumerate(coll):
            s = self.printP4( c )
            print ' %3d : %s' % ( ic, s )
            
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        weight = 1.0

        isMC = event.run == 1
        if self.verbose:
            print '------------------------ ', event.event

        if isMC:

            ### Look at generator level particles
            ### find events where :
            ### a W decays to quarks (Type 1 - partially merged)
            ###    OR
            ### a Top decays to W + b (Type 2 - fully merged top quark)
            gens = Collection(event, "GenPart")
            Wdaus =  [x for x in gens if x.pt>1 and 0<abs(x.pdgId)<9]
            Wmoms =  [x for x in gens if x.pt>10 and abs(x.pdgId)==24]

            Tdaus =  [x for x in gens if x.pt>1 and (abs(x.pdgId)==5  or  abs(x.pdgId)==24 )]
            Tmoms =  [x for x in gens if x.pt>10 and abs(x.pdgId)==6]
                    
            realVs = []
            realTs = []
            if len(Wmoms)>0 and len(Wdaus)>0:
                for dau in Wdaus:
                    for mom in Wmoms:
                        try:
                            if mom == Wmoms[dau.genPartIdxMother]: realVs.append(mom)    
                        except:
                            continue    

            if len(Tmoms)>0 and len(Tdaus)>0:
                for dau in Tdaus:
                    for mom in Tmoms:
                        try:
                            if mom == Tmoms[dau.genPartIdxMother]: realTs.append(mom)    
                        except:
                            continue  


            ###### Get gen Top candidate #######
            genleptons = Collection(event, "GenDressedLepton")

            if len(genleptons) < 1 :
                return False
            if abs(genleptons[0].pdgId) != 13 and abs(genleptons[0].pdgId)!= 12 :
                return False
            ########################

            ### Gen Selection
            ########################

            ### We want the AK4 nearest the lepton
            ### This is the b candidate
            ### check b disc in tagging script


            genAK4s = Collection(event, "GenJet")    
            genAK4jets = [ x for x in genAK4s if x.p4().Perp() > self.minAK4Pt * 0.8 and abs(x.p4().Eta()) < self.maxJetEta ]
            

            METgen_pt = event.GenMET_pt

           
            ### Gen Electron
            ### Pick the high Pt (self.minElpt * 0.8), low eta, HEEPv7 Electrons    
            if abs(genleptons[0].pdgId) == 12 :
                if genleptons[0].p4().Perp() < self.minElpt * 0.8 :
                    return False
                if abs(genleptons[0].p4().Eta()) < 1.44 or (abs(genleptons[0].p4().Eta()) > 1.56 and  abs(genleptons[0].p4().Eta()) < 2.5  ) :
                    return False 
                if METgen_pt < self.minElMETPt :
                    return False
            ### Gen Muons  
            ### Pick high pt, low eta muons       
            if abs(genleptons[0].pdgId) == 13 :
                if genleptons[0].p4().Perp() < self.minMupt * 0.8 :
                    return False
                if abs(genleptons[0].p4().Eta())  > self.maxMuEta :
                    return False 
                if METgen_pt < self.minMuMETPt :
                    return False
            if self.verbose :
                print '----'
                print 'Gen leptons:'
                self.printCollection( genleptons )


            # self.mindRLepJet is minimum seperation btw lep and ak4
            # we want the ak4 with dR > self.mindRLepJet and dR < mindRObs
            mindRObs = 5.0
            genbHad = ROOT.TLorentzVector()
            for ibcand, bcand in enumerate(genAK4jets) :
                tempdR = bcand.p4().DeltaR(genleptons[0].p4())
                if tempdR > self.mindRLepJet and tempdR < mindRObs :
                    mindRObs = tempdR
                    genbHad.SetPtEtaPhiM( bcand.p4().Perp(), bcand.p4().Eta() , bcand.p4().Phi() , bcand.p4().M()  )

            ''' If METgen_eta info is missing we cannot use gen MET for leptonic W selection
            
            METgen_phi = event.GenMET_phi
            METgen_eta = event.GenMET_eta 
            METgen = ROOT.TLorentzVector()

            METgen.SetPtEtaPhiM(METgen_pt[0],METgen_eta[0],METgen_phi[0], 0.0  )
            WLep = genleptons[0].p4() + METgen
            if WLep.Perp() < self.minLepWPt * 0.9 :
                return False

            if self.verbose:
                print '-----'
                print 'Gen W Leptonic:'
                print self.printP4( WLep )

            ''' 

            ###### Get list of gen jets #######
            # List of gen jets:
            allgenjets = list(Collection(event, "GenJetAK8"))
            if self.verbose:
                print '-----'
                print 'all genjets:'
                self.printCollection( allgenjets )
            genjets = [ x for x in allgenjets if x.p4().Perp() > self.minJetPt * 0.8 and abs( x.p4().Eta()) < self.maxJetEta and genleptons[0].p4().DeltaR(x.p4()) > self.mindRLepJet ] #and x.p4().DeltaPhi( WbosonLep ) > self.minDPhiWJet     ]
            # List of gen subjets (no direct link from Genjet):
            gensubjets = list(Collection(event, "SubGenJetAK8"))
            # Dictionary to hold ungroomed-->groomed for gen
            genjetsGroomed = {}
            # Get the groomed gen jets
            maxSubjetMass = 1.

            WHad = ROOT.TLorentzVector()
            for igen,gen in enumerate(genjets):
                gensubjetsMatched = self.getSubjets( p4=gen.p4(),subjets=gensubjets, dRmax=0.8)
                for isub,sub in enumerate(gensubjetsMatched) : 
                    if sub.M() > maxSubjetMass : 
                        maxSubjetMass = sub.M() 
                        WHad.SetPtEtaPhiM(sub.Perp(),sub.Eta(),sub.Phi(),sub.M())
                        

                    self.h_drGenGroomed.Fill( gen.p4().DeltaR( sub ) )
                genjetsGroomed[gen] = sum( gensubjetsMatched, ROOT.TLorentzVector() ) if (len(gensubjetsMatched) > 0 and sum( gensubjetsMatched, ROOT.TLorentzVector() ).Perp() > self.minJetPt *0.8 and sum( gensubjetsMatched, ROOT.TLorentzVector() ).M() > self.minTopmass  *0.8 ) else None
                
            if self.verbose:
                print '----'
                print 'opposite-LepW genjets:'
                for genjet in genjets:
                    sdmassgen = genjetsGroomed[genjet].M() if genjet in genjetsGroomed else -1.0
                    print '         : %s %6.2f' % ( self.printP4(genjet), sdmassgen )            
            

            
        ###### Get reco Top candidate #######
        # List of reco muons
        allmuons = Collection(event, "Muon")
        allelectrons = Collection(event, "Electron")
        # Select reco muons:
        muons = [ x for x in allmuons if x.tightId and x.pfRelIso03_all and x.p4().Perp() > self.minMupt and abs(x.p4().Eta())  < self.maxMuEta ]
        # Select reco muons:
        electrons = [ x for x in allelectrons if  x.cutBased_HEEP and x.p4().Perp() > self.minElpt  and (abs(x.p4().Eta()) < 1.44 or (abs(x.p4().Eta()) > 1.56 and  abs(x.p4().Eta()) < 2.5  ))]

        if ( len(muons) + len(electrons) ) < 1 :
            return False

        ### Choose the leading lepton in the event
        lepton = ROOT.TLorentzVector()
        isMu = None #False

        if  ( len(muons) ) > 0 and  ( len(electrons) ) < 1  :
            lepton = muons[0].p4()
            isMu = True

        if  ( len(muons) ) < 1 and  ( len(electrons) ) > 0  :
            lepton = electrons[0].p4()
            isMu = False
      
        if  ( len(muons) ) > 0 and  ( len(electrons) ) > 0  :
            return False

        triggerMu = Object(event, "HLT_Mu50")
        triggerEl = Object(event, "HLT_Ele115_CaloIdVT_GsfTrkIdT")

   




        



        MET_pt = event.PuppiMET_pt     
        
        if isMu and MET_pt < self.minMuMETPt :
            return False
        if not isMu and MET_pt < self.minElMETPt :
            return False

        MET = ROOT.TLorentzVector()
        MET.SetPtEtaPhiM(MET_pt, 0.0, event.PuppiMET_phi , event.PuppiMET_sumEt)


        WcandLep = lepton + MET
        if WcandLep.Perp() < self.minLepWPt :
            return False

        allrecoAK4jets = list(Collection(event, "Jet")) # are these AK4s ? 
        recojetsAK4 = [ x for x in allrecoAK4jets if x.p4().Perp() > self.minAK4Pt and abs(x.p4().Eta()) < self.maxJetEta]

        mindRObs = 5.0
        bHadreco = ROOT.TLorentzVector()
        for ibcand, bcand in enumerate(recojetsAK4 ) :
            tempdR = bcand.p4().DeltaR(genleptons[0].p4())
            if tempdR > self.mindRLepJet and tempdR < mindRObs :
                mindRObs = tempdR
                bHadreco.SetPtEtaPhiM( bcand.p4().Perp(), bcand.p4().Eta() , bcand.p4().Phi() , bcand.p4().M()  )



        Topcandreco =  WcandLep +  bHadreco
        self.h_toppt.Fill( Topcandreco.Perp() )
        self.h_topmass.Fill( Topcandreco.M() )
        if self.verbose:
            print '-----'
            print ' reco Top Leptonic:', self.printP4( Topcandreco)
        
        ###### Get list of reco jets #######
        # List of reco jets:
        allrecojets = list(Collection(event, "FatJet"))
        if self.verbose:
            print '----'
            print 'all recojets:'
            self.printCollection( allrecojets )
        recojets = [ x for x in allrecojets if x.p4().Perp() > self.minJetPt and  abs(x.p4().Eta()) < self.maxJetEta ] #and x.p4().DeltaPhi( minDPhiWJet ) > self.minDPhiWJet ]
        if len(recojets) < 1 : return False
        recojets.sort(key=lambda x:x.pt,reverse=True)

        if isMC == False:
            genjets = [None] * len(recojets)
        # List of reco subjets:
        recosubjets = list(Collection(event,"SubJet"))
        # Dictionary to hold reco--> gen matching
        recoToGen = matchObjectCollection( recojets, genjets, dRmax=0.05 )
        # Dictionary to hold ungroomed-->groomed for reco
        recojetsGroomed = {}        
        # Get the groomed reco jets
        maxrecoSJmass = 1.
        WHadreco = ROOT.TLorentzVector()
        for ireco,reco in enumerate(recojets):
            if reco.subJetIdx1 >= 0 and reco.subJetIdx2 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4() + recosubjets[reco.subJetIdx2].p4()
                if recosubjets[reco.subJetIdx1].p4().M() > maxrecoSJmass and recosubjets[reco.subJetIdx1].p4().M() >  recosubjets[reco.subJetIdx2].p4().M() :
                    maxrecoSJmass = recosubjets[reco.subJetIdx1].p4().M() 
                    WHadreco = recosubjets[reco.subJetIdx1].p4()
                if recosubjets[reco.subJetIdx2].p4().M() > maxrecoSJmass and recosubjets[reco.subJetIdx1].p4().M() < recosubjets[reco.subJetIdx2].p4().M() :
                    maxrecoSJmass = recosubjets[reco.subJetIdx1].p4().M() 
                    WHadreco = recosubjets[reco.subJetIdx2].p4()
            elif reco.subJetIdx1 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4()
                maxrecoSJmass = recosubjets[reco.subJetIdx1].p4().M() 
                WHadreco = recosubjets[reco.subJetIdx1].p4()     

            else :
                recojetsGroomed[reco] = None
                WHadreco = None

        if self.verbose:
            print '----'
            print 'opposite-Z recojets:'
            for recojet in recojets:
                sdmassreco = recojetsGroomed[recojet].M() if recojet in recojetsGroomed and recojetsGroomed[recojet] != None else -1.0
                print '         : %s %6.2f' % ( self.printP4( recojet),  sdmassreco )            

                
        # Loop over the reco,gen pairs.
        # Check if there are reco and gen SD jets

        for reco,gen in recoToGen.iteritems():
            recoSD = recojetsGroomed[reco]
            if reco == None :
                continue
            #if recoSD != None :
            #    # Fill the groomed det if available

            # Now check ungroomed gen
            genSDVal = None
            if gen != None:
                if self.isttbar :
                    self.h_matchedAK8jetpt.Fill(recoSD.Perp())
                    self.h_matchedAK8jeteta.Fill(recoSD.Eta())
                    self.h_matchedAK8jetphi.Fill(recoSD.Phi())
                    self.h_matchedAK8jetmass.Fill(recoSD.M())
                    
                self.h_drGenReco.Fill( reco.p4().DeltaR(gen.p4()) )

                genSD = genjetsGroomed[gen]
                if recoSD != None and genSD != None:
                    genSDVal = genSD.M()
                                        
                    if self.verbose : 
                        print ' reco: %s %8.4f, gen : %s %8.4f ' % (
                            self.printP4(reco), recoSD.M(), 
                            self.printP4(gen), genSD.M()
                            )

            elif  self.isttbar :
                # Here we have a groomed det, but no groomed gen
                if genSDVal == None and recoSD != None :
                    self.h_unmatchedAK8jetpt.Fill(recoSD.Perp())
                    self.h_unmatchedAK8jeteta.Fill(recoSD.Eta())
                    self.h_unmatchedAK8jetphi.Fill(recoSD.Phi())
                    self.h_unmatchedAK8jetmass.Fill(recoSD.M())


        #self.out.fillBranch("dr_LepJet"  ,dR_jetlep)
        '''
        self.out.fillBranch("dphi_LepJet",jet_4v.DeltaPhi(vLepton_4vec))
        self.out.fillBranch("dphi_MetJet",jet_4v.DeltaPhi(met_4v))
        self.out.fillBranch("dphi_WJet"  ,jet_4v.DeltaPhi(V))
        self.out.fillBranch("W_type",Vtype)
        self.out.fillBranch("W_pt", V.Perp()+met.sumEt )
        self.out.fillBranch("MET", met.sumEt )
        self.out.fillBranch("FatJet_isW", isW)
        self.out.fillBranch("FatJet_softDrop_mass",  wFatJets[0].msoftdrop)
        self.out.fillBranch("FatJet_tau21", wFatJets[0].tau2/wFatJets[0].tau1)
        self.out.fillBranch("FatJet_tau21_ddt", wFatJets[0].tau2/wFatJets[0].tau1+0.063*ROOT.TMath.Log(wFatJets[0].msoftdrop**2/wFatJets[0].pt))
        self.out.fillBranch("FatJet_tau21_ddt_retune", wFatJets[0].tau2/wFatJets[0].tau1+0.082*ROOT.TMath.Log(wFatJets[0].msoftdrop**2/wFatJets[0].pt))
        

        self.out.fillBranch("FatJet_tau32", wFatJets[0].tau3/wFatJets[0].tau2)
        self.out.fillBranch("FatJet_tau32_ddt", wFatJets[0].tau3/wFatJets[0].tau2+0.063*ROOT.TMath.Log(wFatJets[0].msoftdrop**2/wFatJets[0].pt))
        self.out.fillBranch("FatJet_tau32_ddt_retune", wFatJets[0].tau3/wFatJets[0].tau2+0.082*ROOT.TMath.Log(wFatJets[0].msoftdrop**2/wFatJets[0].pt))
        '''

        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbar_semilep = lambda : TTbar_SemiLep() 
