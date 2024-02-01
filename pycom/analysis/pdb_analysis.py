"""
For validation and analysis we have created a number of functions and tooling to help extract data from PDB files

The functions of most relevance are:
 - a C++ script to extract residues and their coordinates from a PDB file (pdb2res.cpp)
 - A number of Python methods for converting these into distance matrices and contact maps (pdb_analysis.py)
   -
"""
import os
import subprocess

import numpy as np
import pandas as pd

from scipy.spatial.distance import pdist, squareform

from . import pdb2res


def get_residue_coordinates(pdb_ent_gz_file_path, fmt='pandas') -> pd.DataFrame or np.ndarray:
    assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
    assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'
    assert fmt in ['pandas', 'numpy'], 'Format must be either "pandas" or "numpy"'

    pdb_data = pdb2res.residues_from_pdb(pdb_ent_gz_file_path)

    if fmt == 'numpy':
        return pdb_data
    elif fmt == 'pandas':
        return pd.DataFrame(pdb_data, columns=['AA', 'resseq', 'x', 'y', 'z'])


def get_distance_matrix(pdb_ent_gz_file_path) -> np.ndarray:
    """
    Returns a distance matrix from a PDB file
    :param pdb_ent_gz_file_path: path to PDB file
    :return: distance matrix
    """
    assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
    assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'

    coords = get_residue_coordinates(pdb_ent_gz_file_path, fmt='numpy')
    coords = coords[:, 2:].astype(float)

    return squareform(pdist(coords))


def get_contact_map(pdb_ent_gz_file_path, cutoff=8) -> np.ndarray:
    """
    Returns a contact map from a PDB file

    Possible values:
    0: no contact
    1: contact
    -1: unknown position (nan)

    :param pdb_ent_gz_file_path: path to PDB file
    :param cutoff: distance cutoff for contact (in Angstroms, default 8Å)
    :return: contact map
    """
    assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
    assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'

    coords = get_residue_coordinates(pdb_ent_gz_file_path, fmt='numpy')
    coords = coords[:, 2:].astype(float)

    print(coords.shape, coords.dtype, coords)

    dist_mat = squareform(pdist(coords))

    contact_matrix = 1 - np.heaviside(dist_mat - cutoff, 0)
    contact_matrix[np.where(np.isnan(contact_matrix))] = -1  # set nan values to -1
    contact_matrix = contact_matrix.astype(int)  # convert to int

    return contact_matrix


class PDBAnalysis:
    """
    Class to analyse PDB files and extract residue contacts
    """


@DeprecationWarning
class _PDBAnalysisFast:
    """
    This implementation is similar to PDBAnalysis, but uses a C++ implementation of pdb2res,
    which is significantly faster than the Python implementation.

    Only needed when analysing large numbers of PDB files.
    """

    def __init__(self, pdb2res_executable_path):
        if not os.access(pdb2res_executable_path, os.X_OK):
            raise RuntimeError(f'pdb2res executable not found at {pdb2res_executable_path}.\n'
                               f'Please compile the C++ code and place in the desired location.\n'
                               f'pdb2res.cpp can be found at: https://github.com/scdantu/pycom/blob/main/pycom'
                               f'/analysis/pdb2res.cpp\n'
                               f'Requires -lz flag for zlib (and zlib needs to be installed).\n'
                               f'g++ -std=c++17 pdb2res.cpp -lz -o bin/pdb2res\n')
        self.pdb2res = pdb2res_executable_path

    def get_residue_coordinates(self, pdb_ent_gz_file_path, fmt='pandas') -> pd.DataFrame or np.ndarray:
        assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
        assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'
        assert fmt in ['pandas', 'numpy'], 'Format must be either "pandas" or "numpy"'

        # parse pdb file into list of coordinates (AA resseq x y z)
        proc = subprocess.Popen([self.pdb2res], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, _ = proc.communicate(str.encode(pdb_ent_gz_file_path))

        if fmt == 'numpy':
            out = np.array(list(map(str.split, out.decode('UTF-8').splitlines())))
            out[:, 1] = out[:, 1].astype(int)  # convert resseq to int
            out[:, 2:] = out[:, 2:].astype(float)  # convert x, y, z to float
        elif fmt == 'pandas':
            out = pd.DataFrame(list(map(str.split, out.decode('UTF-8').splitlines())),
                               columns=['AA', 'resseq', 'x', 'y', 'z'])
            out['resseq'] = out['resseq'].astype(int)
            out['x'] = out['x'].astype(float)
            out['y'] = out['y'].astype(float)
            out['z'] = out['z'].astype(float)
        return out

    def get_distance_matrix(self, pdb_ent_gz_file_path) -> np.ndarray:
        """
        Returns a distance matrix from a PDB file
        :param pdb_ent_gz_file_path: path to PDB file
        :return: distance matrix
        """
        assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
        assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'

        coords = self.get_residue_coordinates(pdb_ent_gz_file_path, fmt='numpy')
        return squareform(pdist(coords[:, 2:]))

    def get_contact_map(self, pdb_ent_gz_file_path, cutoff=8) -> np.ndarray:
        """
        Returns a contact map from a PDB file

        Possible values:
        0: no contact
        1: contact
        -1: unknown position (nan)

        :param pdb_ent_gz_file_path: path to PDB file
        :param cutoff: distance cutoff for contact (in Angstroms, default 8Å)
        :return: contact map
        """
        assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
        assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'

        coords = self.get_residue_coordinates(pdb_ent_gz_file_path, fmt='numpy')
        dist_mat = squareform(pdist(coords[:, 2:]))

        contact_matrix = 1 - np.heaviside(dist_mat - cutoff, 0)
        contact_matrix[np.where(np.isnan(contact_matrix))] = -1  # set nan values to -1
        contact_matrix = contact_matrix.astype(int)  # convert to int

        return contact_matrix
