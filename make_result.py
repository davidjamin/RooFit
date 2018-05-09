import ROOT as r
infile = r.TFile.Open('./results/tth_fit.root')

####### get histos
h_alpha_stat    = infile.Get('alpha_val_STAT'   )
h_alpha_staterr = infile.Get('alpha_err_STAT'   )
h_alpha_SCALEup = infile.Get('alpha_val_SCALEup')
h_alpha_SCALEdo = infile.Get('alpha_val_SCALEdo')
h_alpha_SHAPECR = infile.Get('alpha_val_SHAPECR')
h_alpha_FITCRup = infile.Get('alpha_val_FITCRup')
h_alpha_FITCRdo = infile.Get('alpha_val_FITCRdo')

####### compute numbers
alpha         = h_alpha_stat.GetMean()
alpha_stat    = h_alpha_staterr.GetMean()
alpha_scaleup = h_alpha_SCALEup.GetMean()
alpha_scaledo = h_alpha_SCALEdo.GetMean()
alpha_shapecr = h_alpha_SHAPECR.GetMean()
alpha_fitcrup = h_alpha_FITCRup.GetMean()
alpha_fitcrdo = h_alpha_FITCRdo.GetMean()
#
err_stat    = alpha_stat/alpha
err_scaleup = (alpha_scaleup-alpha)/alpha
err_scaledo = (alpha_scaledo-alpha)/alpha
err_shapecr = (alpha_shapecr-alpha)/alpha
err_fitcrup = (alpha_fitcrup-alpha)/alpha
err_fitcrdo = (alpha_fitcrdo-alpha)/alpha

####### print them
print "alpha = "+str(alpha)
print "STAT err = "+str(err_stat*100.)+"%"
print "BKG SCALE (10%) err = up:"+str(err_scaleup*100.)+" do:"+str(err_scaledo*100.)+" %"
print "BKG SHAPE from CR err = "+str(err_shapecr*100.)+"%"
print "BKG FIT err = up:"+str(err_fitcrup*100.)+" do:"+str(err_fitcrdo*100.)+" %"

