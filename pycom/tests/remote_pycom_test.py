import pandas as pd

from pycom import PyCom, ProteinParams

pyc = PyCom(remote=True)

"""
    ID = 'uniprot_id'
    SEQUENCE = 'sequence'

    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'

    MIN_HELIX = 'min_helix'
    MAX_HELIX = 'max_helix'
    MIN_TURN = 'min_turn'
    MAX_TURN = 'max_turn'
    MIN_STRAND = 'min_strand'
    MAX_STRAND = 'max_strand'

    ORGANISM_ID = 'organism_id'
    ORGANISM = 'organism'

    CATH = 'cath'
    ENZYME = 'enzyme'

    HAS_SUBSTRATE = 'has_substrate'
    HAS_PTM = 'has_ptm'

    HAS_PDB = 'has_pdb'

    DISEASE = 'disease'
    DISEASE_ID = 'disease_id'
    HAS_DISEASE = 'has_disease'

    COFACTOR = 'cofactor'
    COFACTOR_ID = 'cofactor_id'"""


def is_non_empty_dataframe(df):
    assert df is not None
    assert type(df) == pd.DataFrame
    assert len(df) > 0


def test_find_valid():
    is_non_empty_dataframe(pyc.find())
    is_non_empty_dataframe(pyc.find({ProteinParams.ID: 'P01111'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.SEQUENCE: 'MTTDD'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MIN_LENGTH: 100}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MAX_LENGTH: 100}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MIN_HELIX: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MAX_HELIX: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MIN_TURN: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MAX_TURN: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MIN_STRAND: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.MAX_STRAND: 0.5}))
    is_non_empty_dataframe(pyc.find({ProteinParams.ORGANISM_ID: 9606}))
    is_non_empty_dataframe(pyc.find({ProteinParams.ORGANISM: 'Homo sapiens'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.CATH: '1.*.*.*'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.ENZYME: '1.*'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.HAS_SUBSTRATE: True}))
    is_non_empty_dataframe(pyc.find({ProteinParams.HAS_PTM: True}))
    is_non_empty_dataframe(pyc.find({ProteinParams.HAS_PDB: True}))
    is_non_empty_dataframe(pyc.find({ProteinParams.DISEASE: 'epilepsy'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.DISEASE_ID: 'DI-00821'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.HAS_DISEASE: True}))
    is_non_empty_dataframe(pyc.find({ProteinParams.COFACTOR: 'Zn(2+)'}))
    is_non_empty_dataframe(pyc.find({ProteinParams.COFACTOR_ID: 'CHEBI:29105'}))
