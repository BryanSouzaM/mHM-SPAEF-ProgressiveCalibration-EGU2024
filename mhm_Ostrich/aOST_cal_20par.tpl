 !global_parameters
                                     !PARAMETER           lower_bound           upper_bound                 value      FLAG  SCALING
 ! interception
 &interception1
                       canopyInterceptionFactor =     0,       0.400000000000,       1CIF,        1,       1
 /
  
 ! snow
 &snow1
                       snowTreshholdTemperature =     -2.000000000000,       9.000000000000,       2STT,        1,       1
                         degreeDayFactor_forest =      0.000000000000,       4.000000000000,       3DDF_F,        1,       1
                     degreeDayFactor_impervious =      0.000000000000,       1.000000000000,       4DDF_I,        1,       1
                       degreeDayFactor_pervious =      0.000000000000,       2.000000000000,       5DDF_P,        1,       1
                increaseDegreeDayFactorByPrecip =      0.000000000000,       0.900000000000,       6IDDFP,        1,       1
                      maxDegreeDayFactor_forest =      0.000000000000,       8.000000000000,       7MDDF_F,        1,       1
                  maxDegreeDayFactor_impervious =      0.000000000000,      12.000000000000,       8MDDF_I,        1,       1
                    maxDegreeDayFactor_pervious =      0.000000000000,      15.000000000000,       9MDDF_P,        1,       1
 /
  
 ! soilmoisture
 &soilmoisture1
                        orgMatterContent_forest =      0.000000000000,     750.000000000000,       1OMC_F,        1,       1
                    orgMatterContent_impervious =      0.000000000000,       4.500000000000,       2OMC_I,        1,       1
                      orgMatterContent_pervious =      0.000000000000,       4.000000000000,       3OMC_P,        1,       1
                         PTF_lower66_5_constant =      0.000000000000,       1.970600000000,       4PTF_L665_Cnst,        1,       1
                             PTF_lower66_5_clay =      0.000000000000,       0.112900000000,       5PTF_L665_CL,        1,       1
                               PTF_lower66_5_Db =     -0.372700000000,      0.187100000000,       6PTF_L665_Db,        1,       1
                        PTF_higher66_5_constant =      0.000000000000,       1.123200000000,       7PTF_H665_Cnst,        1,       1
                            PTF_higher66_5_clay =     -0.005500000000,       0.009900000000,       8PTF_H665_CL,        1,       1
                              PTF_higher66_5_Db =     -0.551300000000,      0.091300000000,       9PTF_H665_Db,        1,       1
                                PTF_Ks_constant =     -1.200000000000,      0.285000000000,       1PTF_Ks_Cst,        1,       1
                                    PTF_Ks_sand =      0.000000000000,       0.026000000000,       2PTF_Ks_S,        1,       1
                                    PTF_Ks_clay =      0.000000000000,       0.013000000000,       3PTF_Ks_Cl,        1,       1
                              PTF_Ks_curveSlope =      0.000000000000,     100.000000000000,       4PTF_Ks_CS,        1,       1
                 rootFractionCoefficient_forest =      0.000000000000,       0.999000000000,       5RFC_F,        1,       1
             rootFractionCoefficient_impervious =      0.000000000000,       0.950000000000,       6RFC_I,        1,       1
               rootFractionCoefficient_pervious =      0.000000000000,       0.090000000000,       7RFC_P,        1,       1
                        infiltrationShapeFactor =      0.000000000000,       4.000000000000,       8ISF,        1,       1
 /
  
 ! directSealedAreaRunoff
 &directRunoff1
                      imperviousStorageCapacity =      0.000000000000,      60.000000000000,      9ISC,        1,       1
 /
  
 ! potential evapotranspiration
 &PET1
                         minCorrectionFactorPET =      0.000000000000,       2.500000000000,       1MC_FP,        1,       1
                         maxCorrectionFactorPET =      0.000000000000,       0.500000000000,       2MC_FP,        1,       1
                              aspectTresholdPET =      0.000000000000,     200.000000000000,       3ATP,        1,       1
                          HargreavesSamaniCoeff =      0.000000000000,       0.003000000000,       4HSC,        1,       1
 /
  
 ! interflow
 &interflow1
                 interflowStorageCapacityFactor =     0.000000000000,     200.000000000000,     5ISCF,        1,       1
                       interflowRecession_slope =      0.000000000000,      10.000000000000,       6IR_S,        1,       1
                  fastInterflowRecession_forest =      0.000000000000,       3.000000000000,       7FIR_F,        1,       1
                      slowInterflowRecession_Ks =      0.000000000000,      30.000000000000,      8SIR_K,        1,       1
                          exponentSlowInterflow =      0.000000000000,       0.300000000000,       9ESI,        1,       1
 /
  
 ! percolation
 &percolation1
                            rechargeCoefficient =      0.000000000000,      50.000000000000,      1RC,        1,       1
                         rechargeFactor_karstic =     -5.000000000000,       5.000000000000,       2RF_K,        1,       1
                  gain_loss_GWreservoir_karstic =      0.000000000000,       5.000000000000,       3GL_GWR_K,        1,       1
 /
  
 ! routing
 &routing3
                                   slope_factor =      0.000000000000,      50.000000000000,      4SF,        1,       1
 /
  
 ! geology
 &geoparameter
                                  GeoParam(1,:) =      0.000000000000,   10000.000000000000,    5GP1,        1,       1
                                  GeoParam(2,:) =      0.000000000000,   10000.000000000000,    6GP2,        1,       1
                                  GeoParam(3,:) =      0.000000000000,   10000.000000000000,    7GP3,        1,       1
                                  GeoParam(4,:) =      0.000000000000,   10000.000000000000,    8GP4,        1,       1
                                  GeoParam(5,:) =      0.000000000000,   10000.000000000000,    9GP5,        1,       1
                                  GeoParam(6,:) =      0.000000000000,   10000.000000000000,    1GP6,        1,       1
                                  GeoParam(7,:) =      0.000000000000,   10000.000000000000,    2GP7,        1,       1
                                  GeoParam(8,:) =      0.000000000000,   10000.000000000000,    3GP8,        1,       1
                                  GeoParam(9,:) =      0.000000000000,   10000.000000000000,    4GP9,        1,       1
 /
  
 ! neutrons
 /
  
 !    
 /
  
