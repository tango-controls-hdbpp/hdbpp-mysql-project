# hdbpp-mysql-project

[![TangoControls](https://img.shields.io/badge/-Tango--Controls-7ABB45.svg?style=flat&logo=%20data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAkCAYAAADo6zjiAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAsFJREFUWIXtl01IFVEYht9zU%2FvTqOxShLowlOgHykWUGEjUKqiocB1FQURB0KJaRdGiaFM7gzZRLWpTq2olhNQyCtpYCP1gNyIoUTFNnxZzRs8dzvw4Q6564XLnfOf73vedc2a%2BmZEKALgHrC3CUUR8CxZFeEoFalsdM4uLmMgFoIlZLJp3A9ZE4S2oKehhlaR1BTnyg2ocnW%2FxsxEDhbYij4EPVncaeASMAavnS%2FwA8NMaqACNQCew3f4as3KZOYh2SuqTVJeQNiFpn6QGSRVjTH9W%2FiThvcCn6H6n4BvQDvQWFT%2BSIDIFDAKfE3KOAQeBfB0XGPeQvgE67P8ZoB44DvTHmFgJdOQRv%2BUjc%2BavA9siNTWemgfA3TwGquCZ3w8szFIL1ALngIZorndvgJOR0GlP2gtJkzH%2Bd0fGFxW07NqY%2FCrx5QRXcYjbCbmxF1dkBSbi8kpACah3Yi2Sys74cVyxMWY6bk5BTwgRe%2BYlSzLmxNpU3aBeJogk4XWWpJKUeiap3RJYCpQj4QWZDQCuyIAk19Auj%2BAFYGZZjTGjksaBESB8P9iaxUBIaJzjZcCQcwHdj%2BS2Al0xPOeBYYKHk4vfmQ3Y8YkIwRUb7wQGU7j2ePrA1URx93ayd8UpD8klyPbSQfCOMIO05MbI%2BDvwBbjsMdGTwlX21AAMZzEerkaI9zFkP4AeYCPBg6gNuEb6I%2FthFgN1KSQupqzoRELOSed4DGiJala1UmOMr2U%2Bl%2FTWEy9Japa%2Fy41IWi%2FJ3d4%2FkkaAw0Bz3AocArqApwTvet3O3GbgV8qqjAM7bf4N4KMztwTodcYVyelywKSCD5V3xphNXoezuTskNSl4bgxJ6jPGVJJqbN0aSV%2Bd0M0aO7FCs19Jo2lExphXaTkxdRVgQFK7DZVDZ8%2BcpdmQh3wuILh7ut3AEyt%2B51%2BL%2F0cUfwFOX0t0StltmQAAAABJRU5ErkJggg%3D%3D)](http://www.tango-controls.org) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![](https://img.shields.io/github/release/tango-controls-hdbpp/hdbpp-mysql-project.svg)](https://github.com/tango-controls-hdbpp/hdbpp-mysql-project/releases)

- [hdbpp-mysql-project](#hdbpp-mysql-project)
  - [Cloning](#Cloning)
  - [Versioning](#Versioning)
  - [Overview](#Overview)
    - [services](#services)
    - [resources](#resources)
    - [external](#external)
    - [doc](#doc)
  - [Building](#Building)
    - [External Components](#External-Components)
  - [License](#License)

The hdbpp mysql project is a Tango Control system archival backend. The project includes all additional services required by the project, and consolidates various generic components into a single fetch and build cmake system.

Additional documentation is stored in the doc folder, and indexed on its [README](doc/)

Some of the information assumes familiarity with MySQL terms and technologies. Please to MySQL [documentation](https://dev.mysql.com/doc/) for more information.

## Cloning 

To successfully clone the project use the following git command:

```bash
git clone https://github.com/tango-controls-hdbpp/hdbpp-mysql-project.git
```

## Versioning

The project is tagged with a version. 

## Overview

Brief overview of the modules:

### services

Contains various services deployed to assist in running the hdbpp database partitioning operation. Its recommended to use the Docker images to ease deployment.

### resources

Project resources. Including the HDB++ schema, MySQL InnoDB HDB++ Docker images, test scripts that can allow a user to test the project quickly, and any other additional item that may help the user in deploying, testing or running the system.

### external

This directory will be created at CMake configuration time and will contain the external dependencies for the complete build. These are currently hdbpp-es, hdbpp-cm, libhdbpp and libhdbpp-mysql.

### doc

Project documentation

## Building

The build system will build both external and in project dependencies.

### External Components

The project contains a consolidated build system to fetch build all required external dependencies. These are currently:

- [hdbpp-es](https://github.com/tango-controls-hdbpp/hdbpp-es)
- [hdbpp-cm](https://github.com/tango-controls-hdbpp/hdbpp-cm)
- [libhdbpp](https://github.com/tango-controls-hdbpp/libhdbpp)
- [libhdbpp-mysql](https://github.com/tango-controls-hdbpp/libhdbpp-mysql)

The CMakeLists.txt file defines the tag or branch for each of these projects the build system will fetch and build. It currently uses the following tags/branchs:

| Component | Tag/Branch |
|------|-----|
| hdbpp-es | v2.0.0 |
| hdbpp-cm | v2.0.0 |
| libhdbpp | v2.0.0 |
| libhdbpp-mysql | libhdbpp2 |

See the [build](doc/build.md) guide in the doc folder on how to build the project and its external dependencies.

The various services are python scripts, these can be deployed as a script, or a built as Docker images with the supplied build system. Each service comes with a short README on how to build and deploy it:

- [hdbpp-innodb-partition-management](services/hdbpp-innodb-partition-management)

## License

The code is released under the LGPL3 license and a copy of this license is provided with the code. Full license [here](LICENSE.md)
