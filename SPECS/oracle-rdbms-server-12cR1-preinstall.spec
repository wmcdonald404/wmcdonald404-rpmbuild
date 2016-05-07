%define name oracle-rdbms-server-12cR1-preinstall 
%define version 1.0
%define release 4.wmcd.el7



Summary: Sets the system for Oracle Database single instance and Real Application Cluster install for Oracle Linux 7
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
Requires:kernel
Requires:smartmontools


#As per docs
Requires:binutils compat-libstdc++-33 gcc gcc-c++ glibc glibc-devel 
Requires:ksh libaio libaio-devel libgcc libstdc++ libstdc++-devel 
Requires:make sysstat openssh-clients compat-libcap1 

#As per Orabug 20063241
Requires:psmisc

BuildRoot: %{_builddir}/%{name}-%{version}-root

%description
The Oracle Preinstallation RPM package installs software packages and sets system parameters required for Oracle Database single instance and Oracle Real Application Clusters installations for Oracle Linux Release 7
Files affected: /etc/sysctl.conf, /boot/grub/menu.lst OR /boot/grub2/grub.cfg 
Files added: /etc/security/limits.d/oracle-rdbms-server-12cR1-preinstall.conf


%prep
echo RPM_BUILD_ROOT=$RPM_BUILD_ROOT
%setup -q


%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/sysconfig/%{name}
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/bin
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/security/limits.d
mkdir -p -m 700 $RPM_BUILD_ROOT/var/log/%{name}/results

install -m 700 oracle-rdbms-server-12cR1-preinstall-verify $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 700 oracle-rdbms-server-12cR1-preinstall-verify $RPM_BUILD_ROOT/usr/bin
install -m 600 oracle-rdbms-server-12cR1-preinstall.param $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 700 oracle-rdbms-server-12cR1-preinstall-firstboot $RPM_BUILD_ROOT/etc/rc.d/init.d
touch $RPM_BUILD_ROOT/etc/security/limits.d/oracle-rdbms-server-12cR1-preinstall.conf


ln -f -s /etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall-verify $RPM_BUILD_ROOT/usr/bin/oracle-rdbms-server-12cR1-preinstall-verify 

%clean
rm -rf $RPM_BUILD_ROOT

%pre

if [ -f  /etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall.param ]; then 
  cp -f /etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall.param /var/log/%{name}/results/.oracle-rdbms-server-12cR1-preinstall.param 
fi

if [ -d /etc/sysconfig/%{name} ]; then
  rm -rf /etc/sysconfig/%{name} 
fi	

%post
/usr/bin/oracle-rdbms-server-12cR1-preinstall-verify 2> /dev/null 1>&2

if ! [ -f /etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall.conf ]; then
	chkconfig --add oracle-rdbms-server-12cR1-preinstall-firstboot 
fi

%preun
if [ "$1" = "0" ] ; then # last uninstall
 chkconfig --del oracle-rdbms-server-12cR1-preinstall-firstboot
 if [ -x /usr/bin/oracle-rdbms-server-12cR1-preinstall-verify ]; then
   /usr/bin/oracle-rdbms-server-12cR1-preinstall-verify -u 2> /dev/null 1>&2
 fi
fi

%postun
if [ "$1" = "0" ] ; then # last uninstall
 if [ -d /etc/sysconfig/%{name} ]; then
   rm -rf /etc/sysconfig/%{name} 
 fi
 if [ -d /var/log/%{name} ]; then	
   rm -rf /var/log/%{name} 	
 fi
fi

%files
%defattr(-,root,root)
%config /etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall.param
%ghost /etc/security/limits.d/oracle-rdbms-server-12cR1-preinstall.conf
/etc/sysconfig/%{name}
/etc/rc.d/init.d/oracle-rdbms-server-12cR1-preinstall-firstboot
/etc/sysconfig/%{name}/oracle-rdbms-server-12cR1-preinstall-verify  
/var/log/%{name}
/usr/bin/oracle-rdbms-server-12cR1-preinstall-verify

%changelog
* Sat May 7 2016  Will McDonald <wmcdonald@gmail.com> [1.0-4.wmcd.el7]
 - Removed the Oracle UEK dependency for use on other EL variants

* Wed Oct 14 2015  Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-4.el7]
 - Backport of Orabugs 20676277, 20675405, 20095049
 - Added parameter net.ipv4.conf.all.rp_filter
 - Changed description as per Orabug 17797216

* Tue Feb 3 2015  Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-3.el7]
 - Cleaned up code

* Wed Jan 21 2015  Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
 - Add NOZEROCONF setting

* Tue Jan 6 2015 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
 - Add memlock settings

* Fri Dec 5 2014 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
 - Add psmisc dependency per Orabug 20063241

* Fri Jul 25 2014 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-1.el7]
 - Removed 'bc' from being a dependency  

* Wed Jul 16 2014 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-1.el7]
 - Add panic_on_oops parameter per Orabug 19212317

* Thu Jul 10 2014 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-1.el7]
 - Add support for grub2 
 
* Wed Nov 20 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-11.el6]
 - do not chmod limits.conf

* Wed Nov 6 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-10.el6]
 - Fix update grub.conf bug
 - Retain  manual changes
 - fix build warning,bz15552

* Tue Jul 2 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-9.el6]
 - Disable THP 1557478.1, bug17029612
 - update license to GPLv2.

* Fri Apr 23 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-8.el6]
 - include limits.conf in rpm context.

* Fri Apr 23 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-7.el6]
 - generate limits.conf

* Fri Apr 19 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-6.el6]
 - fix comments in limits.conf

* Fri Apr 19 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-5.el6]
 - Increase nproc soft limit to 16384, orabug15971421

* Thu Apr 4 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-4.el6]
 - Remove comments in sysctl.conf related to i386

* Wed Apr 3 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-3.el6]
 - revert: make rpm conflict with older preinstall rpms.

* Fri Jan 18 2013 Gurudas Pai <gurudas.pai@oracle.com> [1.0-2.el6]
 - make rpm conflict with older preinstall rpms.

* Wed Jul 07 2012 Gurudas Pai <gurudas.pai@oracle.com> [1.0-1.el6]
 - Created based on 11g preinstall. 
 - Added oracle-rdbms-server-12cR1-preinstall.conf under 
   /etc/security/limits.d/
 - For sysctl.conf and grub.conf revert change on uninstall 
   rather than copying file from backup which result in missing 
   newer changes.	
 - Do not change sysctl values if they are already higher than 
   preinstall requirement.
 - id chek for firstboot.
 - remove execute privilege for non-root user.
 - move params backup under var/log
