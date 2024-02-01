Install
=======

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

Optionally download the database locally, to speed up the loading: https://pycom.brunel.ac.uk/downloads/

Quick guides
------------

You can use PyCoM in three different ways:

- **PyCoM (local)**: Download the database to your computer and use PyCoM.
- **PyCoM (remote)**: Work with the database on PyCoM server using PyCoM.
- **WebAPI**: Work with the WebAPI without using PyCoM.

.. toctree::
   :numbered:
   :name: gstoc
   :titlesonly:
   :maxdepth: 3

      ../../tutorials/00_Getting_Started_Locally
      ../../tutorials/00_Getting_Started_Remotely
      ../../tutorials/00_WebAPI


Additionally we also provide the alignments for the proteins in the database, which can be used to generate the contact maps. See: https://pycom.brunel.ac.uk/alignments/

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
