import sys
import ROOT as r

if len(sys.argv)>1: mode = int(sys.argv[1])
else : mode = 0

infile = r.TFile.Open('./results/tth_fit.root')

var=''
if mode==0: var='alpha'
if mode==1: var='beta'
if mode==2: var='beta_modif'
if mode==3: var='sigFrac'
if var=='' :
  print "mode="+str(mode)+" not supported -> check !!"
  quit()

####### get histos
h_alpha_exp        = infile.Get(var+'_exp_STAT'   )
h_alpha_stat       = infile.Get(var+'_val_STAT'   )
h_alpha_staterr    = infile.Get('alpha_err_STAT'  ) # only stored for alpha
h_alpha_SCALEup    = infile.Get(var+'_val_SCALEup')
h_alpha_SCALEdo    = infile.Get(var+'_val_SCALEdo')
h_alpha_SHAPECR    = infile.Get(var+'_val_SHAPECR')
h_alpha_FITSR0     = infile.Get(var+'_val_FITSR0')
h_alpha_FITSR1up   = infile.Get(var+'_val_FITSR1up')
h_alpha_FITSR1do   = infile.Get(var+'_val_FITSR1do')
h_alpha_FITSR2up   = infile.Get(var+'_val_FITSR2up')
h_alpha_FITSR2do   = infile.Get(var+'_val_FITSR2do')
h_alpha_FITSR3up   = infile.Get(var+'_val_FITSR3up')
h_alpha_FITSR3do   = infile.Get(var+'_val_FITSR3do')
h_alpha_FITSR4up   = infile.Get(var+'_val_FITSR4up')
h_alpha_FITSR4do   = infile.Get(var+'_val_FITSR4do')
h_alpha_FITSR5up   = infile.Get(var+'_val_FITSR5up')
h_alpha_FITSR5do   = infile.Get(var+'_val_FITSR5do')
h_alpha_FITSR6up   = infile.Get(var+'_val_FITSR6up')
h_alpha_FITSR6do   = infile.Get(var+'_val_FITSR6do')
h_alpha_SHIFT2SRup = infile.Get(var+'_val_SHIFT2SRup')
h_alpha_SHIFT2SRdo = infile.Get(var+'_val_SHIFT2SRdo')
h_alpha_SHIFT1SRup = infile.Get(var+'_val_SHIFT1SRup')
h_alpha_SHIFT1SRdo = infile.Get(var+'_val_SHIFT1SRdo')

####### compute numbers
exp              = h_alpha_exp.GetMean()
alpha            = h_alpha_stat.GetMean()
alpha_stat       = h_alpha_staterr.GetMean()
alpha_scaleup    = h_alpha_SCALEup.GetMean()
alpha_scaledo    = h_alpha_SCALEdo.GetMean()
alpha_shapecr    = h_alpha_SHAPECR.GetMean()
alpha_fitsr0     = h_alpha_FITSR0.GetMean()
alpha_fitsr1up   = h_alpha_FITSR1up.GetMean()
alpha_fitsr1do   = h_alpha_FITSR1do.GetMean()
alpha_fitsr2up   = h_alpha_FITSR2up.GetMean()
alpha_fitsr2do   = h_alpha_FITSR2do.GetMean()
alpha_fitsr3up   = h_alpha_FITSR3up.GetMean()
alpha_fitsr3do   = h_alpha_FITSR3do.GetMean()
alpha_fitsr4up   = h_alpha_FITSR4up.GetMean()
alpha_fitsr4do   = h_alpha_FITSR4do.GetMean()
alpha_fitsr5up   = h_alpha_FITSR5up.GetMean()
alpha_fitsr5do   = h_alpha_FITSR5do.GetMean()
alpha_fitsr6up   = h_alpha_FITSR6up.GetMean()
alpha_fitsr6do   = h_alpha_FITSR6do.GetMean()
alpha_shift2srup = h_alpha_SHIFT2SRup.GetMean()
alpha_shift2srdo = h_alpha_SHIFT2SRdo.GetMean()
alpha_shift1srup = h_alpha_SHIFT1SRup.GetMean()
alpha_shift1srdo = h_alpha_SHIFT1SRdo.GetMean()
# fix
if var!='alpha': alpha_stat = h_alpha_staterr.GetRMS()
#
err_stat       = 100.*alpha_stat/alpha
err_scaleup    = 100.*(alpha_scaleup-alpha)/alpha
err_scaledo    = 100.*(alpha_scaledo-alpha)/alpha
err_shapecr    = 100.*(alpha_shapecr-alpha)/alpha
err_fitsr0     = 100.*(alpha_fitsr0-alpha)/alpha
err_fitsr1up   = 100.*(alpha_fitsr1up-alpha)/alpha
err_fitsr1do   = 100.*(alpha_fitsr1do-alpha)/alpha
err_fitsr2up   = 100.*(alpha_fitsr2up-alpha)/alpha
err_fitsr2do   = 100.*(alpha_fitsr2do-alpha)/alpha
err_fitsr3up   = 100.*(alpha_fitsr3up-alpha)/alpha
err_fitsr3do   = 100.*(alpha_fitsr3do-alpha)/alpha
err_fitsr4up   = 100.*(alpha_fitsr4up-alpha)/alpha
err_fitsr4do   = 100.*(alpha_fitsr4do-alpha)/alpha
err_fitsr5up   = 100.*(alpha_fitsr5up-alpha)/alpha
err_fitsr5do   = 100.*(alpha_fitsr5do-alpha)/alpha
err_fitsr6up   = 100.*(alpha_fitsr6up-alpha)/alpha
err_fitsr6do   = 100.*(alpha_fitsr6do-alpha)/alpha
err_shift2srup = 100.*(alpha_shift2srup-alpha)/alpha
err_shift2srdo = 100.*(alpha_shift2srdo-alpha)/alpha
err_shift1srup = 100.*(alpha_shift1srup-alpha)/alpha
err_shift1srdo = 100.*(alpha_shift1srdo-alpha)/alpha

####### print them
my_round=2
print var+" =",round(alpha,my_round),"(expect from yields=",round(exp,2),")"
print "STAT err =",round(err_stat,my_round),"%"
print "BKG SCALE (10%) err = ",round(err_scaleup,my_round),",",round(err_scaledo,my_round),"%"
print "BKG SHAPE (from CR) err = ",round(err_shapecr,my_round),"%"
print "BKG SHAPE (from SR FIT 0% line + norm) err =",round(err_fitsr0,my_round),"%"
print "BKG SHAPE (from SR FIT 1% line + norm) err =",round(err_fitsr1up,my_round),",",round(err_fitsr1do,my_round),"%"
print "BKG SHAPE (from SR FIT 2% line + norm) err =",round(err_fitsr2up,my_round),",",round(err_fitsr2do,my_round),"%"
print "BKG SHAPE (from SR FIT 3% line + norm) err =",round(err_fitsr3up,my_round),",",round(err_fitsr3do,my_round),"%"
print "BKG SHAPE (from SR FIT 4% line + norm) err =",round(err_fitsr4up,my_round),",",round(err_fitsr4do,my_round),"%"
print "BKG SHAPE (from SR FIT 5% line + norm) err =",round(err_fitsr5up,my_round),",",round(err_fitsr5do,my_round),"%"
print "BKG SHAPE (from SR FIT 6% line + norm) err =",round(err_fitsr6up,my_round),",",round(err_fitsr6do,my_round),"%"
nbins=150.
bin_width=(300.-0.)/nbins
print "BKG SHIFT (from SR FIT,",round(2.*bin_width),"GeV) err =",round(err_shift2srup,my_round),",",round(err_shift2srdo,my_round),"%"
print "BKG SHIFT (from SR FIT,",round(1.*bin_width),"GeV) err =",round(err_shift1srup,my_round),",",round(err_shift1srdo,my_round),"%"

