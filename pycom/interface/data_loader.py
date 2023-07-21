import sqlite3
import pandas as pd


class PyComDataLoader:
    """
    A class used to add additional data to the PyCom DataFrame, after using `PyCom.find()`.

    Most methods have a `force_single_entry` parameter.
    If `False`, the data will be added as a list (all matches in PyCom DB).
    If `True`, only the first match will be added (first match in PyCom DB).

    PyComDataLoader can be created using `PyCom.get_data_loader()` or PyComDataLoader(db_path).

    Attributes
    ----------
    db_path : str
        a string path to the SQLite database

    Methods
    -------
    add_diseases(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds diseases data to the DataFrame.
    add_cath_class(df: pd.DataFrame, force_single_entry: bool = True) -> pd.DataFrame:
        Adds CATH classification data to the DataFrame.
    add_enzyme_commission(df: pd.DataFrame, force_single_entry: bool = True) -> pd.DataFrame:
        Adds enzyme commission data to the DataFrame.
    add_pdbs(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds PDBs data to the DataFrame.
    add_organism_name(df: pd.DataFrame) -> pd.DataFrame:
        Adds organism name data to the DataFrame.
    add_organism_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
        Adds organism taxonomy data to the DataFrame.
    add_substrates(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds substrate data to the DataFrame.
    add_cofactors(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds cofactor data to the DataFrame.
    add_biological_processes(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds biological processes data to the DataFrame.
    add_protein_cellular_component(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds protein cellular component data to the DataFrame.
    add_protein_domain(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds protein domain data to the DataFrame.
    add_coding_sequence_diversity(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds coding sequence diversity data to the DataFrame.
    add_developmental_stage(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds developmental stage data to the DataFrame.
    add_ligand(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds ligand data to the DataFrame.
    add_molecular_function(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds molecular function data to the DataFrame.
    add_ptm(df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        Adds post-translational modification data to the DataFrame.
    """

    def __init__(self, db_path: str):
        """
        Parameters
        ----------
        db_path : str
            a string path to the SQLite database
        """
        self.db_path = db_path

    def _execute_query(self, query: str) -> pd.DataFrame:
        """Helper method to execute a query and return a DataFrame."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn)

    def _add_data(self, df: pd.DataFrame, query: str, force_single_entry: bool) -> pd.DataFrame:
        """Helper method to add data to the DataFrame."""
        data_df = self._execute_query(query)
        if not force_single_entry:
            data_df = data_df.groupby('entryId').agg(lambda x: x.tolist()).reset_index()
        merged_df = df.merge(data_df, left_on='uniprot_id', right_on='entryId', how='left')
        return merged_df.drop(columns=['entryId'])

    def add_diseases(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds diseases data to the DataFrame."""
        query = """
            SELECT disease_entry.entryId, disease.diseaseName as disease_name, disease.diseaseId as disease_id
            FROM disease
            JOIN disease_entry ON disease.diseaseId = disease_entry.diseaseId
        """
        return self._add_data(df, query, force_single_entry)

    def add_cath_class(self, df: pd.DataFrame, force_single_entry: bool = True) -> pd.DataFrame:
        """Adds CATH classification data to the DataFrame."""
        query = """
            SELECT
                entryId,
                cath_1 || '.' || cath_2 || '.' || cath_3 || '.' || cath_4 AS cath_class
            FROM cath_class
        """  # cath_1 as cath_super_class
        return self._add_data(df, query, force_single_entry)

    def add_enzyme_commission(self, df: pd.DataFrame, force_single_entry: bool = True) -> pd.DataFrame:
        """Adds enzyme commission data to the DataFrame."""
        query = """
            SELECT
                entryId,
                enzyme_1 || '.' || enzyme_2 || '.' || enzyme_3 || '.' || enzyme_4 AS enzyme_commission
            FROM enzyme_class
        """  # enzyme_1 as enzyme_super_class
        return self._add_data(df, query, force_single_entry)

    def add_pdbs(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds PDBs data to the DataFrame."""
        query = _build_query(["experimentPDB"], ["entryId", "pdbId as pdb_id"])
        return self._add_data(df, query, force_single_entry)

    def add_organism_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds organism name data to the DataFrame."""
        query = _build_query(["entry", "organism"], ["entry.entryId", "organism.nameScientific as organism_name"],
                             ["entry.organismId = organism.organismId"])
        return self._add_data(df, query, force_single_entry=True)

    def add_organism_taxonomy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds organism taxonomy data to the DataFrame."""
        query = _build_query(["entry", "organism"], ["entry.entryId", "organism.taxonomy as taxonomy"],
                             ["entry.organismId = organism.organismId"])
        taxonomy_df = self._execute_query(query)
        taxonomy_df['taxonomy'] = taxonomy_df['taxonomy'].apply(_extract_taxonomy)
        return df.merge(taxonomy_df, left_on='uniprot_id', right_on='entryId', how='left').drop(columns=['entryId'])

    def add_substrates(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds substrate data to the DataFrame."""
        query = _build_query(["substrate"], ["entryId", "substrateName as substrate"])
        return self._add_data(df, query, force_single_entry)

    def add_cofactors(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds cofactor data to the DataFrame."""
        query = """
            SELECT cofactor_entry.entryId, cofactor.cofactorName as cofactor
            FROM cofactor
            JOIN cofactor_entry ON cofactor.cofactorId = cofactor_entry.cofactorId
        """
        return self._add_data(df, query, force_single_entry)

    def add_biological_processes(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds biological processes data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as biological_process"],
                             filter_condition="keywordCategory = 'Biological process'")
        return self._add_data(df, query, force_single_entry)

    def add_protein_cellular_component(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds protein cellular component data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as cellular_component"],
                             filter_condition="keywordCategory = 'Cellular component'")
        return self._add_data(df, query, force_single_entry)

    def add_protein_domain(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds protein domain data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as domain"],
                             filter_condition="keywordCategory = 'Domain'")
        return self._add_data(df, query, force_single_entry)

    def add_coding_sequence_diversity(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds coding sequence diversity data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as coding_sequence_diversity"],
                             filter_condition="keywordCategory = 'Coding sequence diversity'")
        return self._add_data(df, query, force_single_entry)

    def add_developmental_stage(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds developmental stage data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as developmental_stage"],
                             filter_condition="keywordCategory = 'Developmental stage'")
        return self._add_data(df, query, force_single_entry)

    def add_ligand(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds ligand data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as ligand"],
                             filter_condition="keywordCategory = 'Ligand'")
        return self._add_data(df, query, force_single_entry)

    def add_molecular_function(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds molecular function data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as molecular_function"],
                             filter_condition="keywordCategory = 'Molecular function'")
        return self._add_data(df, query, force_single_entry)

    def add_ptm(self, df: pd.DataFrame, force_single_entry: bool = False) -> pd.DataFrame:
        """Adds post-translational modification data to the DataFrame."""
        query = _build_query(["keyword_entry"], ["entryId", "keywordName as ptm"],
                             filter_condition="keywordCategory = 'Post-translational modification'")
        return self._add_data(df, query, force_single_entry)


def _extract_taxonomy(string):
    string = string.strip(':')  # Remove the leading and trailing colons, if any
    taxonomy_list = string.split(':')
    return taxonomy_list


def _build_query(tables: list, columns: list, join_conditions: list = None, filter_condition: str = "") -> str:
    """Builds a SQL query for given tables, columns, join conditions and filter condition."""
    query = f"SELECT {', '.join(columns)} FROM {tables[0]}"
    if join_conditions:
        for table, join_condition in zip(tables[1:], join_conditions):
            query += f" JOIN {table} ON {join_condition}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    return query
