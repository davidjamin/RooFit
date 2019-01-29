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
h_alpha_FITSR5up   = infile.Get(var+'_val_FITSR0.5up')
h_alpha_FITSR5do   = infile.Get(var+'_val_FITSR0.5do')
h_alpha_FITSR10up  = infile.Get(var+'_val_FITSR1up')
h_alpha_FITSR10do  = infile.Get(var+'_val_FITSR1do')
h_alpha_FITSR15up  = infile.Get(var+'_val_FITSR1.5up')
h_alpha_FITSR15do  = infile.Get(var+'_val_FITSR1.5do')
h_alpha_FITSR20up  = infile.Get(var+'_val_FITSR2up')
h_alpha_FITSR20do  = infile.Get(var+'_val_FITSR2do')
h_alpha_FITSR25up  = infile.Get(var+'_val_FITSR2.5up')
h_alpha_FITSR25do  = infile.Get(var+'_val_FITSR2.5do')
h_alpha_FITSR30up  = infile.Get(var+'_val_FITSR3up')
h_alpha_FITSR30do  = infile.Get(var+'_val_FITSR3do')
#h_alpha_SHIFT5SRup = infile.Get(var+'_val_SHIFT5SRup')
#h_alpha_SHIFT5SRdo = infile.Get(var+'_val_SHIFT5SRdo')
#h_alpha_SHIFT4SRup = infile.Get(var+'_val_SHIFT4SRup')
#h_alpha_SHIFT4SRdo = infile.Get(var+'_val_SHIFT4SRdo')
#h_alpha_SHIFT3SRup = infile.Get(var+'_val_SHIFT3SRup')
#h_alpha_SHIFT3SRdo = infile.Get(var+'_val_SHIFT3SRdo')
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
alpha_fitsr5up   = h_alpha_FITSR5up.GetMean()
alpha_fitsr5do   = h_alpha_FITSR5do.GetMean()
alpha_fitsr10up  = h_alpha_FITSR10up.GetMean()
alpha_fitsr10do  = h_alpha_FITSR10do.GetMean()
alpha_fitsr15up  = h_alpha_FITSR15up.GetMean()
alpha_fitsr15do  = h_alpha_FITSR15do.GetMean()
alpha_fitsr20up  = h_alpha_FITSR20up.GetMean()
alpha_fitsr20do  = h_alpha_FITSR20do.GetMean()
alpha_fitsr25up  = h_alpha_FITSR25up.GetMean()
alpha_fitsr25do  = h_alpha_FITSR25do.GetMean()
alpha_fitsr30up  = h_alpha_FITSR30up.GetMean()
alpha_fitsr30do  = h_alpha_FITSR30do.GetMean()
#alpha_shift5srup = h_alpha_SHIFT5SRup.GetMean()
#alpha_shift5srdo = h_alpha_SHIFT5SRdo.GetMean()
#alpha_shift4srup = h_alpha_SHIFT4SRup.GetMean()
#alpha_shift4srdo = h_alpha_SHIFT4SRdo.GetMean()
#alpha_shift3srup = h_alpha_SHIFT3SRup.GetMean()
#alpha_shift3srdo = h_alpha_SHIFT3SRdo.GetMean()
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
err_fitsr5up   = 100.*(alpha_fitsr5up-alpha)/alpha
err_fitsr5do   = 100.*(alpha_fitsr5do-alpha)/alpha
err_fitsr10up  = 100.*(alpha_fitsr10up-alpha)/alpha
err_fitsr10do  = 100.*(alpha_fitsr10do-alpha)/alpha
err_fitsr15up  = 100.*(alpha_fitsr15up-alpha)/alpha
err_fitsr15do  = 100.*(alpha_fitsr15do-alpha)/alpha
err_fitsr20up  = 100.*(alpha_fitsr20up-alpha)/alpha
err_fitsr20do  = 100.*(alpha_fitsr20do-alpha)/alpha
err_fitsr25up  = 100.*(alpha_fitsr25up-alpha)/alpha
err_fitsr25do  = 100.*(alpha_fitsr25do-alpha)/alpha
err_fitsr30up  = 100.*(alpha_fitsr30up-alpha)/alpha
err_fitsr30do  = 100.*(alpha_fitsr30do-alpha)/alpha
#err_shift5srup = 100.*(alpha_shift5srup-alpha)/alpha
#err_shift5srdo = 100.*(alpha_shift5srdo-alpha)/alpha
#err_shift4srup = 100.*(alpha_shift4srup-alpha)/alpha
#err_shift4srdo = 100.*(alpha_shift4srdo-alpha)/alpha
#err_shift3srup = 100.*(alpha_shift3srup-alpha)/alpha
#err_shift3srdo = 100.*(alpha_shift3srdo-alpha)/alpha
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
print "BKG SHAPE (from SR FIT 0.0% line + norm) err =",round(err_fitsr0 ,my_round),"%"
print "BKG SHAPE (from SR FIT 0.5% line + norm) err =",round(err_fitsr5up ,my_round),",",round(err_fitsr5do ,my_round),"%"
print "BKG SHAPE (from SR FIT 1.0% line + norm) err =",round(err_fitsr10up,my_round),",",round(err_fitsr10do,my_round),"%"
print "BKG SHAPE (from SR FIT 1.5% line + norm) err =",round(err_fitsr15up,my_round),",",round(err_fitsr15do,my_round),"%"
print "BKG SHAPE (from SR FIT 2.0% line + norm) err =",round(err_fitsr20up,my_round),",",round(err_fitsr20do,my_round),"%"
print "BKG SHAPE (from SR FIT 2.5% line + norm) err =",round(err_fitsr25up,my_round),",",round(err_fitsr25do,my_round),"%"
print "BKG SHAPE (from SR FIT 3.0% line + norm) err =",round(err_fitsr30up,my_round),",",round(err_fitsr30do,my_round),"%"
nbins=150.
bin_width=(300.-0.)/nbins
#print "BKG SHIFT (from SR FIT,",round(5.*bin_width),"GeV) err =",round(err_shift5srup,my_round),",",round(err_shift5srdo,my_round),"%"
#print "BKG SHIFT (from SR FIT,",round(4.*bin_width),"GeV) err =",round(err_shift4srup,my_round),",",round(err_shift4srdo,my_round),"%"
#print "BKG SHIFT (from SR FIT,",round(3.*bin_width),"GeV) err =",round(err_shift3srup,my_round),",",round(err_shift3srdo,my_round),"%"
print "BKG SHIFT (from SR FIT,",round(2.*bin_width),"GeV) err =",round(err_shift2srup,my_round),",",round(err_shift2srdo,my_round),"%"
print "BKG SHIFT (from SR FIT,",round(1.*bin_width),"GeV) err =",round(err_shift1srup,my_round),",",round(err_shift1srdo,my_round),"%"

