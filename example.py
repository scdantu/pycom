from pycom import PyCom, ProteinParams

pyc = PyCom(db_path='~/docs/pycom.db', mat_path='~/docs/pycom.mat')


# Query the database by passing a dictionary of conditions
entries_a = pyc.find({
    ProteinParams.ENZYME: '3.*.*.*',
    ProteinParams.DISEASE: 'cancer',  # string search, case-insensitive
})


# Alternatively, query the database by passing keyword arguments
entries_b = pyc.find(
    cofactor='FAD',  # string search, case-insensitive
    has_ptm=True,
    has_disease=True,
)

"""
Supported parameters:
            uniprot_id: Optional[str] = None,
            sequence: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            min_helix: Optional[float] = None,
            max_helix: Optional[float] = None,
            min_turn: Optional[float] = None,
            max_turn: Optional[float] = None,
            min_strand: Optional[float] = None,
            max_strand: Optional[float] = None,
            organism: Optional[str] = None,
            cath: Optional[str] = None,
            enzyme: Optional[str] = None,
            has_substrate: Optional[bool] = None,
            has_ptm: Optional[bool] = None,
            has_pdb: Optional[bool] = None,
            disease: Optional[str] = None,
            disease_id: Optional[str] = None,
            has_disease: Optional[bool] = None,
            cofactor: Optional[str] = None,
            cofactor_id: Optional[str] = None,
"""

# param list with descriptions
"""
Supported parameters:
    uniprot_id: The UniProt ID of the protein.
    sequence: The amino acid sequence of protein to search for. (full match)
    min_length: The minimum length of the protein.
    max_length: The maximum length of the protein.
    min_helix: The minimum percentage of helical secondary structure.
    max_helix: The maximum percentage of helical secondary structure.
    min_turn: The minimum percentage of turn secondary structure.
    max_turn: The maximum percentage of turn secondary structure.
    min_strand: The minimum percentage of strand secondary structure.
    max_strand: The maximum percentage of strand secondary structure.
    organism: The organism of the protein.
    organism_id: The ID of the organism.
    cath: The CATH classification of the protein.
    enzyme: The EC number of the protein.
    has_substrate: Whether the protein has a substrate.
    has_ptm: Whether the protein has a post-translational modification.
    has_pdb: Whether the protein has a PDB structure.
    disease: The name of the disease.
    disease_id: The ID of the disease.
    has_disease: Whether the protein has a disease.
    cofactor: The name of the cofactor.
    cofactor_id: The ID of the cofactor.
"""


# Get the lists of available cofactors and diseases
cofactors = pyc.get_cofactor_list()
diseases = pyc.get_disease_list()

print('The cofactors are:')
print(cofactors)


# Make a large query, then paginate the results:
entries = pyc.find(min_length=5, max_length=20)
print(f'Found {len(entries)} entries with length <= 20')

page = pyc.paginate(entries, page=1)  # get first n entries (default 100)
print(f'Found {len(page)} entries on page 1')


# Load the coevolution matrices for the results:
pyc.load_matrices(page)

print('Coevolution matrix for the first entry:')
print(page.iloc[0].matrix)
