"""
Author: Philipp Bibik (cemiu)

Simple PDB parser. residues_from_pdb() take in a PDB file in .ent.gz format and returns a list of residues
along with their coordinates.

The format is [AA, resseq, x, y, z]
resseq always starts at 0. Missing residues are represented by a dot (.)

Example output:
[['.', 0, 'nan', 'nan', 'nan'],
 ['.', 1, 'nan', 'nan', 'nan'],
 ['A', 2, 3.106, -5.132, 0.993],
 ...
]
"""

import os
import gzip

import numpy as np

_AA_LOOKUP = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLN': 'Q', 'GLU': 'E', 'GLY': 'G',
    'HIS': 'H', 'HIP': 'H', 'HIE': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F',
    'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TYR': 'Y',
    'TRP': 'W', 'VAL': 'V',
    # 'SEC': 'U', 'PYL': 'O', 'UNK': '.',
}


def _read_pdb_gz(pdb_ent_gz_file_path):
    assert os.path.exists(pdb_ent_gz_file_path), f'File not found: {pdb_ent_gz_file_path}'
    assert pdb_ent_gz_file_path.endswith('.ent.gz'), 'File must be a .ent.gz file'

    with gzip.open(pdb_ent_gz_file_path, 'rb') as f:
        file_content = f.read().decode('UTF-8')

    return file_content.splitlines()


def residues_from_pdb(pdb_ent_gz_file_path) -> np.ndarray:
    """
    Returns a list of residues from a PDB file. PDB file must be in .ent.gz format. (compressed)
    """
    pdb_file = _read_pdb_gz(pdb_ent_gz_file_path)
    last_resseq = 0

    out = []

    for l in pdb_file:
        statement = l[:4]
        if statement == 'TER ': break
        if statement != 'ATOM': continue

        atom = l[13:15]
        if atom != 'CA' and atom != 'CB': continue  # only C_a and C_b atoms
        aa = l[17:20]
        if atom == 'CA' and aa != 'GLY': continue  # only C_a atoms for glycine
        if aa not in _AA_LOOKUP: continue  # skip unknown amino acids

        aa = _AA_LOOKUP[aa]
        resseq = int(l[23:27])

        x = l[30:38].lstrip()
        y = l[38:46].lstrip()
        z = l[46:54].lstrip()

        for i in range(last_resseq + 1, resseq):
            out.append(['.', i-1, 'nan', 'nan', 'nan'])

        last_resseq = resseq

        out.append([aa, resseq-1, x, y, z])

    out = np.array(out, dtype=object)
    out[:, 1] = out[:, 1].astype(int)  # convert resseq to int
    out[:, 2:] = out[:, 2:].astype(float)  # convert x, y, z to float

    return out
