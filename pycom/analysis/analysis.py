import pandas as pd
import os
from pycom import PyCom
import numpy as np
from pycom.selector import MatrixFormat

class CoMAnalysis(object):
    """

    CoMAnalysis provides functions to manipulate coevolution matrices from the pandas dataframe

    Usage:

    Parameters:


    """
    def __init__(self):
        pass



    def calculate_scaled_coevolution_matrix(self,matrix) -> np.ndarray:
        '''
        Scales coevolution matrix by average as GREMLIN
        :param matrix:
        :return: scaled_matrix
        '''
        if(matrix.shape[0]==0):
            print("This is an empty matrix. Check your query.")
            exit()
        _matrix_average=np.average(matrix)
        _scaled_matrix=matrix
        if(_matrix_average>0):
            _scaled_matrix=matrix/_matrix_average
            _scaled_matrix[_scaled_matrix < np.average(_scaled_matrix)] = 0
        return _scaled_matrix

    def scale_and_normalise_coevolution_matrices(self,df: pd.DataFrame,normalise_matrix=True) -> pd.DataFrame:
        '''
        scales coevolution matrix by average, set all values <average to 0 --> S
        scale S by max of all S in the data frame and add additional column of normalised matrices
        :param df:
        :return: data frame with normalised and scaled coevolution matrix columns
        '''
        _list_matrix_N = []
        _list_matrix_S = []
        '''
            get scaled coevolution matrices
        '''
        _max_of_SM=[]
        for _matrix in df['matrix']:
            _scaled_M = self.calculate_scaled_coevolution_matrix(_matrix)
            _list_matrix_S.append(_scaled_M)
            _max_of_SM.append(np.max(_scaled_M))
        df["matrix_S"] = _list_matrix_S
        if (normalise_matrix):
            '''
                get the max of scaled matrices
            '''
            _all_max = np.max(_max_of_SM)

            '''
                normalise all scaled matrices by ma
            '''

            for _matrix in _list_matrix_S:
                _list_matrix_N.append(_matrix/_all_max)
            df["matrix_N"] = _list_matrix_N


        return df

    def _get_top_scoring_residues(self,_matrix,res_gap=5,percentile=90):
        '''

        :param _matrix:
        :param res_gap:
        :param percentile:
        :return: None
        '''
        self.out_top_pairs="%9s%9s%12s\n"%("ResID_A","ResID_B","Score")
        max_i,max_j = _matrix.shape
        _coevolution_percentile_score = 1
        if(percentile>0):
            _coevolution_percentile_score = np.percentile(_matrix,percentile)
        _top_list=[]
        for i in range(max_i):
            _upshift=i+res_gap
            if(_upshift<max_j):
                for j in range(max_j):
                    if(j>_upshift):
                        _c_score = _matrix[i,j]
                        if(_c_score>=_coevolution_percentile_score):
                            _top_list.append([i+1,j+1,_c_score])
        _top_list.sort(key=lambda k:k[2],reverse=True)
        for resA,resB,score in _top_list:
            self.out_top_pairs+="%9d%9d%12.5f\n"%(resA,resB,score)
    def _save_file(self,fname,out):
        '''
            svae a string data structure to a txt file
        :param fname:
        :param out:
        :return: None
        '''
        f=open(fname,'w')
        f.write(out)
        f.close()
        print("Saved file : %s"%(fname))
    def save_top_scoring_residue_pairs(self,df:pd.DataFrame,data_folder="output",matrix_type="matrix_S",res_gap=5,percentile=90):
        '''

        Extract top percentile (default: 90) pairs from the chosen matrix and write them in sorted order to a ASCII txt file

        :param df: data frame with coevolution matrices
        :param data_folder: output folder for all files
        :param matrix_type: matrix or matrix_S or matrix_N
        :param res_gap: 5 (default)
        :param percentile: 90
        :return: None
        '''
        if (os.path.isdir(data_folder)==False):
            os.mkdir(data_folder)
        for index,rows in df.iterrows():
            self._get_top_scoring_residues(rows[matrix_type],res_gap=res_gap,percentile=percentile)
            fname = data_folder + "/" + rows["uniprot_id"] + "_Pairs.txt"
            self._save_file(fname,self.out_top_pairs)
