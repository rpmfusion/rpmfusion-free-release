%global _repo free
#global _repo nonfree

Name:           rpmfusion-%{_repo}-release
Version:        8
Release:        0.2
Summary:        RPM Fusion (%{_repo}) Repository Configuration

License:        BSD
URL:            http://rpmfusion.org
Source0:        RPM-GPG-KEY-rpmfusion-%{_repo}-el-8
Source2:        rpmfusion-%{_repo}-updates.repo
Source3:        rpmfusion-%{_repo}-updates-testing.repo
Source5:        rpmfusion-%{_repo}-tainted.repo
Source6:        rpmfusion-%{_repo}-next.repo
Source7:        rpmfusion-%{_repo}-next-testing.repo
BuildArch:      noarch

Requires:       redhat-release >= %{version}
Requires:       epel-release >= %{version}


%if "%{_repo}" == "nonfree"
Requires:       rpmfusion-free-release >= %{version}

%description
RPM Fusion repository contains open source and other distributable software for
EL + EPEL. It is the merger of the Dribble, FreshRPMs and Livna repositories.

This package contains the RPM Fusion GPG key as well as Yum package manager
configuration files for RPM Fusion's "nonfree" repository, which holds
software that is not considered as Open Source Software according to the
Fedora packaging guidelines.
%else
%description
RPM Fusion repository contains open source and other distributable software for
EL + EPEL. It is the merger of the Dribble, FreshRPMs and Livna repositories.

This package contains the RPM Fusion GPG key as well as Yum package manager
configuration files for RPM Fusion's "free" repository, which holds only
software that is considered as Open Source Software according to the Fedora
packaging guidelines.
%endif

%package tainted
Summary:        RPM Fusion %{_repo} Tainted repo definition
Requires:       %{name} = %{version}-%{release}
%if "%{_repo}" == "free"
Obsoletes:      livna-release < 1:1-2
Provides:       livna-release = 1:1-2
%endif

%description tainted
This package provides the RPM Fusion %{_repo} Tainted repo definitions.

%package next
Summary:        RPM Fusion %{_repo} Next repo definition
Requires:       %{name} = %{version}-%{release}
Recommends:     (%{name}-next if centos-stream-release)

%description next
This package provides the RPM Fusion %{_repo} Next repo definitions.

%prep
echo "Nothing to prep"

%build
echo "Nothing to build"

%install
# Create dirs
install -d -m755 \
  %{buildroot}%{_sysconfdir}/pki/rpm-gpg  \
  %{buildroot}%{_sysconfdir}/yum.repos.d

# GPG Key
%{__install} -Dp -m644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

# Yum .repo files
%{__install} -p -m644 \
    %{SOURCE2} \
    %{SOURCE3} \
    %{SOURCE5} \
    %{SOURCE6} \
    %{SOURCE7} \
    %{buildroot}%{_sysconfdir}/yum.repos.d

%files
%config %{_sysconfdir}/pki/rpm-gpg/*
%config(noreplace) %{_sysconfdir}/yum.repos.d/rpmfusion-%{_repo}-updates*.repo

%files tainted
%config(noreplace) %{_sysconfdir}/yum.repos.d/rpmfusion-%{_repo}-tainted.repo

%files next
%config(noreplace) %{_sysconfdir}/yum.repos.d/rpmfusion-%{_repo}-next*.repo

%changelog
* Fri Jul 23 2021 Xavier Bachelot <xavier@bachelot.org> - 8-0.2
- Create sub-package for next repo

* Wed Jan 09 2019 Xavier Bachelot <xavier@bachelot.org> - 8-0.1
- Release for EL-8.

* Tue Jun 19 2018 Xavier Bachelot <xavier@bachelot.org> - 7-4
- Don't use $releasever, it's not expanding as expected on RHEL.

* Tue Jun 19 2018 Xavier Bachelot <xavier@bachelot.org> - 7-3
- Only include tainted repo definition in tainted sub-package.

* Mon Mar 19 2018 Xavier Bachelot <xavier@bachelot.org> - 7-2
- Create sub-package for tainted repo.

* Thu Sep 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 7-1
- Release for EL-7

* Tue Jun 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 6-1
- Release for EL-6

* Sun May 01 2011 Robert Scheck <robert@fedoraproject.org> 6-0.1
- Initial RPM release based on Thorsten Leemhuis' work for EL-5
