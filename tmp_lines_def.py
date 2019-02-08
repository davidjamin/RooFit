import ROOT as r
percent = 3.
percent /= 100.
parl = [percent/25., 1.-4.*percent]
low_x=50
high_x=250
my_line = r.TF1("my_line","pol1", low_x, high_x)
my_line.SetParameters(parl[1],parl[0])
my_line.SetLineWidth(4)
my_line.Draw()
percent = 1.5
percent /= 100.
parl2 = [percent/25., 1.-4.*percent]
my_line2 = r.TF1("my_line2","pol1", low_x, high_x)
my_line2.SetParameters(parl2[1],parl2[0])
my_line2.SetLineColor(r.kBlue)
my_line2.SetLineWidth(4)
my_line2.Draw("same")
percent = 0.5
percent /= 100.
parl3 = [percent/25., 1.-4.*percent]
my_line3 = r.TF1("my_line3","pol1", low_x, high_x)
my_line3.SetParameters(parl3[1],parl3[0])
my_line3.SetLineColor(r.kGreen+3)
my_line3.SetLineWidth(4)
my_line3.Draw("same")
my_line4 = r.TF1("my_line4","pol1", low_x, high_x)
my_line4.SetParameters(1.03,0.)
my_line4.SetLineColor(r.kBlack)
my_line4.SetLineStyle(r.kDashed)
my_line4.Draw("same")
my_line5 = r.TF1("my_line5","pol1", low_x, high_x)
my_line5.SetParameters(1.015,0.)
my_line5.SetLineColor(r.kBlack)
my_line5.SetLineStyle(r.kDashed)
my_line5.Draw("same")
my_line6 = r.TF1("my_line6","pol1", low_x, high_x)
my_line6.SetParameters(1.005,0.)
my_line6.SetLineColor(r.kBlack)
my_line6.SetLineStyle(r.kDashed)
my_line6.Draw("same")
my_line7 = r.TLine(125.,0.93,125.,1.19)
my_line7.SetLineColor(r.kBlack)
my_line7.SetLineStyle(r.kDashed)
my_line7.SetLineWidth(2)
my_line7.Draw("same")

