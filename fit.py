import ROOT as r
r.gROOT.SetBatch(r.kTRUE)
infile = r.TFile.Open('/afs/cern.ch/user/d/djamin/public/FCC/20180403_tth_boosted/tmp/root_ttH_full_2gevbins/root_ttH/histos.root')
Rebin=2


#######ttH
h_tth=infile.Get('ttH_sel1_h_mjj_l2')
h_tth.Rebin(Rebin)
x_tth = r.RooRealVar("x_tth", "mjj", 50, 140)
d_tth = r.RooDataHist("d_tth", "d_tth", r.RooArgList(x_tth),r.RooFit.Import(h_tth))
frame = x_tth.frame(r.RooFit.Title("CB fit ttH"))
d_tth.plotOn(frame, r.RooFit.MarkerColor(r.kRed), r.RooFit.LineColor(r.kRed) )

# Fit a CB p.d.f to the data
m0_tth    = r.RooRealVar("m0_tth","m0_tth",125,0,300)
alpha_tth = r.RooRealVar("alpha_tth","alpha_tth",1,0,10)
n_tth     = r.RooRealVar("n_tth","n_tth",1, 0.1,10)
sigma_tth = r.RooRealVar("sigma_tth", "sigma_tth", 20, 1, 100)

CB_tth = r.RooCBShape("CB_tth", "CB_tth", x_tth, m0_tth, sigma_tth, alpha_tth, n_tth)
CB_tth.fitTo(d_tth)
CB_tth.plotOn(frame, r.RooFit.LineColor(r.kRed))

#######ttZ
h_ttz=infile.Get('ttZ_sel1_h_mjj_l2')
h_ttz.Rebin(Rebin)
x_ttz = r.RooRealVar("x_ttz", "mjj", 50, 100)
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x_ttz),r.RooFit.Import(h_ttz))
frame2 = x_ttz.frame(r.RooFit.Title("CB fit ttZ"))
d_ttz.plotOn(frame2)

# Fit a CB p.d.f to the data
m0_ttz    = r.RooRealVar("m0_ttz","m0_ttz",90,0,300)
alpha_ttz = r.RooRealVar("alpha_ttz","alpha_ttz",1,0,10)
n_ttz     = r.RooRealVar("n_ttz","n_ttz",1, 0.1,10)
sigma_ttz = r.RooRealVar("sigma_ttz", "sigma_ttz", 20, 1, 100)

CB_ttz = r.RooCBShape("CB_ttz", "CB_ttz", x_ttz, m0_ttz, sigma_ttz, alpha_ttz, n_ttz)
CB_ttz.fitTo(d_ttz)
CB_ttz.plotOn(frame2, r.RooFit.LineColor(r.kBlack))


#######COMB
h_ttcomb=h_ttz+h_tth
x_ttcomb = r.RooRealVar("x_ttcomb", "mjj", 50, 140)
d_ttcomb = r.RooDataHist("d_ttcomb", "d_ttcomb", r.RooArgList(x_ttcomb),r.RooFit.Import(h_ttcomb))
frame3 = x_ttcomb.frame(r.RooFit.Title("CB fit ttcomb"))
d_ttcomb.plotOn(frame3)
CB_ttz = r.RooCBShape("CB_ttz", "CB_ttz", x_ttcomb, m0_ttz, sigma_ttz, alpha_ttz, n_ttz)
CB_tth = r.RooCBShape("CB_tth", "CB_tth", x_ttcomb, m0_tth, sigma_tth, alpha_tth, n_tth)

sigfrac = r.RooRealVar("sigfrac", "fraction of component in signal", 0.8, 0., 1.)
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(CB_tth, CB_ttz),r.RooArgList(sigfrac))
sig.fitTo(d_ttcomb)
sig.plotOn(frame3, r.RooFit.LineColor(r.kBlack))


frame4 = x_ttcomb.frame(r.RooFit.Title("CB fit ttcomb"))
d_ttcomb.plotOn(frame4)
sig.plotOn(frame4, r.RooFit.LineColor(r.kBlack))

sigtth = r.RooArgSet(CB_tth)
sig.plotOn(frame4, r.RooFit.Components(sigtth), r.RooFit.LineStyle(r.kDashed))
sigttz = r.RooArgSet(CB_ttz)
sig.plotOn(frame4, r.RooFit.Components(sigttz), r.RooFit.LineStyle(r.kDashed))



# Draw all frames on a canvas
c = r.TCanvas("CBfit", "CBfit", 800, 800)
c.Divide(2, 2)
c.cd(1)
r.gPad.SetLeftMargin(0.15)
#r.gPad.SetLogy()
frame.GetYaxis().SetTitleOffset(1.4)
frame.Draw()
c.cd(2)
r.gPad.SetLeftMargin(0.15)
frame2.GetYaxis().SetTitleOffset(1.4)
frame2.Draw()
c.cd(3)
r.gPad.SetLeftMargin(0.15)
frame3.GetYaxis().SetTitleOffset(1.4)
frame3.Draw()
c.cd(4)
r.gPad.SetLeftMargin(0.15)
frame4.GetYaxis().SetTitleOffset(1.4)
frame4.Draw()
c.SaveAs("CBfit.png")


c1 = r.TCanvas("CBfit_comb", "CBfit", 600, 800)
frame3.Draw()
c1.SaveAs("CBfit_comb.png")


