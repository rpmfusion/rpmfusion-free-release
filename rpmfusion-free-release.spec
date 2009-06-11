%define repo free
#define repo nonfree

Name:           rpmfusion-%{repo}-release
Version:        11
Release:        90
Summary:        RPM Fusion (%{repo}) Repository Configuration

Group:          System Environment/Base
License:        BSD
URL:            http://rpmfusion.org
Source1:        rpmfusion-%{repo}.repo
Source2:        rpmfusion-%{repo}-updates.repo
Source3:        rpmfusion-%{repo}-updates-testing.repo
Source4:        rpmfusion-%{repo}-rawhide.repo
Source11:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-11-primary
Source12:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-12-primary
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       system-release >= %{version}

# If apt is around, it needs to be a version with repomd support
Conflicts:      apt < 0.5.15lorg3

%if %{repo} == "nonfree"
Requires:       rpmfusion-free-release >= %{version}

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
%{__install} -Dp -m644 %{SOURCE11} %{SOURCE12} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

# compatibility symlink for easy transition to F11
ln -s $(basename %{SOURCE11}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora

# Links for the keys
for i in i386 x86_64 ppc ppc64; do
  ln -s $(basename %{SOURCE11}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-11-${i}
  ln -s $(basename %{SOURCE12}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-12-${i}
  ln -s $(basename %{SOURCE11}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-latest-${i}
  ln -s $(basename %{SOURCE12}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-rawhide-${i}
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
* Thu Jun 11 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 11.90-1
- build for rawhide (enable rawhide, disable all the other repos)

* Sun May 17 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 11-1
- F11 release: disable rawhide, enable everything and updates
- use "metadata_expire=7d" for everything repos
- Track in some changes from 10-{34} (myself):
-- remove old comments to obsolete release packages from freshrpms, dribble and livna
-- add proper links for rawhide
-- add key for F12
-- some small adjustments to the spec
-- add post script that switch old config files from serverside mirrorlists to
   mirrormanager 
- Track in some changes from 10-{23} (Till Maas):
-- fix symlinks
-- allow easy transition to F11 with new gpg key and naming structure
- 

* Sun May 17 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 10-4
- add key for F12
- some small adjustments to the spec
- add post script that switch old config files from serverside mirrorlists to
  mirrormanager

* Sat May 16 2009 Till Maas <opensource@till.name> - 10-3
- fix symlinks

* Sat May 16 2009 Till Maas <opensource@till.name> - 10-2
- allow easy transition to F11 with new gpg key and naming structure



* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.90-3
- rebuild for new F11 features

* Sat Mar 21 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 10.90-2
- add new key for SHA256 signatures
- use the same structure for keys as fedora does

* Wed Nov 26 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 10.90-1
- Initial build for Fedora 11.

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

* Sat Sep 27 2008 Stewart Adam <s.adam at diffingo.com> - 9-7
- Use temporary mirrorlists for now, and baseurl for the debug & source repos

* Thu Sep 18 2008 Stewart Adam <s.adam at diffingo.com> - 9-6
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

