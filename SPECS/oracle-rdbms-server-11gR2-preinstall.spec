%define name oracle-rdbms-server-11gR2-preinstall 
%define version 1.0
%define release 4.el7



Summary: Sets the system for Oracle single instance and Real Application Cluster install for Oracle Linux 7
Name: %{name}
Version: %{version}
Release: %{release}
Group: Test Environment/Libraries
License: GPLv2
Vendor:Oracle
Source: %{name}-%{version}.tar.gz

Provides: %{name} = %{version}

Requires(pre):/etc/redhat-release

#System requirement
Requires:procps module-init-tools ethtool initscripts 
Requires:bind-utils nfs-utils util-linux-ng pam
Requires:xorg-x11-utils xorg-x11-xauth 
Requires:kernel-uek
Requires:smartmontools

# Per Orabug 20063241
Requires:psmisc

#As per cert/11203crs/db-cvu_prereq.xml
Requires:binutils compat-libstdc++-33 gcc gcc-c++ glibc glibc-devel 
Requires:ksh libaio libaio-devel libgcc libstdc++ libstdc++-devel 
Requires:make sysstat openssh-clients compat-libcap1     


BuildRoot: %{_builddir}/%{name}-%{version}-root

# Per Orabug 17797216 
%description
The Oracle Preinstallation RPM package installs software packages and sets system parameters required for Oracle Database single instance and Oracle  Real Application Clusters installations for Oracle Linux Release 7
Files affected: /etc/sysctl.conf, /etc/security/limits.conf, /boot/grub/menu.lst or /boot/grub2/grub.cfg.

%prep
echo RPM_BUILD_ROOT=$RPM_BUILD_ROOT
%setup -q


%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/sysconfig/%{name}
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/bin
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p -m 700 $RPM_BUILD_ROOT/var/log/%{name}/results

install -m 744 oracle-rdbms-server-11gR2-preinstall-verify $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 744 oracle-rdbms-server-11gR2-preinstall-verify $RPM_BUILD_ROOT/usr/bin
install -m 644 oracle-rdbms-server-11gR2-preinstall.param $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 744 oracle-rdbms-server-11gR2-preinstall-firstboot $RPM_BUILD_ROOT/etc/rc.d/init.d
ln -f -s /etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall-verify $RPM_BUILD_ROOT/usr/bin/oracle-rdbms-server-11gR2-preinstall-verify 2> /dev/null;

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -f  /etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall.param ]; then 
  cp -f /etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall.param /var/log/%{name}/results/.oracle-rdbms-server-11gR2-preinstall.param 2> /dev/null
fi

if [ -d /etc/sysconfig/%{name} ]; then
  rm -rf /etc/sysconfig/%{name} 2> /dev/null
fi	

%post
/usr/bin/oracle-rdbms-server-11gR2-preinstall-verify 2> /dev/null 1>&2

if ! [ -f /etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall.conf ]; then
	chkconfig --add oracle-rdbms-server-11gR2-preinstall-firstboot 
fi

%preun
if [ "$1" = "0" ] ; then # last uninstall
 chkconfig --del oracle-rdbms-server-11gR2-preinstall-firstboot
 if [ -x /usr/bin/oracle-rdbms-server-11gR2-preinstall-verify ]; then
   /usr/bin/oracle-rdbms-server-11gR2-preinstall-verify -u 2> /dev/null 1>&2
 fi
fi

%postun
if [ "$1" = "0" ] ; then # last uninstall
 if [ -d /etc/sysconfig/%{name} ]; then
   rm /usr/bin/oracle-rdbms-server-11gR2-preinstall-verify 2> /dev/null
   rm -rf /etc/sysconfig/%{name} 2> /dev/null
 fi
 if [ -d /var/log/%{name} ]; then	
   rm -rf /var/log/%{name} 2> /dev/null	
 fi
fi

%files
%defattr(-,root,root)
%config /etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall.param
/etc/sysconfig/%{name}/oracle-rdbms-server-11gR2-preinstall-verify
/usr/bin/oracle-rdbms-server-11gR2-preinstall-verify
/etc/rc.d/init.d/oracle-rdbms-server-11gR2-preinstall-firstboot
/var/log/%{name}
/etc/sysconfig/%{name}

%changelog
* Tue Oct 13 2015 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-4.el7]
      - Fix for Orabugs 20676277, 20675405, 20095949
      - Fix for Orabug 17797216 
      - Added parameter net.ipv4.conf.all.rp_filter, net.ipv4.conf.default.rp_filter

* Tue Feb 3 2015 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-3.el7]
      - Cleaned up Code

* Thu Jan 22 2015 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
      - Added settings for NOZEROCONF 

* Fri Jan 2 2015 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
      - Added psmisc as a dependency, bug20063241, Added memlock settings 

* Thu Jul 24 2014 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-1.el7]
      - Removed 'bc' from being a dependency
      - Added GRUB2 support

* Wed Nov 20 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-9.el6]
      - do not chmod limits.conf

* Tue Oct 29 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-8.el6]
      - Disable THP 1557478.1, bug17029612
      - update license to GPLv2.
      - Increase nproc soft limit to 16384, orabug15971421
      - Do not change values if it is already higher
      - fix rpm remove issue of missing updates.
      - fix warning in build of preinstall bz15552

* Thu Dec 24 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-7.el6]
      - id check for firstboot bz14121
      - remove execute privilege for non-root user.
	
* Thu Jun 07 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-6.el6]
      - fixed comment in sysctl.conf

* Wed May 30 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-5.el6]
      - fixed comment in limits.conf

* Tue Apr 10 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-4.el6]
      - kernel.shmall=2097152  for x86
      - kernel.shmmax=4294967295 for x86 

* Mon Mar 26 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-3.el6]
      - Added smartmontools as dependency, bz13653

* Thu Mar 22 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-2.el6]
      - kernel.shmall=1073741824 as per bz7256 
      - kernel.shmmax=4398046511104 as per bz7256
      - stack hard = 32768 as per doc max limit

* Thu Mar 22 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-1.el6]
      - Renamed rpm to oracle-rdbms-server-11gR2-preinstall
      - Included xorg-x11-utils xorg-x11-xauth as dependency bz13653
      - Included kernel-uek as dependency.
      - fs.aio-max-nr=1048576 to match document,bz13653
      - kernel.shmall=2097152 to match document,bz13653
      - kernel.shmmax=536870912 to match document,bz13653
      - nofile soft = 1024 to match document,bz13653
      - nofile hard = 65536 to match document,bz13653
      - nproc soft = 2047 to match document,bz13653
      - nproc hard = 16384 to match document,bz13653
      - stack soft = 10240 to match document,bz13653
      - stack hard = 10240 to match document,bz13653
      

* Wed Nov 9 2011 Gurudas Pai <gurudas.pai@oracle.com> [1.0.0-3.el6]
      - removed util-linux and added util-linux-ng (fork of util-linux)
      - removed openssh and added openssh-clients bz13173
      - removed 32 bit dependency for x86_64 as per st docs.
      - removed kernel-uek-headers/kernel-headers
      - disable login for oracle user for bug12623491
      - Merge fix
      - Removed msgmni, msgmnb, msgmax for bz11029
      - Increase stack limit for oracle user bz11683
      - bugfix for bug11656858
      - added compat-libcap1 dependency bz12221
      - move link creation to install part bz11030
      - removed comment related to bugdb6820451	
      - removed flowcontrol settings bz11508	
      - Removed 10G related info from oracle-rdbms-server-11gR2-preinstall.param
      - Changed kernel.semmni to 128 as per 11203crs-cvu_prereq.xml
      - removed vm.min_free_kbytes
      - removed readme 
     
* Tue Sep 07 2010 Tianyue Lan <tianyue.lan@oracle.com> [1.0.0-1.el6]
      - Changed requirement for x86_64 arch
        /lib/libaio.so.1
        libodbc.so.2()(64bit)
        /usr/lib/libodbc.so.2
        /usr/lib/gcc/x86_64-redhat-linux/4.4.4/libstdc++.a

