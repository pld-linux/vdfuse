# TODO
# - split VirtualBox spec to -libs and -devel so this package could be built
%define		virtualbox_version 4.1.8
Summary:	A FUSE module for mounting VirtualBox disk images (VDI/VMDK/VHD) on the host
Name:		vdfuse
Version:	8.2a
Release:	1
License:	GPL v3
Group:		Base/Kernel
URL:		http://forums.virtualbox.org/viewtopic.php?f=7&t=17574
Source0:	VirtualBox-%{virtualbox_version}-include-only.tar.bz2
# Source0-md5:	2444d8604cc628ff2b2fa17adf0d3e58
Source1:	%{name}-v82a.c
# Source1-md5:	0450afd90bf7157a4a3057431f635108
BuildRequires:	libfuse-devel
BuildRequires:	VirtualBox
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program presents a virtual disk as a Filesystem in User Space
(FUSE). The separate partitions appear as block files Partition1, ...
under the mount point. You can then mount any or all of the partitions
as a Loop Device. If you use the readonly flag then these files are
readonly and the partitions themselves can only be mounted readonly.

NB: you will need to add "user_allow_other" to /etc/fuse.conf

%prep
%setup -q -n VirtualBox-%{virtualbox_version}_OSE

%build
export LD_LIBRARY_PATH=%{_libdir}/VirtualBox
FUSE_CFLAGS=$(pkg-config --cflags --libs fuse)
%{__cc} %{SOURCE1} -o %{name} \
	$FUSE_CFLAGS \
	-I./include \
	-Wl,-rpath,%{_libdir}/VirtualBox \
	-l:%{_libdir}/VirtualBox/VBoxDD.so \
	-l:%{_libdir}/VirtualBox/VBoxDD2.so \
	-l:%{_libdir}/VirtualBox/VBoxDDU.so \
	-Wall %{rpmcflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
