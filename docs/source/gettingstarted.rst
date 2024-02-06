Getting Started
===============

You can easily install PyCoM using pip, from our `GitHub respository <https://github.com/scdantu/pycom>`_.

.. code-block:: bash

    pip3 install git+https://github.com/scdantu/pycom

Now, you are ready to use PyCoM:

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

Optionally download the database locally, to speed up the loading: https://pycom.brunel.ac.uk/downloads/

.. toctree::
   :name: gstoc
   :hidden:
   :titlesonly:
   :maxdepth: 3

      ../../tutorials/00_Getting_Started_Locally
      ../../tutorials/00_Getting_Started_Remotely
      ../../tutorials/00_WebAPI

Quick guides
------------

Here are some quick guides on starting up using PyCoM:

You can use PyCoM in three different ways:

- `PyCoM (local) tutorial <tutorials/00_Getting_Started_Locally.html>`_: Download the database to your computer and use PyCoM.
- `PyCoM (remote) tutorial <tutorials/00_Getting_Started_Remotely.html>`_: Work with the database on PyCoM server using PyCoM.
- `WebAPI tutorial <tutorials/00_WebAPI.html>`_: Work with the WebAPI without using PyCoM.

There is also a Alignment File Repository, where 370,000+ alignment files are available for download. See: https://pycom.brunel.ac.uk/alignments/

More indepth tutorials are available in the `Tutorials <tutorials.html>`_ section.

Differences
-----------

You can work with PyCoMdb in three different modes:
   #. *PyCoM (local)*: Download the database to your computer and use PyCoM.
   #. *PyCoM (remote)*: Work with the database on PyCoM server using PyCoM.
   #. *WebAPI*: Work with the WebAPI without using PyCoM.


Using PyCoM (local) allows access to all the functional features, while PyCoM (remote) and the WebAPI has some limitations as shown in the table below:

.. xlsx-table::
   :file: tables/Table2.xlsx
   :sheet: Sheet1
   :header-rows: 1
