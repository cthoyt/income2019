table-validator
===============
Use tables with validation schemata to validate other tables.

Installation
------------
Install directly from `GitHub <https://github.com/cthoyt/table-validator>`_ with:

.. code-block:: sh

   $ pip install git+https://github.com/cthoyt/table-validator.git

Testing
-------
Install ``tox`` with ``pip install tox`` then run with ``tox``.

CLI Usage
---------
Installation with ``pip`` adds a command ``table_validator`` that takes two arguments: a path to the template file,
and a path to the candidate file. Given files ``template.tsv`` and ``candidate.tsv``:

.. code-block:: tsv

    # template.tsv
    	C_A C_B C_C
    R_1 {INT(REQUIRED=TRUE)}	{INT(REQUIRED=TRUE)}	{INT(REQUIRED=TRUE)}

.. code-block:: tsv

    # candidate.tsv
    	C_A C_B C_C
    R_1 1	2	3

You can run:

.. code-block:: sh

    $ table_validator template.tsv candidate.tsv
