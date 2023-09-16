Install
=======

   You can easily install PyCoM using pip from the source code on `github respository <https://github.com/scdantu/pycom>`_. 

.. code-block:: bash

    pip3 install git+https://github.com/scdantu/pycom

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
  
  
Quick guides
------------

Here are some quick guides on how to work with three different modes of PyCoM.

.. toctree::
   :numbered:
   :name: gstoc
   :titlesonly:
   :maxdepth: 3
   
      ../../tutorials/jp_notebooks/getting_started/01_PyCoM_Local
      ../../tutorials/jp_notebooks/getting_started/02_PyCoM_Remote
      ../../tutorials/jp_notebooks/getting_started/03_WebAPI
      