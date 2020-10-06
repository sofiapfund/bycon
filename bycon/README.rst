|License: CC0-1.0|

Bycon - a Python-based environment for the Beacon v2 genomics API
-----------------------------------------------------------------

The ``bycon`` project - at least at its current stage - is a mix of
*Progenetix* (i.e. GA4GH object model derived, *MongoDB* implemented) -
data management, and the implementation of middleware & server for the
Beacon API.

More information about the current status of the package can be found in
the inline documentation which is also `presented in an accessible
format <https://info.progenetix.org/tags/Beacon.html>`__ on the
*Progenetix* website.

More Documentation
~~~~~~~~~~~~~~~~~~

`ByconPlus <./doc/byconplus.md>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This page provides more information about the *Beacon* functionality,
current implementation status and usage examples.

`Services <./doc/services.md>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *bycon* environment - together with the
`Progenetix <http://progenetix.org>`__ resource - provide a growing
numer of data services in (cancer) genomics and disease ontologies.
*bycon*\ ’s services are tools to enable the APIs.

Directory Structure
~~~~~~~~~~~~~~~~~~~

``bin``
'''''''

-  web applications for data access

``bycon``
'''''''''

-  Python modules for Beacon query and response functions

``config``
''''''''''

-  configuration files, separated for topic/scope
-  YAML …

``doc``
'''''''

-  documentation, in Markdown
-  also invoked by ``-h`` flag

.. |License: CC0-1.0| image:: https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg
   :target: http://creativecommons.org/publicdomain/zero/1.0/
