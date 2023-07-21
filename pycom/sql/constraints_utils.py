
organism_constraint = lambda _: '''
    entry.organismId IN (
        SELECT  organism.organismId
        FROM    organism
        WHERE   organism.taxonomyFull LIKE ?
    )'''


disease_id_constraint = lambda _: '''
    entry.entryId IN (
        SELECT  disease_entry.entryId
        FROM    disease_entry
        WHERE   (disease_entry.diseaseId = ?)
    )'''


disease_constraint = lambda _: '''
    entry.entryId IN (
        SELECT  disease_entry.entryId
        FROM    disease_entry
        JOIN    disease ON disease_entry.diseaseId = disease.diseaseId
        WHERE   lower(disease.diseaseName) LIKE lower(?)
    )'''


has_disease_constraint = lambda has_disease: f'''
    entry.entryId {'NOT' if not has_disease else ''} IN (
        SELECT  disease_entry.entryId
        FROM    disease_entry
        WHERE ? OR TRUE
    )'''

cofactor_id_constraint = lambda _: '''
    entry.entryId IN (
        SELECT  cofactor_entry.entryId
        FROM    cofactor_entry
        WHERE   (cofactor_entry.cofactorId = ?)
    )'''


cofactor_constraint = lambda _: '''
    entry.entryId IN (
        SELECT  cofactor_entry.entryId
        FROM    cofactor_entry
        JOIN    cofactor ON cofactor_entry.cofactorId = cofactor.cofactorId
        WHERE   lower(cofactor.cofactorName) LIKE lower(?)
    )'''


has_keyword_constraint = lambda _, keyword_category: f'''
    entry.entryId IN (
        SELECT keyword_entry.entryId
        FROM keyword_entry
        WHERE keyword_entry.keywordCategory = '{keyword_category}'
    )'''

keyword_constraint = lambda _, keyword_category: f'''
    entry.entryId IN (
        SELECT keyword_entry.entryId
        FROM keyword_entry
        WHERE lower(keyword_entry.keywordName) LIKE lower(?)
        AND keyword_entry.keywordCategory = '{keyword_category}'
    )'''

_CATH_ENZYME_ERROR = 'CATH/Enzyme class must be in format: 1.2.3.4 or 1.2.*.*'


def class_param(arg):
    """Converts a CATH/Enzyme class param into a list of integers

    Validates the param for correctness and returns a list of integers

    Args:
        arg (str): CATH/Enzyme class param in format (1.2.3.4 or 1.2.*.*))"""
    split = arg.split('.')

    assert 1 <= len(split) <= 4, _CATH_ENZYME_ERROR  # must be 1-4
    assert len(split) == 4 or split[-1] == '*', _CATH_ENZYME_ERROR  # last must be * if not 4
    assert all([x.isdigit() for x in split if x != '*']), _CATH_ENZYME_ERROR  # all must be digits

    split = [int(x) if x != '*' else None for x in split]

    correct_order = not any(x is None and y is not None for x, y in zip(split, split[1:]))
    assert correct_order, _CATH_ENZYME_ERROR  # cannot have wildcards in the middle

    split = [x for x in split if x is not None]  # remove wildcards

    return split


def class_constraint(arg, entry_type):
    """Generates a CATH/Enzyme class SQL constraint
    The query is generated based on the number of arguments in the param
    between 1 and 4.

    The entry_type is either 'cath' or 'enzyme' and should be specified
    through the functools.partial function.
    """
    assert entry_type in ['cath', 'enzyme'], 'Entry type must be either cath or enzyme'
    assert type(arg) == list, 'Param should be pre-processed by _class_param'

    if len(arg) == 0:
        return '0=0'

    default_cath_query = f'''entry.entryId IN (
        SELECT  {entry_type}_class.entryId
        FROM    {entry_type}_class
        WHERE   (%s)
    )'''

    default_cath_selector = f'{entry_type}_class.{entry_type}_%s = ?'

    cath_query = [(default_cath_selector % i) for i in range(1, len(arg) + 1)]
    cath_query = ' AND '.join(cath_query)

    cath_query = default_cath_query % cath_query

    return cath_query


def to_str(arg, entry, starts_with=None):
    """Returns a string, throws an error if starts_with is specified and the string does not start with it"""
    if starts_with is not None:
        assert arg.startswith(starts_with), f'{entry} must follow format: {starts_with}00000'

    return str(arg)


def to_int(arg, entry):
    """Converts a string to an integer if possible"""
    try:
        return int(arg)
    except ValueError:
        assert False, f'{entry} must be an integer'


def to_float(arg, entry):
    """Converts a string to a float if possible"""
    try:
        return float(arg)
    except ValueError:
        assert False, f'{entry} must be a float'


_BOOL_TRUE_VALUES = {'true', 't', 'yes', 'y', '1'}
_BOOL_FALSE_VALUES = {'false', 'f', 'no', 'n', '0'}
_BOOL_VALUES = _BOOL_TRUE_VALUES | _BOOL_FALSE_VALUES


def to_bool(arg, entry):
    """Converts a string to a boolean if possible"""
    if type(arg) == bool:
        return arg

    arg = arg.lower()

    assert arg in _BOOL_VALUES, f'{entry} must be a boolean [true/false, yes/no, 0/1]'
    return arg in _BOOL_TRUE_VALUES
