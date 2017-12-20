# psycopg2 ships with its own required shared libraries
%global __requires_exclude_from site-packages/psycopg2
%global __provides_exclude_from site-packages/psycopg2

Name:           cloudify-management-worker
Version:        %{CLOUDIFY_VERSION}
Release:        %{CLOUDIFY_PACKAGE_RELEASE}%{?dist}
Summary:        Cloudify's Management Worker
Group:          Applications/Multimedia
License:        Apache 2.0
URL:            https://github.com/cloudify-cosmo/cloudify-manager
Vendor:         Gigaspaces Inc.
Packager:       Gigaspaces Inc.

BuildRequires:  python >= 2.7, python-virtualenv, openssl-devel, git
Requires:       python >= 2.7, postgresql95-libs
Requires(pre):  shadow-utils


%description
Cloudify's Management worker


%prep


%build
virtualenv /opt/mgmtworker/env
/opt/mgmtworker/env/bin/pip install --upgrade pip setuptools
/opt/mgmtworker/env/bin/pip install git+https://github.com/cloudify-cosmo/cloudify-rest-client
/opt/mgmtworker/env/bin/pip install git+https://github.com/cloudify-cosmo/cloudify-plugins-common
/opt/mgmtworker/env/bin/pip install git+https://github.com/cloudify-cosmo/cloudify-script-plugin
/opt/mgmtworker/env/bin/pip install git+https://github.com/cloudify-cosmo/cloudify-agent
/opt/mgmtworker/env/bin/pip install psycopg2
/opt/mgmtworker/env/bin/pip install --upgrade "${RPM_SOURCE_DIR}/plugins/riemann-controller"
/opt/mgmtworker/env/bin/pip install --upgrade "${RPM_SOURCE_DIR}/workflows"
rm /opt/mgmtworker/env/lib/python2.7/site-packages/zmq/tests/_test_asyncio.py


%install
mkdir -p %{buildroot}/opt/mgmtworker
mv /opt/mgmtworker/env %{buildroot}/opt/mgmtworker
mkdir -p %{buildroot}/var/log/cloudify/mgmtworker


%pre
groupadd -fr cfyuser
getent passwd cfyuser >/dev/null || useradd -r -g cfyuser -d /etc/cloudify -s /sbin/nologin cfyuser

%post

%preun
%postun

%files

%defattr(-,root,root)
/opt/mgmtworker

%attr(750,cfyuser,adm) /var/log/cloudify/mgmtworker
