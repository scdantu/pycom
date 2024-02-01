.. PyCoM documentation master file


Introduction!
=============

   PyCoM is a Python API to the Coevolution Matrix database (PyCoMdb), containing *457,622* annotated proteins, from `UniProtKB/Swiss-Prot <https://www.expasy.org/resources/uniprotkb-swiss-prot>`_  with their coevolution matrices calculated using `HH-suite3 <https://github.com/soedinglab/hh-suite>`_ and `CCMpred <https://github.com/soedinglab/CCMpred>`_.

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


   If you are more interested in alignment data (rather than Protein Residue-Residue Contacts), we also provide these at: https://pycom.brunel.ac.uk/alignments/

   The parameters for generating the alignment using `HH-suite3 <https://github.com/soedinglab/hh-suite>`_  can be found in `Kamisetty et al. 2013 <https://www.pnas.org/doi/10.1073/pnas.1314045110>`_.



How to Cite
-----------

   Bibik. P, Alibai. S, Pandini. A, Dantu, S.C. "PyCoM: a python API to query, extract and visualise coevolution matrices". 2023


.. toctree::
   :maxdepth: 3
   :caption: Contents:

      Getting Started <gettingstarted>
      Tutorials <tutorials>
      GitHub <https://google.com>
      Database <database>
      Documentation <documentation>
      Help <help>

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
