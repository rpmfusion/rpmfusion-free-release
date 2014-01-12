%define repo free
#define repo nonfree

Name:           rpmfusion-%{repo}-release
Version:        21
Release:        0.1
Summary:        RPM Fusion (%{repo}) Repository Configuration

Group:          System Environment/Base
License:        BSD
URL:            http://rpmfusion.org
Source1:        rpmfusion-%{repo}.repo
Source2:        rpmfusion-%{repo}-updates.repo
Source3:        rpmfusion-%{repo}-updates-testing.repo
Source4:        rpmfusion-%{repo}-rawhide.repo
Source20:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-20-primary
Source21:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-21-primary
Source22:       RPM-GPG-KEY-rpmfusion-%{repo}-fedora-22-primary
BuildArch:      noarch

Requires:       system-release >= %{version}


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

# Create dirs
install -d -m755 \
  $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg  \
  $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

# GPG Key
%{__install} -Dp -m644 \
    %{SOURCE20} \
    %{SOURCE21} \
    %{SOURCE22} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

# compatibility symlink for easy transition to F11
ln -s $(basename %{SOURCE20}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora

# Avoid using basearch in name for the key. Introduced in F18
ln -s $(basename %{SOURCE20}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-20
ln -s $(basename %{SOURCE21}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-21
ln -s $(basename %{SOURCE22}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-22

# Links for the keys
ln -s $(basename %{SOURCE20}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-latest
ln -s $(basename %{SOURCE21}) $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-%{repo}-fedora-rawhide


# Yum .repo files
%{__install} -p -m644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d


%files
%{_sysconfdir}/pki/rpm-gpg/*
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%changelog
* Sun Jan 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 21-0.1
- Bump for Rawhide/F-21

* Sun Dec 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 20-1
- Update to f20 final

* Fri Jun 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 20-0.2
- Add key for Rawhide/F-21
- Spec file clean-up

* Mon Mar 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 20-0.1
- Build for Rawhide/F-20

* Thu Mar 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 19-0.4
- Fix GPG's key name

* Wed Mar 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 19-0.3
- Branch F-19

* Tue Jan 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 19-0.2
- Add key for Rawhide/F-20

* Mon Aug 20 2012 Nicolas Chauvet <kwizart@gmail.com> - 19-0.1
- Build for Rawhide/F-19

* Wed Aug 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 18-0.2
- Bump for Branched/F-18

* Fri May 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 18-0.1
- Build for Rawhide/F-18

* Fri May 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-1
- Update to final 17

* Tue Mar 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-0.5
- Bump

* Mon Feb 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-0.4
- Split to development/17
- Enable rpmfusion*-updates-testing

* Sat Feb 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-0.3
- Bump for branched F-17

* Sat Nov 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 17-0.1
- build for rawhide/F-17
- Drop key for F-15

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 16-1.2
- Fix compat key for F-15
- Fix Installation of F-17 key

* Thu Oct 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 16-1
- Add keys for Rawhide/F-17
- Build for F-16

* Sun Jun 05 2011 Thorsten Leemhuis <fedora at leemhuis.info> - 16.1
- build for rawhide/F-16

* Sat May 28 2011 Thorsten Leemhuis <fedora at leemhuis.info> - 15-1
- Add keys for Rawhide/F16
- Build for F-15

* Sat Oct 16 2010 Thorsten Leemhuis <fedora at leemhuis.info> - 14-0.4
- drop ppc
- add key for F-15, drop the one for F-13

* Sun Oct 10 2010 Thorsten Leemhuis <fedora at leemhuis.info> - 14-0.3
- branching for F14: disable rawhide, enable everything and updates

* Mon Apr 26 2010 Thorsten Leemhuis <fedora at leemhuis.info> - 14-0.2
- fix compatibility symlink

* Sat Apr 24 2010 Thorsten Leemhuis <fedora at leemhuis.info> - 14-0.1
- rebuild for rawhide

* Fri Apr 16 2010 Thorsten Leemhuis <fedora at leemhuis.info> - 13-1
- add key for Rawhide/F14
- remove key for F12

* Sun Nov 22 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 13-0.1
- Bump for Fedora 13's rawhide.
- Put the version at 13 from the start. 
- drop post script

* Sun Nov 15 2009 Thorsten Leemhuis <fedora at leemhuis.info> - 12-1
- F12 release: disable rawhide, enable everything and updates
- remove key for F11
- add key for F13

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

