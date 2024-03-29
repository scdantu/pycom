import os
from collections import Counter

import numpy as np
import pandas as pd


class CoMAnalysis(object):
    """
    CoMAnalysis provides functions to manipulate coevolution matrices from
    the pandas dataframe and save the interesting residue pairs into an ASCII file
    """

    def __init__(self):
        self.df_top_scores = pd.DataFrame()
        self.df_residue_counts = pd.DataFrame()

    def add_contact_predictions(self, df: pd.DataFrame, contact_factor: int = 1.5):
        """
        Takes in a datafrmae containing coevolution matrices ('matrix' column) and adds a column
        with contact predictions ('contact_matrix' column).

        By default, the top 1.5xL pairs are returned as contact predictions, L being the length of the protein
        This can be modified by changing the contact_factor parameter.

        :param df: dataframe with coevolution matrices (matrix column)
        :param contact_factor: 1.5 (default)
        :return: dataframe with contact predictions (contact_matrix column)
        """
        # assert mode in ['CCMpred'], "Only CCMpred is supported at the moment"
        assert 'matrix' in df.columns, "No coevolution matrix column in dataframe"
        assert contact_factor > 0, "contact_factor should be greater than 0 (default: 1.5)"

        # scale_and_normalise_coevolution_matrices
        scaled_mat = CoMAnalysis.scale_and_normalise_coevolution_matrices(df, normalise_matrix=False)
        # top_contacts = self.get_top_contacts_from_coevolution(mat)
        top_contact_mat = scaled_mat.apply(
            lambda row: self.scaled_matrix_to_contact_predictions(row['matrix_S'], contact_factor), axis=1)
        df.drop(columns=['matrix_S'], inplace=True)
        df['contact_matrix'] = top_contact_mat
        return df

    def scaled_matrix_to_contact_predictions(self, scaled_matrix, num_contact_factor=1.5):
        """
        Takes in a scaled coevolution matrix and returns a contact prediction matrix

        By default, the leading diagonal (self contacts) are not set to 1.

        :param scaled_matrix: scaled coevolution matrix
        :param num_contact_factor: 1.5 (default)
        :return: contact prediction matrix
        """
        self.get_top_contacts_from_coevolution(scaled_matrix, num_contact_factor)

        contact_mat = np.zeros(scaled_matrix.shape)
        top_contacts = self.get_top_contacts_from_coevolution(scaled_matrix)

        res_a = np.array(top_contacts['ResA'].values, dtype=int) - 1
        res_b = np.array(top_contacts['ResB'].values, dtype=int) - 1

        # contact_matrix = np.eye(scaled_matrix.shape[0], dtype=np.int8)  # set diagonal to 1, if needed
        contact_mat[res_a, res_b] = 1
        contact_mat[res_b, res_a] = 1

        return contact_mat

    @staticmethod
    def calculate_scaled_coevolution_matrix(matrix) -> np.ndarray:
        """
        Scales coevolution matrix by average
        :param matrix:
        :return: scaled_matrix
        """
        if matrix.shape[0] == 0:
            print("This is an empty matrix. Check your query.")
            exit()
        _matrix_average = np.average(matrix)
        _scaled_matrix = matrix
        if _matrix_average > 0:
            _scaled_matrix = matrix / _matrix_average
            _scaled_matrix[_scaled_matrix < np.average(_scaled_matrix)] = 0
        return _scaled_matrix

    @staticmethod
    def scale_and_normalise_coevolution_matrices(df: pd.DataFrame, normalise_matrix=True) -> pd.DataFrame:
        """
        scales coevolution matrix by average, set all values <average to 0 --> S
        scale S by max of all S in the data frame and add additional column of normalised matrices
        :param df:
        :param normalise_matrix:
        :return: data frame with normalised and scaled coevolution matrix columns
        """
        _list_matrix_N = []
        _list_matrix_S = []

        # get scaled coevolution matrices
        _max_of_SM = []
        for _matrix in df['matrix']:
            _scaled_M = CoMAnalysis.calculate_scaled_coevolution_matrix(_matrix)
            _list_matrix_S.append(_scaled_M)
            _max_of_SM.append(np.max(_scaled_M))
        df["matrix_S"] = _list_matrix_S
        if normalise_matrix:
            # get the max of scaled matrices
            _all_max = np.max(_max_of_SM)

            # normalise all scaled matrices by max of all scaled matrices
            for _matrix in _list_matrix_S:
                _list_matrix_N.append(_matrix / _all_max)
            df["matrix_N"] = _list_matrix_N

        return df

    def get_top_scoring_residues(self, matrix, res_gap=5, percentile=90):
        """
        returns top scoring residues using percentile cut-off

        :param matrix:
        :param res_gap:
        :param percentile:
        :return: data frame with top residue pairs
        """

        max_i, max_j = matrix.shape
        _coevolution_percentile_score = 1
        if percentile > 0:
            _coevolution_percentile_score = np.percentile(matrix, percentile)

        _top_residues_list = []
        for i in range(max_i):
            _upshift = i + res_gap
            if _upshift < max_j:
                for j in range(max_j):
                    if j > _upshift:
                        _c_score = matrix[i, j]
                        if _c_score >= _coevolution_percentile_score:
                            _top_residues_list.append([i + 1, j + 1, _c_score])
        _top_residues_list.sort(key=lambda k: k[2], reverse=True)
        self.df_top_scores = pd.DataFrame(_top_residues_list, columns=["ResA", "ResB", "coevolution_score"])

        self.df_top_scores['ResA'] = self.df_top_scores['ResA'].astype('str')
        self.df_top_scores['ResB'] = self.df_top_scores['ResB'].astype('str')
        return self.df_top_scores

    def get_top_contacts_from_coevolution(self, scaled_matrix, num_contact_factor=1.5):
        """
            returns 'N' top scoring residues as a dataframe
            by default, consistent with GREMLIN, top 1.5xL pairs are returned, L being the length of the protein

        :param scaled_matrix:
        :param num_contact_factor:
        :return: data frame with top residue pairs
        """
        df_top_contacts = []
        max_i, max_j = scaled_matrix.shape

        if max_i == 0:
            print("Matrix is empty. Please check and provide a scaled matrix")
            exit()

        if max_i > 0:
            num_top_pairs = round(num_contact_factor * max_i)
            self.get_top_scoring_residues(scaled_matrix, 3, 75)
            if len(self.df_top_scores) > num_top_pairs:
                df_top_contacts = self.df_top_scores.iloc[:num_top_pairs]
            else:
                df_top_contacts = self.df_top_scores

        return df_top_contacts

    def get_residue_frequencies(self, top_residue_pairs):
        """
        Calculate the residue frequencies count from the top_scoring_residue pairs list

        :param top_residue_pairs:
        :return: dataframe with residueID and count df_res_count
        """

        if len(top_residue_pairs) == 0:
            print("Length of the residue pairs list is 0. Nothing to be done.")
        else:

            _top_res_pairs_array = np.asarray(top_residue_pairs)
            _res_array_count = np.array(
                np.unique(np.concatenate((_top_res_pairs_array[:, 0], _top_res_pairs_array[:, 1])),
                          return_counts=True)).T
            df_res_count = pd.DataFrame(_res_array_count, columns=["residueID", "count"])
            df_res_count = df_res_count.sort_values(by=['count'], ascending=False)

            _full_residue_list = top_residue_pairs["ResA"].to_list() + top_residue_pairs["ResB"].to_list()

            _dict_residue_counts = dict(Counter(_full_residue_list))
            self.df_residue_counts = pd.DataFrame.from_dict(
                {"residueID": _dict_residue_counts.keys(), "count": _dict_residue_counts.values()}
            )

        return self.df_residue_counts

    def save_top_scoring_residue_pairs(self, df: pd.DataFrame, data_folder="output", matrix_type="matrix_S", res_gap=5,
                                       percentile=90):
        """

        Extract top percentile (default: 90) pairs from the chosen matrix
        and write them in sorted order to an ASCII txt file

        :param df: data frame with coevolution matrices
        :param data_folder: output folder for all files
        :param matrix_type: matrix or matrix_S or matrix_N
        :param res_gap: 5 (default)
        :param percentile: 90
        :return: None
        """
        if not os.path.isdir(data_folder):
            os.mkdir(data_folder)
        for index, rows in df.iterrows():
            self.get_top_scoring_residues(rows[matrix_type], res_gap=res_gap, percentile=percentile)
            fname = data_folder + "/" + rows["uniprot_id"] + "_Pairs.csv"
            self.df_top_scores.to_csv(fname, index=False)
