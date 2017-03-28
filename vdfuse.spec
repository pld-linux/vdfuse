# TODO
# - split VirtualBox spec to -libs and -devel so this package could be built
%define		virtualbox_version 5.1.18
Summary:	A FUSE module for mounting VirtualBox disk images (VDI/VMDK/VHD) on the host
Name:		vdfuse
Version:	0.83
Release:	1
Epoch:		2
License:	GPL v3
Group:		Base/Kernel
URL:		http://forums.virtualbox.org/viewtopic.php?f=7&t=17574
Source0:	VirtualBox-%{virtualbox_version}-include-only.tar.bz2
# Source0-md5:	a47cca26712ba293567f55c6b0a9683b
Source1:	%{name}-%{version}.c
# Source1-md5:	9185cc68b7b5227694e295d814b77d36
# https://bugs.launchpad.net/ubuntu/+source/virtualbox-ose/+bug/759988
Patch0:		%{name}-ebr.patch
BuildRequires:	VirtualBox
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program presents a virtual disk as a Filesystem in User Space
(FUSE). The separate partitions appear as block files Partition1, ...
under the mount point. You can then mount any or all of the partitions
as a Loop Device. If you use the readonly flag then these files are
readonly and the partitions themselves can only be mounted readonly.

NB: you will need to add "user_allow_other" to /etc/fuse.conf

%prep
%setup -q -n VirtualBox-%{virtualbox_version}
%{__cp} %{SOURCE1} .
%patch0 -p0

%build
export LD_LIBRARY_PATH=%{_libdir}/VirtualBox
FUSE_CFLAGS=$(pkg-config --cflags --libs fuse)
%{__cc} %{name}-%{version}.c -o %{name} \
	$FUSE_CFLAGS \
	-I./include \
	-Wl,-rpath,%{_libdir}/VirtualBox \
	%{_libdir}/VirtualBox/VBoxDD.so \
	%{_libdir}/VirtualBox/VBoxDD2.so \
	%{_libdir}/VirtualBox/VBoxDDU.so \
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
