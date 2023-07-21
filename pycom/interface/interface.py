from abc import abstractmethod
from typing import Optional

import pandas as pd

from pycom.interface.data_loader import PyComDataLoader
from pycom.selector import MatrixFormat

# supress SettingWithCopyWarning from pandas
pd.options.mode.chained_assignment = None  # default='warn'


class PyCom(object):

    def __new__(
            cls,
            db_path: Optional[str] = None,
            mat_path: Optional[str] = None,
            remote: bool = False,
    ) -> 'PyCom':
        """
        PyCom is a class that functions as the main interface for querying the PyCom database.


        Can be used remotely, by setting remote=True
        Can be used locally, by setting db_path to `pycom.db` and (optionally) mat_path to `pycom.mat`

        The main mode of interaction with PyCom is through the `find` function, which returns a pandas DataFrame.

        There are slight differences between the remote and local variants of PyCom:
            Remote:
                - The results of `find` are paginated, and find takes the `page` and `per_page` parameters.
                - Matrices are loaded by setting the `matrix` parameter to True
                - `paginate` and `load_matrices` are not implemented
            Local:
                - `find` returns all results in a single DataFrame.
                - Results can be paginated using `paginate(df, page, per_page)`
                - Matrices are loaded using `load_matrices(df)`
                - Local PyCom requires the `db_path` and `mat_path` parameters to be set to the location of the \
                  `pycom.db` and `pycom.mat` files respectively. These files can be downloaded from \
                  https://pycom.brunel.ac.uk/downloads/

        Usage:
            >>> from pycom import PyCom
            >>> # For local use:
            >>> pycom = PyCom(db_path='~/docs/pycom.db', mat_path='~/docs/pycom.mat')
            >>> # Or for remote use:
            >>> pycom_remote = PyCom(remote=True)
            Find all proteins associated with cancer:
            >>> df = pycom.find(disease='cancer')
            Get the first page of results, 100 results per page:
            >>> page = pycom.paginate(df, page=1)
            Load the coevolution matrices for the first page of results:
            >>> pycom.load_matrices(page)
            >>> print(page.iloc[0].matrix)
            Get a list of all cofactors / diseases / organism in the database
            >>> cofactors = pycom.get_cofactor_list()
            >>> diseases = pycom.get_disease_list()
            >>> organisms = pycom.get_organism_list()

        Parameters:
            db_path: Path to the PyCom database (pycom.db)
            mat_path: Path to the coevolution matrix file (pycom.mat)
            remote: Whether to use the remote API. Defaults to False.
        """
        if cls is PyCom:
            if remote:
                assert db_path is None, 'Cannot specify db_path when using remote API, remove param or set remote=False'
                assert mat_path is None, 'Cannot specify mat_path when using remote API, remove param or set ' \
                                         'remote=False'

                from pycom.interface.interface_remote import PyComRemote
                return PyComRemote()
            else:
                assert db_path is not None, 'Must specify db_path when using local API, set remote=True or specify ' \
                                            'the location of `pycom.db` in db_path, which can be downloaded from ' \
                                            'https://pycom.brunel.ac.uk/downloads/'

                from pycom.interface.interface_local import PyComLocal
                return PyComLocal(db_path=db_path, mat_path=mat_path)
        else:
            return super(PyCom, cls).__new__(cls)

    @abstractmethod
    def find(
            self,
            constraint_dict: Optional[dict] = None,
            /,  # force positional arguments
            *,  # force keyword arguments
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
            organism_id: Optional[str] = None,
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
            biological_process: Optional[str] = None,
            cellular_component: Optional[str] = None,
            developmental_stage: Optional[str] = None,
            domain: Optional[str] = None,
            ligand: Optional[str] = None,
            molecular_function: Optional[str] = None,
            ptm: Optional[str] = None,

            page: Optional[int] = None,
            per_page: Optional[int] = None,
            matrix: Optional[bool] = None,
            matrix_format: Optional[MatrixFormat] = None,
    ) -> pd.DataFrame:
        """
        Find proteins in the database that match the given criteria.

        This function searches the database for proteins that match the given criteria. The criteria can be specified
        using any combination of the parameters listed below.

        Use either constraint_dict or the individual parameters, not both.

        Usage:
            >>> from pycom import PyCom, ProteinParams
            >>> pyc = PyCom(db_path='/path/on/disk/pycom.db')
            load all proteins associated with cancer:
            >>> pyc = pyc.find(disease='cancer')
            or (equivalent):
            >>> pyc = pyc.find({ProteinParams.DISEASE: 'cancer'})

        :param constraint_dict: A dictionary of constraints to apply to the search {ProteinParams: value}.
        :param uniprot_id: The UniProt ID of the protein.
        :param sequence: The amino acid sequence of protein to search for. (full match)
        :param min_length: Minimum number of residues.
        :param max_length: Maximum number of residues.
        :param min_helix: Min percentage of helical structure in the protein.
        :param max_helix: Max percentage of helical structure in the protein.
        :param min_turn: Min percentage of turn structure in the protein.
        :param max_turn: Max percentage of turn structure in the protein.
        :param min_strand: Min percentage of beta strand structure in the protein.
        :param max_strand: Max percentage of beta strand structure in the protein.
        :param organism_id: NCBI Taxonomy ID of the genus / species of the protein. (get_organism_list())
        :param organism: Taxonomic name of the genus / species of the protein. (case-insensitive, get_organism_list())
        :param cath: CATH classification of the protein ( '3.40.50.360' or '3.40.*.*' or '3.*' ).
        :param enzyme: Enzyme Commission number of the protein. ( '3.40.50.360' or '3.40.*.*' or '3.*' ).
        :param has_substrate: Whether the protein has a known substrate. (True/False)
        :param has_ptm: Whether the protein has a known post-translational modification. (True/False)
        :param has_pdb: Whether the protein has a known PDB structure. (True/False)
        :param disease: The disease associated with the protein. (name of disease, case-insensitive [e.g 'cancer'])
        :param disease_id: The ID of the disease associated with the protein. ('DI-00001', get_disease_list()
        :param has_disease: Whether the protein is associated with a disease. (True/False)
        :param cofactor: The cofactor associated with the protein. (name of cofactor, case-insensitive [e.g 'Zn(2+)'])
        :param cofactor_id: The ID of the cofactor associated with the protein. ('CHEBI:00001', get_cofactor_list())
        :param biological_process: The biological process associated with the protein.
               (name of process, case-insensitive, get_biological_process_list())
        :param cellular_component: The cellular component associated with the protein.
               (name of component, case-insensitive, get_cellular_component_list())
        :param developmental_stage: The developmental stage associated with the protein.
               (name of stage, case-insensitive, get_developmental_stage_list())
        :param domain: The domain associated with the protein.
               (name of domain, case-insensitive, get_domain_list())
        :param ligand: The ligand associated with the protein.
               (name of ligand, case-insensitive, get_ligand_list())
        :param molecular_function: The molecular function associated with the protein.
               (name of function, case-insensitive, get_molecular_function_list())
        :param ptm: The post-translational modification associated with the protein.
               (name of ptm, case-insensitive, get_ptm_list())

        (specific to PyComRemote)
        :param page: The page number of results to return. (1-i)
        :param per_page: The number of results per page. (1-100)
        :param matrix: Whether to return the coevolution matrix with the results.
        :param matrix_format: The format of the coevolution matrix. (MatrixFormat.NUMPY or MatrixFormat.PANDAS)

        :return: A pandas DataFrame containing the proteins that match the given criteria.
        raise NotImplementedError('Implementation at bottom of file')
        """
        pass

    @abstractmethod
    def load_matrices(
            self,
            df: pd.DataFrame,
            max_load: int = 1000,
            mat_format: MatrixFormat = MatrixFormat.NUMPY
    ) -> pd.DataFrame:
        """
        Only for PyComLocal:
        Load the coevolution matrices into memory

        Takes a DataFrame from PyCom.find() or PyCom.paginate() and loads the coevolution matrices into memory,
        into the 'matrix' column.

        Requires the coevolution matrix file (pycom.mat) to be downloaded from https://pycom.brunel.ac.uk/downloads/

        By default, this function will only load the first 1000 matrices. This can be changed by setting max_load.
        """
        pass

    @staticmethod
    @abstractmethod
    def paginate(df: pd.DataFrame, page: int, per_page: int = 100) -> pd.DataFrame:
        """
        Only for PyComLocal:
        Paginate a DataFrame that is generated by PyCom.find().
        This is useful for using PyCom.load_matrices() on a large DataFrame.

        First page is 1.
        By default, 100 results are returned per page; this can be changed by setting per_page.

        :param df: The DataFrame to paginate
        :param page: The page number to return
        :param per_page: The number of results to return per page
        """
        pass

    @abstractmethod
    def get_data_loader(self) -> PyComDataLoader:
        """
        Returns the PyComDataLoader object that is used to load additional data into the dataframe.

        Not implemented in PyComRemote.

        :return: PyComDataLoader
        """
        pass

    @abstractmethod
    def get_disease_list(self) -> pd.DataFrame:
        """Retrieves the list of all diseases in the database."""
        pass

    @abstractmethod
    def get_cofactor_list(self) -> pd.DataFrame:
        """Retrieves the list of all cofactors in the database."""
        pass

    @abstractmethod
    def get_organism_list(self) -> pd.DataFrame:
        """Retrieves the list of all organisms in the database."""
        pass

    @abstractmethod
    def get_biological_process_list(self):
        """Retrieves the list of all biological processes in the database."""
        pass

    @abstractmethod
    def get_cellular_component_list(self):
        """Retrieves the list of all cellular components in the database."""
        pass

    @abstractmethod
    def get_developmental_stage_list(self):
        """Retrieves the list of all developmental stages in the database."""
        pass

    @abstractmethod
    def get_domain_list(self):
        """Retrieves the list of all domains in the database."""
        pass

    @abstractmethod
    def get_ligand_list(self):
        """Retrieves the list of all ligands in the database."""
        pass

    @abstractmethod
    def get_molecular_function_list(self):
        """Retrieves the list of all molecular functions in the database."""
        pass

    @abstractmethod
    def get_ptm_list(self):
        """Retrieves the list of all post-translational modifications in the database."""
        pass
