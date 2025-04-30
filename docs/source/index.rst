.. PyCoM documentation master file

Welcome to PyCoM: Unlock the Power of Protein Coevolution Analysis!
=============================================================================

April 2025: **Introducing PyCoM-Web:** Seamlessly access the extensive PyCoM database through our intuitive web interface— `pycomweb <pycomweb.html>`_.

**PyCoM – Protein Coevolution Database (API & Python Library)**
=============================================================================

PyCoM provides researchers and bioinformaticians with a database of **457,622 annotated proteins and Coevolution Matrices** alongside an intuitive Python API, a comprehensive library with tools for analysis, and REST API. sourced from `UniProtKB/Swiss-Prot <https://www.expasy.org/resources/uniprotkb-swiss-prot>`_ and processed with `HH-suite3 <https://github.com/soedinglab/hh-suite>`_ and `CCMpred <https://github.com/soedinglab/CCMpred>`_. PyCoM simplifies the complex task of protein coevolution analysis. Additionally we host the *PyCoM Alignment Repository*, containing pre-computed for most proteins in SwissProt.

**Why PyCoM?**

- **Ease of Use:** Rapidly query, extract, and visualize protein annotation and coevolution data!
- **Comprehensive Tutorials:** Quickly get started with detailed `tutorials <tutorials.html>`_ to maximise your research impact.
- Enables **Large Scale Analysis** of coevolution data taking 35 CPU-core years and 1 GPU year to compute

**Installation Made Easy:**

Begin exploring immediately:

.. code-block:: bash

    pip3 install git+https://github.com/scdantu/pycom

**Example Usage:**

Effortlessly query proteins linked to specific conditions, visualize coevolution matrices, and perform sophisticated analyses:

.. code-block:: py3

    from pycom import PyCom, CoMAnalysis
    import matplotlib.pyplot as plt

    pyc = PyCom(remote=True)
    prots = pyc.find(
        min_length=200, max_length=210,
        disease='cancer', has_substrate=True,
        matrix=True, page=1
    )

    CoMAnalysis().add_contact_predictions(prots)

    plt.axis('off')
    plt.title(f'Contact Map for uniprot_id={prots.uniprot_id[0]}')
    plt.imshow(prots.contact_matrix[0])
    plt.show()

    print(prots.iloc[0])

**Example Output:**

.. list-table::
    :widths: 50 50

    * - .. image:: _static/example_run.png
           :alt: Output of the code above

      - .. code-block::

            uniprot_id           P62070
            neff                 12.754
            sequence_length      204
            sequence             MAAAGWRDGSGQEK...
            organism_id          9606
            helix_frac           0.29902
            turn_frac            0.019608
            strand_frac          0.220588
            has_ptm              1
            has_pdb              1
            has_substrate        1
            matrix               [[0.0, 0.268, ...
            contact_matrix       [[0.0, 0.0,   ...
            Name: 0, dtype: object

(If the image is not displaying, click `here <_images/example_run.png>`_.)

**Key Features**
-------------------------

- **PyCoMdb**: Extensive database of coevolution matrices, accessible at `PyCoMdb Downloads <https://pycom.brunel.ac.uk/downloads/>`_.
- **PyCoM Python Library**:
  - **Querying**: Quickly find proteins by specific criteria.
  - **Coevolution Matrix Analysis**: Visualize and analyze detailed coevolution data (`Analysis Tutorial <tutorials/01_Workflow.html>`_).
  - **PDB & AlphaFold Analysis**: Integrated tools for protein structure parsing and analysis (`PDB Tutorial <tutorials/05_Contact_Map_and_PDB.html>`_).

- **RESTful API**:
  - Direct and flexible access through our RESTful API (`API Guide <tutorials/00_WebAPI.html>`_).
  - Available at: https://pycom.brunel.ac.uk/api/

- **Alignment File Repository**:
  - Over 370,000 protein alignment files available at `Alignment Repository <https://pycom.brunel.ac.uk/alignments/>`_.
  - Comprehensive guide: `Alignment Analysis Tutorial <tutorials/03_Alignment_analysis.html>`_.

Alignment generation parameters via `HH-suite3 <https://github.com/soedinglab/hh-suite>`_ are detailed in `Kamisetty et al. 2013 <https://www.pnas.org/doi/10.1073/pnas.1314045110>`_.

How to Cite PyCoM
-------------------------

Please cite the following if PyCoM supports your research:

**Harvard-style citation**:
Glass, P.E., Alibai, S., Pandini, A. & Dantu, S.C., 2024. PyCoM: a Python library for large-scale analysis of residue–residue coevolution data. *Bioinformatics*, 40(4), p.btae166. https://doi.org/10.1093/bioinformatics/btae166

**BibTeX**:

.. code-block:: bibtex

    @article{glass2024pycom,
        author = {Glass, Philipp E and Alibai, Sabriyeh and Pandini, Alessandro and Dantu, Sarath Chandra},
        title = "{PyCoM: a python library for large-scale analysis of residue–residue coevolution data}",
        journal = {Bioinformatics},
        volume = {40},
        number = {4},
        pages = {btae166},
        year = {2024},
        url = {https://doi.org/10.1093/bioinformatics/btae166},
    }

**Our Team**
-------------------------
- **Philipp E. Glass** (`Personal Site <https://cemiu.net/>`_), Lead Developer
- **Sabriyeh Alibai** (`LinkedIn <https://www.linkedin.com/in/salibai/>`_), Literature Review & Testing
- **Alessandro Pandini** (`Personal Site <http://pandinilab.org/>`_), Scientific Advisor
- **Sarath Chandra Dantu** (`Personal Site <https://sites.google.com/view/sarathchandradantu/home>`_), Corresponding Author, PI

Brunel University London, UK

.. toctree::
   :maxdepth: 3
   :caption: Explore Further:

   PyCoM <self>
   Getting Started <gettingstarted>
   Tutorials <tutorials>
   Database <database>
   Documentation <documentation>
   GitHub <https://github.com/scdantu/pycom>

Indices and tables
------------------

* :ref:`genindex`

