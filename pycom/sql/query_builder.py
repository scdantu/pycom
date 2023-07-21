from pycom.sql.query_constraints import constraints_template as template

_BASE_QUERY = '''
SELECT
    {columns}
FROM
    entry
WHERE (
    {constraints}
)
'''

_queried_columns_map = {
    'entryId': 'uniprot_id',
    'neff': 'neff',
    'sequenceLength': 'sequence_length',
    'sequence': 'sequence',
    'organismId': 'organism_id',
    'structHelix': 'helix_frac',
    'structTurn': 'turn_frac',
    'structStrand': 'strand_frac',
    'hasPTM': 'has_ptm',
    'hasPDB': 'has_pdb',
    'hasSubstrate': 'has_substrate',
}


class PyComSQLQueryBuilder:
    """PyCom SQL Query Builder
    
    This class is used to build a SQL query based on the constraints
    for the protein database."""

    _db_columns = list(_queried_columns_map.keys())
    columns = [x for x in _queried_columns_map.values()]

    def __init__(self):
        # self.columns = ['entry.entryId', 'entry.sequence', 'entry.sequenceLength', 'entry.organismId']
        self.columns = PyComSQLQueryBuilder._db_columns

        self.constraint_store = []
        self.param_store = []

        self.query = None
        self.params = None

        # self.strip_query = False  # Strip whitespace from the query, for debugging purposes

    def add_column(self, column):
        raise NotImplementedError

    def add_constraint(self, constraint, param):
        """Add a constraint to the query
        
        The constraint name is a predefined string """
        self.constraint_store.append(constraint)
        self.param_store.extend(param) if isinstance(param, list) else self.param_store.append(param)

    def add_constraints(self, constraints: dict):
        """Add multiple constraints to the query

        The constraints are defined as a dictionary with the constraint name as the key
        and the constraint parameters as the value

        Example:
            add_constraints({ProteinParams.MIN_LENGTH: 100, ProteinParams.CATH: '1.20.*.*'})
        """
        for constraint, param in constraints.items():
            self.add_constraint(constraint, param)

    def build(self):
        """Build the query"""
        assert len(self.constraint_store) == len(self.param_store), 'Number of constraints and parameters must be equal'
        query_input = zip(self.constraint_store, self.param_store)

        selector_parts = []
        params = []

        for constraint, param in query_input:
            assert constraint in template, f'Selector {constraint} is not defined'
            param = template[constraint]['param'](param)  # Apply the param function to the param
            constraint_query = template[constraint]['constraint'](param)

            selector_parts.append(constraint_query)
            params.extend(param) if isinstance(param, list) else params.append(param)

        columns = ', '.join(self.columns)
        selector = ' AND '.join(selector_parts if selector_parts else ['1=1'])

        self.query = _BASE_QUERY.format(columns=columns, constraints=selector)
        # if self.strip_query:
        #     self.query = strip_whitespace(self.query)

        self.params = params

        return self.query, self.params


__all__ = ['PyComSQLQueryBuilder']
