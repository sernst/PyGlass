PyGlass
=======

A PySide powered application framework for faster, easier desktop application development. Some
key features are:

 * Efficient resource management system
 * Transparent UI design File support in widgets
 * SQLAlchemy integration with Alembic migration capabilities
 * Streamlined widget classes for easier custom styling
 * Designed for application compilation using py2exe and py2app

Resource Management
-------------------
PyGlass implements a Qt-independent resource management system with simplified application and
widget level resource access and transparent resource handling in both source and installed
applications.

SQLAlchemy Integration
----------------------
PyGlass includes SQLAlchemy for data-driven (SQLite) applications. The framework locates the
databases within the resource system mentioned above with resource specified engine URLs. Alembic
is also included and integrated into the system for handling database migration during application
updates.
