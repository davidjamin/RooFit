import ROOT as r
#r.gROOT.SetBatch(r.kTRUE)
#infile = r.TFile.Open('/afs/cern.ch/user/d/djamin/public/FCC/20180403_tth_boosted/tmp/root_ttH_full_2gevbins/root_ttH/histos.root')
infile = r.TFile.Open('/afs/cern.ch/work/s/selvaggi/private/Analysis/FCC/FlatTreeAnalyzer/tth_boosted/root_ttH/histos.root')
Rebin=1


def makePseudoExp(tth_datahist, ttz_datahist, sig, alpha, ntth, nttz, alpha_val, alpha_err):
 # generate datasets

    print '================================================================================================='
    print '================================================================================================='


    gen_tth = p_tth.generate(r.RooArgSet(x), ntth, r.RooFit.Extended())
    gen_ttz = p_ttz.generate(r.RooArgSet(x), nttz, r.RooFit.Extended())

    d_ttcomb = gen_tth
    d_ttcomb.append(gen_ttz)

    #d_ttcomb.plotOn(frame)

    sig.fitTo(d_ttcomb, r.RooFit.SumW2Error(False), r.RooFit.PrintLevel(-1))
    #sig.plotOn(frame, r.RooFit.LineColor(r.kBlack))
    #frame.Draw()
    #alpha.Print()

    print alpha.getError(), alpha.getVal()
    alpha.Print()

    #ratio = alpha.getVal()*(ntth+nttz)/ntth
    #ratio_err = alpha.getError()*(ntth+nttz)/ntth
    ratio = (1-alpha.getVal())/(alpha.getVal())
    ratio_err = alpha.getError()


    print ratio, ratio_err

    alpha_err.Fill(ratio_err)
    alpha_val.Fill(ratio)



x = r.RooRealVar("x", "mjj", 0, 300)
#######ttH
h_tth=infile.Get('ttH_sel3_h_mbb')
h_tth.Rebin(Rebin)
d_tth = r.RooDataHist("d_tth", "d_tth", r.RooArgList(x),r.RooFit.Import(h_tth))
p_tth = r.RooHistPdf("p_tth", "p_tth", r.RooArgSet(x),d_tth)
frame = x.frame(r.RooFit.Title("ttH"))
p_tth.plotOn(frame, r.RooFit.MarkerColor(r.kRed), r.RooFit.LineColor(r.kRed) )


#######ttZ
h_ttz=infile.Get('ttZ_sel3_h_mbb')
h_ttz.Rebin(Rebin)
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x),r.RooFit.Import(h_ttz))
p_ttz = r.RooHistPdf("p_ttz", "p_ttz", r.RooArgSet(x),d_ttz)
#frame2 = x.frame(r.RooFit.Title("CB fit ttZ"))
p_ttz.plotOn(frame)
#frame.Draw()

# add pdfs

alpha = r.RooRealVar("alpha", "fraction of component in signal", 0.7167035, 0., 1.)
#alpha.setConstant(True)
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(p_tth, p_ttz),r.RooArgList(alpha))
#sig.plotOn(frame, r.RooFit.MarkerColor(r.kBlack), r.RooFit.LineColor(r.kBlack))
frame.Draw()
#
#def :

ntth = 158836
nttz = 85785

ntth = int(0.99*ntth)
nttz = int(0.99*nttz)

alpha_val = r.TH1F("alpha_val", "alpha_val", 100, 0.50, 0.58)
alpha_err = r.TH1F("alpha_err", "alpha_err", 100, 0.001, 0.003)


for i in xrange(1000):
    makePseudoExp(p_tth, p_ttz, sig, alpha, ntth, nttz, alpha_val, alpha_err)


outfile = r.TFile('tth_fit.root','RECREATE')
alpha_val.Write()
alpha_err.Write()



#input("Press Enter to continue...")

'''

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

'''
