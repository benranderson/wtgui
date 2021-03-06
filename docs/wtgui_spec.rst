======================================
 WTGUI Program Specification
======================================


Description
-----------
WTGUI streamlines the process of carrying out wall thickness calculations in
accordance with PD 8010-2 and provides a means of persisting a database of
previous calculations.

Functionality Required
----------------------

The program must:

* provide a UI for reading, updating and appending data to the CSV file
* allow all relevant, valid input data to be entered, as per PD8010-2 requirements
* append entered input data to a CSV file
  - The CSV file must have a filename of wt_data_CURRENTDATE.csv,
    where CURRENTDATE is the date of the calculation in ISO format (Year-month-day)
  - The CSV file must have all required input parameters
* enforce correct datatypes per field
* prevent running the calculation when errors are present

The program should try, whenever possible, to:

* enforce reasonable limits on data entered
* Auto-fill data
* Suggest likely correct values
* Provide a smooth and efficient workflow

Functionality Not Required
--------------------------

The program does not need to:

* Allow deletion of data.

Limitations
-----------

The program must:

* Be efficiently operable by keyboard-only users.
* Be accessible to color blind users.
* Run on Debian Linux.
* Run acceptably on a low-end PC.

Data Dictionary
---------------
+------------+----------+------+------------------+--------------------------+
|Field       | Datatype | Units| Range            |Descripton                |
+============+==========+======+==================+==========================+
|Date        |Date      |      |                  |Date of record            |
+------------+----------+------+------------------+--------------------------+
|Time        |Time      |      |8:00, 12:00,      |Time period               |
|            |          |      |16:00, or 20:00   |                          |
+------------+----------+------+------------------+--------------------------+
|Lab         |String    |      | A - E            |Lab ID                    |
+------------+----------+------+------------------+--------------------------+
|Technician  |String    |      |                  |Technician name           |
+------------+----------+------+------------------+--------------------------+
|Plot        |Int       |      | 1 - 20           |Plot ID                   |
+------------+----------+------+------------------+--------------------------+
|Seed        |String    |      |                  |Seed sample ID            |
|sample      |          |      |                  |                          |
+------------+----------+------+------------------+--------------------------+
|Fault       |Bool      |      |                  |Fault on environmental    |
|            |          |      |                  |sensor                    |
+------------+----------+------+------------------+--------------------------+
|Light       |Decimal   |klx   | 0 - 100          |Light at plot             |
+------------+----------+------+------------------+--------------------------+
|Humidity    |Decimal   |g/m³  | 0.5 - 52.0       |Abs humidity at plot      |
+------------+----------+------+------------------+--------------------------+
|Temperature |Decimal   |°C    | 4 - 40           |Temperature at plot       |
+------------+----------+------+------------------+--------------------------+
|Blossoms    |Int       |      | 0 - 1000         |Number of blossoms in plot|
+------------+----------+------+------------------+--------------------------+
|Fruit       |Int       |      | 0 - 1000         |Number of fruits in plot  |
+------------+----------+------+------------------+--------------------------+
|Plants      |Int       |      | 0 - 20           |Number of plants in plot  |
+------------+----------+------+------------------+--------------------------+
|Max height  |Decimal   |cm    | 0 - 1000         |Height of tallest plant in|
|            |          |      |                  |plot                      |
+------------+----------+------+------------------+--------------------------+
|Min height  |Decimal   |cm    | 0 - 1000         |Height of shortest plant  |
|            |          |      |                  |in plot                   |
+------------+----------+------+------------------+--------------------------+
|Median      |Decimal   |cm    | 0 - 1000         |Median height of plants in|
|height      |          |      |                  |plot                      |
+------------+----------+------+------------------+--------------------------+
|Notes       |String    |      |                  |Miscellaneous notes       |
+------------+----------+------+------------------+--------------------------+
