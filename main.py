
import dataprovider
import mds


if __name__ == '__main__':


    #TO DO -> interface and export data

    #pesos na ordem
    #cf.creditscore = 1.0
    #cf.requestamount = 1.0
    #cf.numberofoffers = 1.0
    #cf.loangoal = 1.0
    #cf.editdist = 1.0
    # cf.jaccard = 1.0
    weights = [1.0,0.5,0.0,0.5,1.0,0.0]
    #sample size
    size = 100

    #params = size of sample set and list of weight
    data = dataprovider.DataProvider(size, weights)
    endsit = data.GetEndSituation()
    dots = data.Calculate()
    pos = mds.mdsGen(dots,endsit)
    mds.drawPlot(size,pos,endsit)
