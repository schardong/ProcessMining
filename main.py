
import dataprovider
import mds
import matplotlib.patches as mpatches
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
    weights = [1.0,1.0,1.0,1.0,1.0,1.0]
    #sample size
    size = 15000

    #params = size of sample set and list of weight
    data = dataprovider.DataProvider(size, weights)
    endsit = data.GetEndSituation()
    dots = data.Calculate()
    pos = mds.mdsGen(dots,endsit)


    fig, ax = plt.subplots()
    color = ['green', 'red', 'blue']
    labels = ['Aproved','Denied','Canceled']

    for i in range(size):
      ax.scatter(pos[i, 0], pos[i, 1], c=color[int(endsit[i])],
                  alpha=0.7, edgecolors='none')

    green_patch = mpatches.Patch(color='green', label='Aproved')
    red_patch = mpatches.Patch(color='red', label='Denied')
    blue_patch = mpatches.Patch(color='blue', label='Canceled')
    ax.legend(handles=[green_patch,red_patch,blue_patch])

    plt.show()