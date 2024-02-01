Documentation
=============

.. warning::

   Documentation sites are **Work in progress**
   


This is the documentation of the three core classes that users will be interacting with:
   #. :class:`PyCoM`
   #. :class:`ProteinParams`
   #. :class:`CoMAnalysis`

.. automodule:: pycom.interface.PyCom
    :members:

Quick Summary
-------------

.. currentmodule:: pycom.interface.PyCom
.. autosummary::
   pycom.interface.PyCom.find
   pycom.interface.PyCom.load_matrices
   pycom.interface.PyCom.paginate
   pycom.interface.PyCom.get_data_loader
   pycom.interface.PyCom.get_biological_process_list
   pycom.interface.PyCom.get_cellular_component_list
   pycom.interface.PyCom.get_cofactor_list
   pycom.interface.PyCom.get_disease_list
   pycom.interface.PyCom.get_developmental_stage_list
   pycom.interface.PyCom.get_domain_list
   pycom.interface.PyCom.get_ligand_list
   pycom.interface.PyCom.get_molecular_function_list
   pycom.interface.PyCom.get_organism_list
   pycom.interface.PyCom.get_ptm_list
   
.. currentmodule:: pycom.selector.ProteinParams
.. autosummary::
   pycom.selector.ProteinParams.descriptions
   
.. currentmodule:: pycom.analysis.CoMAnalysis
.. autosummary::
   pycom.analysis.CoMAnalysis.add_contact_predictions
   pycom.analysis.CoMAnalysis.scaled_matrix_to_contact_predictions
   pycom.analysis.CoMAnalysis.get_top_contacts_from_coevolution
   pycom.analysis.CoMAnalysis.get_residue_frequencies
   pycom.analysis.CoMAnalysis.calculate_scaled_coevolution_matrix
   pycom.analysis.CoMAnalysis.get_top_scoring_residues
   pycom.analysis.CoMAnalysis.scale_and_normalise_coevolution_matrices
   pycom.analysis.CoMAnalysis.save_top_scoring_residue_pairs

 
Class Documentation
-------------------

.. toctree::
   :maxdepth: 2

   PyCom class <api_pycom>
   Matrix analysis <api_matrix_analysis>
   Query words Selection  <api_params>