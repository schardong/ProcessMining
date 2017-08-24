import casedata
import numpy as np
import pandas as pd
from multiprocessing import Pool

class DataProvider(object):
    def __init__(self,size,list_weigth):
        self.size = size
        self.caseDataCoefs = casedata.CaseDataCoeficients()
        self.caseDataCoefs.set_coefs(list_weigth)
        self.casedata_v = np.array(casedata.ReadData(self.caseDataCoefs))
        self.editDist = np.array(pd.read_csv('editDist.csv', sep=';',header=None))
        self.jaccard = np.array(pd.read_csv('all_SimilarityMatrix.csv', sep=';', header=None))
        self.list_end_info = np.zeros(self.size)
        for i in range(self.size):
            self.list_end_info[i] = self.casedata_v[i].endsituation

    def GetEndSituation(self):
        return self.list_end_info

    def DataProviderMDS(self,initial):
         m = np.zeros(shape=(self.size))
         for j in range(0,self.size):
             vari = int(self.casedata_v[initial].variant) - 1
             varj = int(self.casedata_v[j].variant) - 1
             edition = float(self.editDist[vari,varj])
             jac = float(self.jaccard[vari,varj])
             m[j] = casedata.CompositeDistance(self.casedata_v[initial], self.casedata_v[j],self.caseDataCoefs, jac, edition)
         return m
    
    def Calculate(self):
        print("calculando")
        pool = Pool(processes=8)
        list_start_vals = range(0, self.size)
        array_2D = np.array(pool.map(self.DataProviderMDS, list_start_vals))
        pool.close() # ATTENTION HERE
        print(array_2D)
        return array_2D
