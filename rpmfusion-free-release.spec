%define repo free
#define repo nonfree

Name:           rpmfusion-%{repo}-release
Version:        10
Release:        4
Summary:        RPM Fusion (%{repo}) Repository Configuration

Group:          System Environment/Base
License:        BSD
URL:            http://rpmfusion.org
Source1:        rpmfusion-%{repo}.repo
Source2:        rpmfusion-%{repo}-updates.repo
Source3:        rpmfusion-%{repo}-updates-testing.repo
Source4:        rpmfusion-%{repo}-rawhide.repo
Source10:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-10-primary
Source11:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-11-primary
Source12:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-12-primary
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       system-release >= %{version}

# If apt is around, it needs to be a version with repomd support
Conflicts:      apt < 0.5.15lorg3

%if %{repo} == "nonfree"
Requires:       rpmfusion-free-release >= %{version}
# enable those once RPM Fusion is in full production and ready
# to obsolete the old repos:
#Provides:   freshrpms-release = %{version}-%{release}
#Obsoletes:  freshrpms-release <= %{version}-%{release}

#Provides:   livna-release  = %{version}-%{release}
#Obsoletes:  livna-release <= %{version}-%{release}

#Provides:   dribble-release  = %{version}-%{release}
#Obsoletes:  dribble-release <= %{version}-%{release}

%description
RPM Fusion repository contains open source and other distributable software for
Fedora. It is the merger of the Dribble, FreshRPMs and Livna repositories.

This package contains the RPM Fusion GPG key as well as Yum package manager
configuration files for RPM Fusion's "nonfree" repository, which holds
software that is not considered as Open Source Software according to the
Fedora packaging guidelines. 
%else
%description
RPM Fusion repository contains open source and other distributable software for
Fedora. It is the merger of the Dribble, FreshRPMs and Livna repositories.

This package contains the RPM Fusion GPG key as well as Yum package manager
configuration files for RPM Fusion's "free" repository, which holds only
software that is considered as Open Source Software according to the Fedora
packaging guidelines. 
%endif

%prep
echo "Nothing to prep"

%build
echo "Nothing to build"

%install
rm -rf $RPM_BUILD_ROOT

# Create dirs
install -d -m755 \
  $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg  \
  $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

# GPG Key
%{__install} -Dp -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

# compatibility symlink for easy transition to F11
ln -s $(basename %{SOURCE10}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora

# Links for the keys
for i in i386 x86_64 ppc ppc64; do
	  ln -s $(basename %{SOURCE10}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-10-${i}
  ln -s $(basename %{SOURCE11}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-11-${i}
  ln -s $(basename %{SOURCE12}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-12-${i}
done


# Yum .repo files
%{__install} -p -m644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%post
if grep 'mirrorlist=http://download1.rpmfusion.org/' %{_sysconfdir}/yum.repos.d/rpmfusion-%{repo}.repo &> /dev/null ; then
  sed -i 's!mirrorlist=http://download1.rpmfusion.org/%{repo}/fedora/.mirrorlist-%{repo}-fedora-releases$!mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=%{repo}-fedora-$releasever\&arch=$basearch!' %{_sysconfdir}/yum.repos.d/rpmfusion-%{repo}.repo
fi
if grep 'mirrorlist=http://download1.rpmfusion.org/' %{_sysconfdir}/yum.repos.d/rpmfusion-%{repo}-updates.repo &> /dev/null ; then
  sed -i 's!mirrorlist=http://download1.rpmfusion.org/%{repo}/fedora/.mirrorlist-%{repo}-fedora-updates$!mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=%{repo}-fedora-updates-released-$releasever\&arch=$basearch!' %{_sysconfdir}/yum.repos.d/rpmfusion-%{repo}-updates.repo
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki/rpm-gpg/*
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%changelog
* Sun May 17 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 10-4
- add key for F12
- some small adjustments to the spec
- add post script that switch old config files from serverside mirrorlists to
  mirrormanager

* Sat May 16 2009 Till Maas <opensource@till.name> - 10-3
- fix symlinks

* Sat May 16 2009 Till Maas <opensource@till.name> - 10-2
- allow easy transition to F11 with new gpg key and naming structure

* Sat Nov 15 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 10-1
- build for F-10

* Mon Nov 03 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9.90-5
- enable the proper mirrormanager server in the repo files

* Sat Oct 04 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9.90-4
- require system-release instead of fedora-release

* Tue Sep 30 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9.90-3
- s|download.rpmfusion.org|download1.rpmfusion.org|' *.repo
- s|basearch/debug/|basearch/os/debug/|" in *rawhide.repo

* Sun Sep 28 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9.90-2
- Fix rpmfusion-rpmfusion typo (again)
- update summary to properly say free or nonfree

* Sat Sep 27 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9.90-1
- Update for Fedora 10 rawhide
- enable devel repos, disable all the others

* Sat Sep 27 2008 Stewart Adam <s.adam at diffingo.com>	- 9-7
- Use temporary mirrorlists for now, and baseurl for the debug & source repos

* Thu Sep 18 2008 Stewart Adam <s.adam at diffingo.com>	- 9-6
- Fix rpmfusion-rpmfusion typo

* Mon Aug 18 2008 Stewart Adam <s.adam at diffingo.com> - 9-5
- Use mirrors.rpmfusion.org instead of rpmfusion.org/mirrorlist
- Use download.rpmfusion.org instead of download1.rpmfusion.org

* Fri Aug 15 2008 Stewart Adam <s.adam at diffingo.com> - 9-4
- Only include provides/obsoletes for pre-merger release RPMs in nonfree 
- Remove GPL doc

* Thu Aug 14 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 9-3
- add conditionals and macros to use one spec file for both free and nonfree
- some cleanups

* Wed Aug 13 2008 Stewart Adam <s.adam at diffingo.com> - 9-2
- Split into free and non-free RPMs based on original release RPM
- Remove double BuildArch
- Remove GPL source
- Fix mirror URLs
- devel --> rawhide

* Tue Aug 12 2008 Stewart Adam <s.adam at diffingo.com> - 9-1
- Initial RPM release

