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
h_alpha_FITCR1percentup = infile.Get('alpha_val_FITCR1percentup')
h_alpha_FITCR1percentdo = infile.Get('alpha_val_FITCR1percentdo')
h_alpha_SHIFT5SRup = infile.Get('alpha_val_SHIFT5SRup')
h_alpha_SHIFT5SRdo = infile.Get('alpha_val_SHIFT5SRdo')
h_alpha_SHIFT4SRup = infile.Get('alpha_val_SHIFT4SRup')
h_alpha_SHIFT4SRdo = infile.Get('alpha_val_SHIFT4SRdo')
h_alpha_SHIFT3SRup = infile.Get('alpha_val_SHIFT3SRup')
h_alpha_SHIFT3SRdo = infile.Get('alpha_val_SHIFT3SRdo')
h_alpha_SHIFT2SRup = infile.Get('alpha_val_SHIFT2SRup')
h_alpha_SHIFT2SRdo = infile.Get('alpha_val_SHIFT2SRdo')
h_alpha_SHIFT1SRup = infile.Get('alpha_val_SHIFT1SRup')
h_alpha_SHIFT1SRdo = infile.Get('alpha_val_SHIFT1SRdo')

####### compute numbers
alpha         = h_alpha_stat.GetMean()
alpha_stat    = h_alpha_staterr.GetMean()
alpha_scaleup = h_alpha_SCALEup.GetMean()
alpha_scaledo = h_alpha_SCALEdo.GetMean()
alpha_shapecr = h_alpha_SHAPECR.GetMean()
alpha_fitcrup = h_alpha_FITCRup.GetMean()
alpha_fitcrdo = h_alpha_FITCRdo.GetMean()
alpha_fitcr1percentup = h_alpha_FITCR1percentup.GetMean()
alpha_fitcr1percentdo = h_alpha_FITCR1percentdo.GetMean()
alpha_shift5srup = h_alpha_SHIFT5SRup.GetMean()
alpha_shift5srdo = h_alpha_SHIFT5SRdo.GetMean()
alpha_shift4srup = h_alpha_SHIFT4SRup.GetMean()
alpha_shift4srdo = h_alpha_SHIFT4SRdo.GetMean()
alpha_shift3srup = h_alpha_SHIFT3SRup.GetMean()
alpha_shift3srdo = h_alpha_SHIFT3SRdo.GetMean()
alpha_shift2srup = h_alpha_SHIFT2SRup.GetMean()
alpha_shift2srdo = h_alpha_SHIFT2SRdo.GetMean()
alpha_shift1srup = h_alpha_SHIFT1SRup.GetMean()
alpha_shift1srdo = h_alpha_SHIFT1SRdo.GetMean()
#
err_stat    = alpha_stat/alpha
err_scaleup = (alpha_scaleup-alpha)/alpha
err_scaledo = (alpha_scaledo-alpha)/alpha
err_shapecr = (alpha_shapecr-alpha)/alpha
err_fitcrup = (alpha_fitcrup-alpha)/alpha
err_fitcrdo = (alpha_fitcrdo-alpha)/alpha
err_fitcr1percentup = (alpha_fitcr1percentup-alpha)/alpha
err_fitcr1percentdo = (alpha_fitcr1percentdo-alpha)/alpha
err_shift5srup = (alpha_shift5srup-alpha)/alpha
err_shift5srdo = (alpha_shift5srdo-alpha)/alpha
err_shift4srup = (alpha_shift4srup-alpha)/alpha
err_shift4srdo = (alpha_shift4srdo-alpha)/alpha
err_shift3srup = (alpha_shift3srup-alpha)/alpha
err_shift3srdo = (alpha_shift3srdo-alpha)/alpha
err_shift2srup = (alpha_shift2srup-alpha)/alpha
err_shift2srdo = (alpha_shift2srdo-alpha)/alpha
err_shift1srup = (alpha_shift1srup-alpha)/alpha
err_shift1srdo = (alpha_shift1srdo-alpha)/alpha

####### print them
print "alpha = "+str(alpha)
print "STAT err = "+str(err_stat*100.)+"%"
print "BKG SCALE (10%) err = up:"+str(err_scaleup*100.)+" do:"+str(err_scaledo*100.)+" %"
print "BKG SHAPE (from CR) err = "+str(err_shapecr*100.)+"%"
print "BKG SHAPE (from CR FIT) err = up:"+str(err_fitcrup*100.)+" do:"+str(err_fitcrdo*100.)+" %"
print "BKG SHAPE (from CR FIT) err (1%) = up:"+str(err_fitcr1percentup*100.)+" do:"+str(err_fitcr1percentdo*100.)+" %"
nbins=150.
bin_width=(300.-0.)/nbins
print "BKG SHIFT (from SR FIT, "+str(5.*bin_width)+" GeV) err = up:"+str(err_shift5srup*100.)+" do:"+str(err_shift5srdo*100.)+" %"
print "BKG SHIFT (from SR FIT, "+str(4.*bin_width)+" GeV) err = up:"+str(err_shift4srup*100.)+" do:"+str(err_shift4srdo*100.)+" %"
print "BKG SHIFT (from SR FIT, "+str(3.*bin_width)+" GeV) err = up:"+str(err_shift3srup*100.)+" do:"+str(err_shift3srdo*100.)+" %"
print "BKG SHIFT (from SR FIT, "+str(2.*bin_width)+" GeV) err = up:"+str(err_shift2srup*100.)+" do:"+str(err_shift2srdo*100.)+" %"
print "BKG SHIFT (from SR FIT, "+str(1.*bin_width)+" GeV) err = up:"+str(err_shift1srup*100.)+" do:"+str(err_shift1srdo*100.)+" %"

