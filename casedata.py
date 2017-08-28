import math
import numpy as np
import glob
import fileinput


class CaseDataCoeficients(object):
    def __init__(self):
        self.coef_creditscore = 1.0
        self.coef_requestamount = 1.0
        self.coef_numberofoffers = 1.0
        self.coef_loangoal = 1.0
        self.coef_jaccard = 1.0
        self.coef_editdist = 1.0

        self.max_numberofoffers = -1.0
        self.max_creditscore = -1.0
        self.max_requestamount = -1.0

    def set_coefs(self,list):
        self.coef_creditscore = list[0]
        self.coef_requestamount = list[1]
        self.coef_numberofoffers = list[2]
        self.coef_loangoal = list[3]
        self.coef_jaccard = list[4]
        self.coef_editdist = list[5]

class CaseData(object):
    def __init__(self, casename, endsituation, requestamount, creditscore, variant,
                 numberofoffers, loangoal):
        self.casename = casename
        self.endsituation = endsituation
        self.requestamount = requestamount
        self.creditscore = creditscore
        self.variant = variant
        self.numberofoffers = numberofoffers
        self.loangoal = loangoal

    @classmethod
    def GetNumberOfFeatures(cf):
        return 4

    @classmethod
    def ConvertCaseToPoint(p):
        return np.array([p.variant, p.requestamount, p.creditscore, p.numberofoffers])



def ReadData(cf):
    casedata = []
    index = 0
    with open('./case_data.txt', 'r') as f:
        # skip header
        first_line = f.readline()
        for line in f:
            coefs = line.split()
            requestamount = float(coefs[2])
            creditscore = float(coefs[3])
            numberofoffers = float(coefs[5])
            cf.max_requestamount = np.fmax(cf.max_requestamount, float(requestamount))
            cf.max_creditscore = np.fmax(cf.max_creditscore, float(creditscore))
            cf.max_numberofoffers = np.fmax(cf.max_numberofoffers, float(numberofoffers))
            cd = CaseData(coefs[0], int(coefs[1]), float(coefs[2]), float(coefs[3]), float(coefs[4]), float(coefs[5]), coefs[6])
            casedata.append(cd)
            index = index + 1

    return casedata


def UpdateMaxValues(number_of_cases, case_datas, cf):
    cf.max_numberofoffers = -1.0
    cf.max_creditscore = -1.0
    cf.max_requestamount = -1.0
    for i in range(0, number_of_cases):
        cf.max_requestamount = np.fmax(cf.max_requestamount, case_datas[i].requestamount)
        cf.max_creditscore = np.fmax(cf.max_creditscore, case_datas[i].creditscore)
        cf.max_numberofoffers = np.fmax(cf.max_numberofoffers, case_datas[i].numberofoffers)



#OUR MEASURE
def CompositeDistance(a, b, cf, jaccard, editdist):

    return 1.0 - (math.exp(-cf.coef_creditscore * abs(a.creditscore - b.creditscore) / cf.max_creditscore) *
                  math.exp(-cf.coef_requestamount * abs(a.requestamount - b.requestamount) / cf.max_requestamount) *
                  math.exp(-cf.coef_numberofoffers * abs(a.numberofoffers - b.numberofoffers) / cf.max_numberofoffers) *
                  math.exp(-cf.coef_loangoal * (a.loangoal != b.loangoal)) *
                  math.exp(-cf.coef_jaccard * jaccard) * math.exp(-cf.coef_editdist * editdist))
