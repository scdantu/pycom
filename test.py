from pycom import PyCom,ProteinParams,CoMAnalysis
import numpy as np
if __name__ == '__main__':
    #set the path to the database 
    database_folder_path="/Volumes/mason/Work/Sarath/Research/pycom/"
    #matrix file name and path
    file_matrix_db = database_folder_path+"pycom.mat"
    #protein database file name and path
    file_protein_db= database_folder_path+"pycom.db"
    pyc = PyCom(db_path=file_protein_db, mat_path=file_matrix_db)
    #pyc = PyCom(remote=True)
    query_parameters={ProteinParams.ID:"Q65209"}
    df  =   pyc.find(query_parameters)
    df  =   pyc.load_matrices(df)
    
    print(df)
    com = CoMAnalysis()
    
    df_N=com.scale_and_normalise_coevolution_matrices(df)
    df_top_list=com.get_top_scoring_residues(df_N['matrix_S'][0])
        
    x_df=com.get_residue_frequencies(df_top_list)
    print(x_df)
    com.save_top_scoring_residue_pairs(df_N,data_folder="/Users/sdantu/Work/output",res_gap=10,percentile=0)
    #for index,rows in df_N.iterrows():
    #    print(rows["matrix"].max(),rows["matrix_S"].max(),rows["matrix_N"].max())


