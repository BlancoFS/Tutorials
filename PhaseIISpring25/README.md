# Spring25 MC Phase II 
## DY and QCD Sample generation using Spring25 non-oficial conditions

The oficial samples (Spring24) correspond to `CMSSW_14_0_6`, which is too old for a proper MTD timing study due to the last updates on the geometry and, particularly, on the `ETLSample` class.

## Init

Rebase on Luca's configuration to run the muon reconstruction on top of Alpaka Pixel tracks and reduce timing for Particle Flow based isolation.

```
cmsrel CMSSW_15_1_0_pre5
cd CMSSW_15_1_0_pre5/src

git cms-rebase-topic Parsifal-2045:singleIterMuonsExt
git cms-addpkg HLTrigger/Configuration
git clone -b Run2024 https://github.com/wonpoint4/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3
git clone -b PhaseII_PFIsolation https://github.com/BlancoFS/MuonHLTTool.git

cp -r MuonHLTTool/CMSSW_Tools/* ./
scram b -j 15
```

## GEN-SIM step

One can modify some lines on the genFragment to supress the Z decay to electron and tau leptons and effectively get a ZMM sample ([link](https://github.com/cms-sw/cmssw/blob/master/Configuration/Generator/python/ZMM_14TeV_TuneCP5_cfi.py)).

To get DYTo2L or ZMM:

```
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/TSG-Phase2Spring24GS-00186 --retry 3 --create-dirs -o Configuration/GenProduction/python/TSG-Phase2Spring24GS-00186-fragment.py
scram b -j 1
```

To get QCD samples:

```
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/TSG-Phase2Spring24GS-00018 --retry 3 --create-dirs -o Configuration/GenProduction/python/TSG-Phase2Spring24GS-00018-fragment.py
```

Please modify the inital selection as desired. Now, get configuration for CMSSW:

```
cmsDriver.py Configuration/GenProduction/python/TSG-Phase2Spring24GS-00186-fragment.py --era Phase2C17I13M9 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot HLLHC14TeV --step GEN,SIM --geometry ExtendedRun4D110 --conditions auto:phase2_realistic_T33 --datatier GEN-SIM --eventcontent FEVTDEBUG --python_filename TSG-Phase2Spring25GS_cfg.py --fileout file:TSG-Phase2Spring25GS.root --number 100000 --number_out 100000 --no_exec --mc
```

## RAW-DIGI-MINIAOD

```
cmsDriver.py reco --python_filename TSG-Phase2Spring25RDM_cfg.py --eventcontent FEVTDEBUGHLT --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,SimGeneral/MixingModule/customiseStoredTPConfig.higherPtTP,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI-RAW --fileout file:TSG-Phase2Spring25DIGIRECOMiniAOD.root --conditions auto:phase2_realistic_T33 --customise_commands "process.FEVTDEBUGHLToutput.outputCommands.append('keep *_l1tSC8PFL1PuppiCorrectedEmulator_*_HLT')" --step DIGI:pdigi_valid,L1TrackTrigger,L1,DIGI2RAW --nThreads 8 --geometry ExtendedRun4D110 --nStreams 2 --filein file:TSG-Phase2Spring25GS.root --pileup AVE_200_BX_25ns --pileup_input das:/RelValMinBias_14TeV/CMSSW_14_1_0-141X_mcRun4_realistic_v1_STD_RegeneratedGS_2026D110_noPU-v1/GEN-SIM --era Phase2C17I13M9 --no_exec --mc -n -1
```

## Run ntuplizer configuration

Default ntuplizer without timing and particle flow sequences

```
cmsDriver.py Phase2 -s L1,L1TrackTrigger,L1P2GT,HLT:75e33 --processName=MYHLT --conditions auto:phase2_realistic_T33 --geometry ExtendedRun4D110 --era Phase2C17I13M9 --eventcontent FEVTDEBUGHLT --datatier GEN-SIM-DIGI-RAW-MINIAOD --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring,L1Trigger/Configuration/customisePhase2FEVTDEBUGHLT.customisePhase2FEVTDEBUGHLT,L1Trigger/Configuration/customisePhase2TTOn110.customisePhase2TTOn110 --filein file:TSG-Phase2Spring25DIGIRECOMiniAOD.root --fileout file:output_Phase2_HLT.root --python_filename hlt_muon_mc.py --inputCommands=keep *, drop l1tPFJets_*_*_*, drop l1tTrackerMuons_l1tTkMuonsGmt*_*_HLT, drop *_hlt*_*_HLT, drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT --mc --procModifiers alpaka,phase2CAExtension -n -1 --nThreads 1 --no_exec
```

## PF+MTD+Ntuplizer customizations

To be added to `hlt_muon_mc.py` on line 19:

```
# import of standard configurations                                                                                                                                                                                                                                             
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimPhase2L1GlobalTriggerEmulator_cff')
process.load('L1Trigger.Configuration.Phase2GTMenus.SeedDefinitions.step1_2024.l1tGTMenu_cff')
process.load('HLTrigger.Configuration.HLT_75e33_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
###                                                                                                                                                                                                                                                                             
process.load("TrackingTools.KalmanUpdators.Chi2MeasurementEstimator_cfi")
process.load('TrackingTools.TrackFitters.KFTrajectoryFitter_cfi')
process.load("TrackingTools.KalmanUpdators.KFUpdatorESProducer_cfi")
process.load('TrackingTools.GeomPropagators.SmartPropagatorAnyRK_cfi')
process.load('TrackingTools.TrackFitters.KFTrajectorySmoother_cfi')
process.load('RecoMTD.TrackExtender.PropagatorWithMaterialForMTD_cfi')
process.load('RecoMTD.TransientTrackingRecHit.MTDTransientTrackingRecHitBuilder_cfi')
#                                                                                                                                                                                                                                                                               
process.load('RecoLocalFastTime.FTLRecProducers.MTDTimeCalibESProducer_cfi')
process.load('RecoLocalFastTime.FTLClusterizer.MTDCPEESProducer_cfi')
#                                                                                                                                                                                                                                                                               
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('RecoMuon.TrackingTools.MuonTrackLoader_cff')
process.load('RecoMuon.TransientTrackingRecHit.MuonTransientTrackingRecHitBuilder_cfi')
#                                                                                                                                                                                                                                                                               
process.load("SimTracker.TrackAssociatorProducers.trackAssociatorByChi2_cfi")
process.load("SimTracker.TrackAssociatorProducers.trackAssociatorByPosition_cfi")
```

Now, just after Line 274 when it says `# End adding early deletion`, add:

```
process.source.inputCommands = cms.untracked.vstring(
    'keep *',
    'drop l1tPFJets_*_*_*',
    'drop l1tTrackerMuons_l1tTkMuonsGmt*_*_HLT',
    'drop *_hlt*_*_HLT',
    'drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT',
    'drop l1tPFCandidates_*_*_RECO'
)

# PF isolation                                                                                                                                                                                                                                                                  
from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTPFIsolation import *
customizeFuncForMuonPFIsolation(process, "MYHLT", False)

from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTNtupler import *
customizerFuncForMuonGeneralTrackerExtender(process, True, "MYHLT")

# -- Ntuple, DQMOutput, and EDMOutput -- #                                                                                                                                                                                                                                      
doNtuple = True
if doNtuple:
    process = customizerFuncForMuonHLTNtupler(process, "MYHLT", False)
    process.ntupler.offlineMuon                   = cms.untracked.InputTag("slimmedMuons")
    process.ntupler.TkMuonToken                   = cms.InputTag("l1tTkMuonsGmt")
    process.ntupler.doMVA                         = cms.bool(True)

    from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTSeedNtupler import *
    process = customizerFuncForMuonHLTSeedNtupler(process, "MYHLT", True)

    process.seedNtupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "", "MYHLT")
    process.TFileService.fileName = cms.string("step2.root")

doDQMOut = False
if doDQMOut:
    process.dqmOutput = cms.OutputModule("DQMRootOutputModule",
        dataset = cms.untracked.PSet(
            dataTier = cms.untracked.string('DQMIO'),
            filterName = cms.untracked.string('')
        ),
        fileName = cms.untracked.string("DQMIO.root"),
        outputCommands = process.DQMEventContent.outputCommands,
        splitLevel = cms.untracked.int32(0)
    )
    process.DQMOutput = cms.EndPath( process.dqmOutput )

doEDMOut = False
if doEDMOut:
    process.writeDataset = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('edmOutput.root'),
        outputCommands = cms.untracked.vstring(
            'drop *',
            'keep *_*_*_MYHLT'
        )
    )
    process.EDMOutput = cms.EndPath(process.writeDataset)
# -- #

process.schedule = cms.Schedule(
    process.L1simulation_step,
    process.L1TrackTrigger_step,
    process.Phase2L1GTProducer,
    process.Phase2L1GTAlgoBlockProducer,
    process.pTripleTkMuon_5_3_0_DoubleTkMuon_5_3_OS_MassTo9,
    process.pTripleTkMuon_5_3p5_2p5_OS_Mass5to17,
    process.pDoubleEGEle37_24,
    process.pDoubleIsoTkPho22_12,
    process.pDoublePuppiJet112_112,
    process.pDoublePuppiJet160_35_mass620,
    process.pDoublePuppiTau52_52,
    process.pDoubleTkEle25_12,
    process.pDoubleTkElePuppiHT_8_8_390,
    process.pDoubleTkMuPuppiHT_3_3_300,
    process.pDoubleTkMuPuppiJetPuppiMet_3_3_60_130,
    process.pDoubleTkMuon15_7,
    process.pDoubleTkMuonTkEle5_5_9,
    process.pDoubleTkMuon_4_4_OS_Dr1p2,
    process.pDoubleTkMuon_4p5_4p5_OS_Er2_Mass7to18,
    process.pDoubleTkMuon_OS_Er1p5_Dr1p4,
    process.pIsoTkEleEGEle22_12,
    process.pNNPuppiTauPuppiMet_55_190,
    process.pPuppiHT400,
    process.pPuppiHT450,
    process.pPuppiMET200,
    process.pPuppiMHT140,
    process.pPuppiTauTkIsoEle45_22,
    process.pPuppiTauTkMuon42_18,
    process.pQuadJet70_55_40_40,
    process.pSingleEGEle51,
    process.pSingleIsoTkEle28,
    process.pSingleIsoTkPho36,
    process.pSinglePuppiJet230,
    process.pSingleTkEle36,
    process.pSingleTkMuon22,
    process.pTkEleIsoPuppiHT_26_190,
    process.pTkElePuppiJet_28_40_MinDR,
    process.pTkEleTkMuon10_20,
    process.pTkMuPuppiJetPuppiMet_3_110_120,
    process.pTkMuTriPuppiJet_12_40_dRMax_DoubleJet_dEtaMax,
    process.pTkMuonDoubleTkEle6_17_17,
    process.pTkMuonPuppiHT6_320,
    process.pTkMuonTkEle7_23,
    process.pTkMuonTkIsoEle7_20,
    process.pTripleTkMuon5_3_3,
    process.HLT_Mu50_FromL1TkMuon,
    process.HLT_IsoMu24_FromL1TkMuon,
    process.HLT_Mu37_Mu27_FromL1TkMuon,
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,
    process.HLTriggerFinalPath,
    process.mypath,
    process.myendpath,
)
```



