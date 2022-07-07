##### Fragment to make decay tau leptons produced in the decay vertex (w > l vl)
##### 
##### If the gridpack is needed instead of LHE file, just remove the # in the begining of the first lines
#####


#import FWCore.ParameterSet.Config as cms                                                                                                                                                                                                     
#                                                                                                                                                                                                                                             
#externalLHEProducer = cms.EDProducer("ExternalLHEProducer",                                                                                                                                                                                  
#                                     args = cms.vstring('/afs/cern.ch/work/s/sblancof/private/POLARIZED_SAMPLES/HToW0W0To2l2v_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),                                                              
#                                     inputFile = cms.string('unweight_events.lhe'),                                                                                                                                                          
#                                     nEvents = cms.untracked.uint32(5000),                                                                                                                                                                   
#                                     numberOfParameters = cms.uint32(1),                                                                                                                                                                     
#                                     outputFile = cms.string('cmsgrid_final.lhe'),                                                                                                                                                           
#                                     scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')                                                                                                        
#)                                                                                                                                                                                                                                            

# Link to cards:                                                                                                                                                                                                                              
# https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DarkHiggs_WW2l2nu                                                                                                                   

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         ExternalDecays = cms.PSet(
                             Tauola = cms.untracked.PSet(
                                 TauolaPolar,
                                 TauolaDefaultInputCards
                             ),
                             parameterSets = cms.vstring('Tauola')
                         ),
                         UseExternalGenerators = cms.untracked.bool(True),

                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             pythia8PSweightsSettingsBlock,

                             processParameters = cms.vstring(
                                 'Main:timesAllowErrors    = 10000',
                                 'ParticleDecays:limitTau0 = on',
                                 'ParticleDecays:tauMax = 10'),

                             parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    'pythia8PSweightsSettings'
                                                     )
                        )
)

ProductionFilterSequence = cms.Sequence(generator)


# Link to generator fragment:                                                                                                                                                                                                                 
# https://raw.githubusercontent.com/cms-sw/genproductions/master/genfragments/ThirteenTeV/DarkHiggs/ZprimeToDmDmDarkhiggs_DarkhiggsToWW2l2nu_TuneCP5_13TeV_DM_LHE_pythia8_cff.py 
