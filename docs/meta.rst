Meta-Documentation
==================

This page documents the documentation. How very meta. Sphinx is used
to document this project. Since documentation will mostly be written
and built from the local development environment, we simply ensure
that the latest version of ``Sphinx`` is included in 
``<repo_root>/requirements/local.txt``. It does not need to be included
in ``base.txt``.    

This documentation was created using the ``sphinx-quickstart`` command, 
and lives at ``<repo_root>/docs``.

Refer to the following to see the options selected at the time of creation::

  $ sphinx-quickstart
  Welcome to the Sphinx 1.2.3 quickstart utility.

  Please enter values for the following settings (just press Enter to
  accept a default value, if one is given in brackets).

  Enter the root path for documentation.
  > Root path for the documentation [.]: doc

  You have two options for placing the build directory for Sphinx output.
  Either, you use a directory "_build" within the root path, or you separate
  "source" and "build" directories within the root path.
  > Separate source and build directories (y/n) [n]: n

  Inside the root directory, two more directories will be created; "_templates"
  for custom HTML templates and "_static" for custom stylesheets and other static
  files. You can enter another prefix (such as ".") to replace the underscore.
  > Name prefix for templates and static dir [_]: 

  The project name will occur in several places in the built documentation.
  > Project name: NBA Statistics  
  > Author name(s): Louis Tiao

  Sphinx has the notion of a "version" and a "release" for the
  software. Each version can have multiple releases. For example, for
  Python the version is something like 2.5 or 3.0, while the release is
  something like 2.5.1 or 3.0a1.  If you don't need this dual structure,
  just set both to the same value.
  > Project version: 1.0
  > Project release [1.0]: 

  The file name suffix for source files. Commonly, this is either ".txt"
  or ".rst".  Only files with this suffix are considered documents.
  > Source file suffix [.rst]: 

  One document is special in that it is considered the top node of the
  "contents tree", that is, it is the root of the hierarchical structure
  of the documents. Normally, this is "index", but if your "index"
  document is a custom template, you can also set this to another filename.
  > Name of your master document (without suffix) [index]: 

  Sphinx can also add configuration for epub output:
  > Do you want to use the epub builder (y/n) [n]: y

  Please indicate if you want to use one of the following Sphinx extensions:
  > autodoc: automatically insert docstrings from modules (y/n) [n]: y
  > doctest: automatically test code snippets in doctest blocks (y/n) [n]: y
  > intersphinx: link between Sphinx documentation of different projects (y/n) [n]: n
  > todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: y
  > coverage: checks for documentation coverage (y/n) [n]: y
  > pngmath: include math, rendered as PNG images (y/n) [n]: 
  > mathjax: include math, rendered in the browser by MathJax (y/n) [n]: y
  > ifconfig: conditional inclusion of content based on config values (y/n) [n]: y
  > viewcode: include links to the source code of documented Python objects (y/n) [n]: y

  A Makefile and a Windows command file can be generated for you so that you
  only have to run e.g. `make html' instead of invoking sphinx-build
  directly.
  > Create Makefile? (y/n) [y]: y
  > Create Windows command file? (y/n) [y]: n

  Creating file doc/conf.py.
  Creating file doc/index.rst.
  Creating file doc/Makefile.

  Finished: An initial directory structure has been created.

  You should now populate your master file doc/index.rst and create other documentation
  source files. Use the Makefile to build the docs, like so:
     make builder
  where "builder" is one of the supported builders, e.g. html, latex or linkcheck.