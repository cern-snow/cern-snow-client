.. This file is part of the cern-snow-client library.
   Copyright (c) 2017 CERN
   Authors:
   - James Clerc <james.clerc@cern.ch> <james.clerc@epitech.eu>
   - David Martin Clavo <david.martin.clavo@cern.ch>

   The cern-snow-client library is free software; you can redistribute it
   and/or modify it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

   The cern-snow-client library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with the cern-snow-client library.  If not, see <http://www.gnu.org/licenses/>.

   In applying this license, CERN does not waive the privileges and immunities granted to it by virtue of its status
   as an Intergovernmental Organization or submit itself to any jurisdiction.

.. cern-snow-client documentation master file, created by
   sphinx-quickstart on Mon Nov  6 23:36:54 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for the cern-snow-client library
==============================================

The CERN ServiceNow Client library (CERN SNow Client) facilitates the usage of the ServiceNow REST API with a
CERN account via Single Sign On authentication. Basic Authentication is also supported.

Low level operations such as get, post and put are implemented. Also, other higher level operations
have been implemented, such as querying/inserting/updating records,
or querying/inserting/updating incidents and requests, including adding comments and work notes.

You can find below the documentation for the different modules:

.. toctree::
   :maxdepth: 4

   cern_snow_client
   tests


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
