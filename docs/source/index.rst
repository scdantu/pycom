.. PyCoM documentation master file


PyCoM - Protein Coevolution Database (API & Python Library)
==============================================================================

   PyCoM is a Python API and libray to the Coevolution Matrix database (PyCoMdb), containing *457,622* annotated proteins, from `UniProtKB/Swiss-Prot <https://www.expasy.org/resources/uniprotkb-swiss-prot>`_  with their coevolution matrices calculated using `HH-suite3 <https://github.com/soedinglab/hh-suite>`_ and `CCMpred <https://github.com/soedinglab/CCMpred>`_.

   We provide you simple tools written in Python to `query <tutorials.html>`_, `extract <tutorials.html>`_ and `visualise <tutorials.html>`_ data for your choice of protein(s).

   The code is open source and available on `GitHub <https://github.com/scdantu/pycom>`_.

   Installing is as simple as running:

   .. code-block:: bash

       pip3 install git+https://github.com/scdantu/pycom

   And you are ready to run the code!

   .. code-block:: py3

    from pycom import PyCom, CoMAnalysis
    import matplotlib.pyplot as plt

    pyc = PyCom(remote=True)
    proteins = pyc.find(
        min_length=200,
        max_length=210,
        disease='cancer',
        has_substrate=True,
        page=1,
        matrix=True
    )

    CoMAnalysis().add_contact_predictions(proteins)
    plt.axis('off')
    plt.title(f'Contact Map for uniprot_id={proteins.uniprot_id[0]}')
    plt.imshow(proteins.contact_matrix[0])

    print(proteins.iloc[0])


.. list-table:: Output:

   * - .. image:: _static/example_run.png
          :alt: Output of the code above

     - .. code-block::

          uniprot_id                    P62070
          neff                          12.754
          sequence_length                  204
          sequence           MAAAGWRDGSGQEK...
          organism_id                     9606
          helix_frac                   0.29902
          turn_frac                   0.019608
          strand_frac                 0.220588
          has_ptm                            1
          has_pdb                            1
          has_substrate                      1
          matrix             [[0.0, 0.268, ...
          contact_matrix     [[0.0, 0.0,   ...
          Name: 0, dtype: object

Features
--------

PyCoM breaks down into:

- **PyCoMdb**: A database of coevolution matrices for proteins from `UniProtKB/Swiss-Prot <https://www.expasy.org/resources/uniprotkb-swiss-prot>`_, with *457,622* annotated proteins.

  - Available at: https://pycom.brunel.ac.uk/downloads/
- **PyCoM Python Library**: A Python API to query, extract and visualise coevolution matrices from PyCoMdb

  - Available at: `https://github.com/scdantu/pycom <https://github.com/scdantu/pycom>`_
  - Guides: `Getting Started <gettingstarted.html>`_
  - This library supports:

    - **Querying** - Search for proteins based on various criteria
    - **Coevolution Matrices** - Load coevolution matrices for proteins
    - **Analysis** - A set of tools for performing analysis on coevolution matrices `Analysis Tutorial <tutorials/01_Workflow.html>`_
    - **PDB&AlphaFold PDB parsing/analysis** - A set of tools for parsing and analysing PDB files. `PDB Tutorial <tutorials/05_Contact_Map_and_PDB.html>`_

- **PyCoM API**: A RESTful API to query, extract and visualise coevolution matrices from PyCoMdb

  - Available at: https://pycom.brunel.ac.uk/api/
  - `Guide to the API <tutorials/00_WebAPI.html>`_

- **Alignment File Repository**: A repository of 370,000+ alignment files, available for download

  - Available at: https://pycom.brunel.ac.uk/alignments/
  - `Tutorial: Using the Alignment Repository <tutorials/03_Alignment_analysis.html>`_



If you are more interested in alignment data (rather than Protein Residue-Residue Contacts), we also provide these at: https://pycom.brunel.ac.uk/alignments/

The parameters for generating the alignment using `HH-suite3 <https://github.com/soedinglab/hh-suite>`_  can be found in `Kamisetty et al. 2013 <https://www.pnas.org/doi/10.1073/pnas.1314045110>`_.



How to Cite
-----------

   Bibik. P, Alibai. S, Pandini. A, Dantu, S.C. "PyCoM: a python API to query, extract and visualise coevolution matrices". 2023


Authors
-----------
   - `Philipp Bibik <https://www.brunel.ac.uk/people/philipp-bibik>`_\*, `GitHub Link <https://github.com/cemiu>`_
     - *Lead Developer of Database, API, & Python Library*
   - `Sabriyeh Alibai <https://www.linkedin.com/in/salibai/>`_\*
     - *Literature Review, Use Cases, & Testing*
   - `Alessandro Pandini <http://pandinilab.org/>`_\*
     - *Scientific Advisor*
   - `Sarath Dantu <https://sites.google.com/view/sarathchandradantu/home>`_\*
     - *Corresponding Author, PI*

    \*Brunel University London, UK

.. toctree::
   :maxdepth: 3
   :caption: Contents:

      PyCoM <self>
      Getting Started <gettingstarted>
      Tutorials <tutorials>
      Database <database>
      Documentation <documentation>
      GitHub <https://github.com/scdantu/pycom>

Indices and tables
------------------

* :ref:`genindex`
