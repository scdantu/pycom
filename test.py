from pycom import PyCom,CoMAnalysis
import numpy as np
if __name__ == '__main__':

    pyc = PyCom(remote=True)
    df = pyc.find(page=1, matrix=True)
    print(df.loc[1])
    com = CoMAnalysis()
    #df_N=com.scale_and_normalise_coevolution_matrices(df)
    #com.save_top_scoring_residue_pairs(df_N,data_folder="/Users/sdantu/Work/output",res_gap=10,percentile=0)
    #for index,rows in df_N.iterrows():
    #    print(rows["matrix"].max(),rows["matrix_S"].max(),rows["matrix_N"].max())


