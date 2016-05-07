# wmcdonald404-rpmbuild

RPM build tree for various occasionally maintained packages.

# oracle-preinstall
The Oracle Preinstall (formerly Oracle Validated) RPMs prepare a host with the correct users, groups, memberships, package dependencies and a set of sensible defaults for shell and kernel tunables ready for Oracle RDBMS and Grid Infrastructure installation.

The packages in http://public-yum.oracle.com/ do impose a dependency on the oracle-uek which results in installation failures on other EL variants.

This is easily resolved by removing that dependency and rebuilding the packages.

