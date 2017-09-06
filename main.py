
import dataprovider
import learn
import numpy as np
from matplotlib import pyplot as plt


if __name__ == '__main__':


    #TO DO -> interface and export data

    #pesos na ordem
    #cf.creditscore = 1.0
    #cf.requestamount = 1.0
    #cf.numberofoffers = 1.0
    #cf.loangoal = 1.0
    #cf.editdist = 1.0
    # cf.jaccard = 1.0

    #click botão esquerdo para adicionar pontos da área de seleção, clique botão direito para confirmar seleção
    # tecle s para salvar
    # tecle z para limpar seleção

    weights = [1.0,0.5,0.0,0.5,1.0,0.0]
    #sample size
    size = 10000


    #params = size of sample set and list of weight
    data = dataprovider.DataProvider(size, weights)
    endsit = data.GetEndSituation()
    dots = data.Calculate()

    # using Multidimensional Scalling
    mds = learn.mdsClass()
    pos1 = mds.mdsGen(dots)
    plot1 = learn.chart("MDS")
    plot1.saveCallback(data.SaveExportedData)
    plot1.drawPlot(size,pos1,endsit)

    #using t-distributed stochastic neighbor embedding
    # https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding
    tsne = learn.tsneClass()
    pos2 = tsne.tsneGen(dots)
    d = 2 * (pos2 - np.max(pos2)) / -np.ptp(pos2) - 1
    print(d)
    plot2 = learn.chart("t-distributed_stochastic_neighbor_embedding")
    plot2.saveCallback(data.SaveExportedData)
    plot2.drawPlot(size, d, endsit)

    #using Spectral embedding for non-linear dimensionality reduction.

    spe = learn.spectralEmbeddingClass()
    pos3 = spe.genSPE(dots)
    d = 2 * (pos3 - np.max(pos3)) / -np.ptp(pos3) - 1
    print(d)
    plot3 = learn.chart("Spectral_embedding")
    plot3.saveCallback(data.SaveExportedData)
    plot3.drawPlot(size, d, endsit)

    #mostra todos os gráficos
    plt.show()