# hdbpp-innodb-partition-management

- [hdbpp-innodb-partition-management](#hdbpp-innodb-partition-management)
  - [Dependencies](#Dependencies)
  - [Usage](#Usage)
  - [License](#License)

WORK IN PROGRESS - Current release is still a development release.

This is a Python script to manage hdbpp InnoDB partitions. The aim is to create new partition for the incoming year and move old partitiond from the 'live' db to an 'archive' db. 

## Dependencies

Following Python dependencies are required for direct deployment or development:

* mysql-connector

## Usage

The script has a simple command line help menu with some helpful utilities. To view:

```bash
./hdbpp-innodb-partition-management.py --help
```

## License

The source code is released under the LGPL3 license and a copy of this license is provided with the code.
