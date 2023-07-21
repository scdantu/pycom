from functools import partial

from pycom.selector.selector_params import ProteinParams
from pycom.sql.constraints_utils import *

"""This class defines the constraints for the query builder

It both defines the constraint to query mapping and validation
of the parameters.
"""

_constraints_simple = {
    ProteinParams.ID: {  # uniprot id
        'constraint': lambda _: 'entry.entryId = ?',
        'param': lambda x: str(x),
        # 'validate': lambda x: bool(re.match(r'^[\d\w]{6,10}$', x))
    },
    ProteinParams.SEQUENCE: {  # sequence
        'constraint': lambda _: 'entry.sequence = ?',
        'param': lambda x: str(x).upper(),
        # 'validate': lambda x: bool(re.match(r'^[A-Z]+$', x))
    },
    ProteinParams.MIN_LENGTH: {  # minimum sequence length
        'constraint': lambda _: 'entry.sequenceLength >= ?',
        'param': partial(to_int, entry=ProteinParams.MIN_LENGTH),
    },
    ProteinParams.MAX_LENGTH: {  # maximum sequence length
        'constraint': lambda _: 'entry.sequenceLength <= ?',
        'param': partial(to_int, entry=ProteinParams.MAX_LENGTH),
    },
}

_constraints_struct = {
    ProteinParams.MIN_HELIX: {  # minimum fraction of protein in helix
        'constraint': lambda _: 'entry.structhelix >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_HELIX),
    },
    ProteinParams.MAX_HELIX: {  # maximum fraction of protein in helix
        'constraint': lambda _: 'entry.structhelix <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_HELIX),
    },
    ProteinParams.MIN_TURN: {  # minimum fraction of protein in turn
        'constraint': lambda _: 'entry.structturn >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_TURN),
    },
    ProteinParams.MAX_TURN: {  # maximum fraction of protein in turn
        'constraint': lambda _: 'entry.structturn <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_TURN),
    },
    ProteinParams.MIN_STRAND: {  # minimum fraction of protein in strand
        'constraint': lambda _: 'entry.structstrand >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_STRAND),
    },
    ProteinParams.MAX_STRAND: {  # maximum fraction of protein in strand
        'constraint': lambda _: 'entry.structstrand <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_STRAND),
    },
    ProteinParams.HAS_PTM: {  # has post-translational modification
        'constraint': lambda _: 'entry.hasPTM = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_PTM)
    },
    ProteinParams.HAS_SUBSTRATE: {  # has substrate
        'constraint': lambda _: 'entry.hasSubstrate = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_SUBSTRATE)
    },
    ProteinParams.HAS_PDB: {  # has PDB structure
        'constraint': lambda _: 'entry.hasPDB = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_PDB)
    },
    ProteinParams.ORGANISM_ID: {  # organism id (NCBI taxonomy id)
        'constraint': lambda _: 'entry.organismId = ?',
        'param': partial(to_int, entry=ProteinParams.ORGANISM_ID),
    },
}


_constraints_special = {
    ProteinParams.ORGANISM: {  # protein name
        'constraint': organism_constraint,
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.CATH: {  # CATH class
        'constraint': partial(class_constraint, entry_type='cath'),
        'param': lambda x: class_param(x),
    },
    ProteinParams.ENZYME: {  # Enzyme class
        'constraint': partial(class_constraint, entry_type='enzyme'),
        'param': lambda x: class_param(x),
    },
    ProteinParams.DISEASE: {  # disease name
        'constraint': disease_constraint,
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.DISEASE_ID: {  # disease id
        'constraint': disease_id_constraint,
        'param': lambda x: partial(to_str, entry=ProteinParams.DISEASE_ID, starts_with='DI-')(x),
    },
    ProteinParams.HAS_DISEASE: {  # has disease
        'constraint': has_disease_constraint,
        'param': partial(to_bool, entry=ProteinParams.HAS_DISEASE)
    },
    ProteinParams.COFACTOR: {  # cofactor name
        'constraint': cofactor_constraint,
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.COFACTOR_ID: {  # cofactor id
        'constraint': cofactor_id_constraint,
        'param': lambda x: partial(to_str, entry=ProteinParams.COFACTOR_ID, starts_with='CHEBI:')(x),
    },
}

_constraints_keyword_based = {
    ProteinParams.BIOLOGICAL_PROCESS: {  # biological process
        'constraint': partial(keyword_constraint, keyword_category='Biological process'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.CELLULAR_COMPONENT: {  # cellular component
        'constraint': partial(keyword_constraint, keyword_category='Cellular component'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.DEVELOPMENTAL_STAGE: {  # developmental stage
        'constraint': partial(keyword_constraint, keyword_category='Developmental stage'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.DOMAIN: {  # domain
        'constraint': partial(keyword_constraint, keyword_category='Domain'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.LIGAND: {  # ligand
        'constraint': partial(keyword_constraint, keyword_category='Ligand'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.MOLECULAR_FUNCTION: {  # molecular function
        'constraint': partial(keyword_constraint, keyword_category='Molecular function'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    },
    ProteinParams.PTM: {  # post-translational modification
        'constraint': partial(keyword_constraint, keyword_category='PTM'),
        'param': lambda x: f'%{x}%'.lower(),  # add wildcards
    }
}

# merge all constraints into the final list
constraints_template = {**_constraints_simple, **_constraints_struct, **_constraints_special,
                        **_constraints_keyword_based}

# check that all constraints are implemented
assert set(constraints_template.keys()) == set(ProteinParams), 'Not all query constraints are implemented'
