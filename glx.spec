# $Revision $, $Date $
%define		mesa_version	3.1
Summary:	Utah-GLX modules and libraries
Name:		glx
Version:	20000407
Release:	1
Copyright:	Custom
Group:		X11/Libraries
Source:		%{name}-%{version}.tar.bz2	
Source1:	ftp://ftp.mesa3d.org/mesa/MesaLib-%{mesa_version}.tar.bz2
Patch0:		glx-DESTDIR.patch
URL:		http://utah-glx.sourceforge.net
Requires:	XFree86 >= 3.3.5
Provides:	Mesa = %{mesa_version}
BuildRequires:	XFree86-devel
BuildRequires:	perl	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Utah-GLX is a module providing GLX protocol support to XFree 3.3.x.
The package contains also OpenGL libraries making use of it.
Hardware acceleration for following chipsets is supported:
	- nVidia's Riva 128, Riva TNT and Riva TNT2
	- Matrox's G200 and G400
	- ATI's 3D Rage Pro
	- i810
	- S3 ViRGE
	- SiS 6326

%description -l pl
Utah-GLX jest modu³em implementuj±cym protokó³ GLX dla XFree 3.3.x
Pakiet zawiera tak¿e biblioteki OpenGL wyko¿ystuj±ce GLX.
Sprzêtowa akceleracja jest obs³ugiwana dla nastêpuj±cych uk³adów:
	- nVidia's Riva 128, Riva TNT oraz Riva TNT2
	- Matrox's G200 and G400
	- ATI's 3D Rage Pro
	- i810
	- S3 ViRGE
	- SiS 6326

%prep
%setup -q -a 1
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" \
./autogen.sh \
	--prefix=%{_prefix} \
	--with-mesa="./Mesa-%{mesa_version}" \
	--sysconfdir=%{_sysconfdir}/X11 \
	--disable-agp \
	--enable-GLU \
	--disable-glut \
%ifarch %{ix86} \
	--with-x86-asm="yes" \
  %ifarch i686 \
	--with-mmx-asm="yes" \
	--with-3dnow-asm="no" \
    	--enable-mtrr \
  %else \
    %ifarch k6 \
	--with-mmx-asm="yes" \
	--with-3dnow-asm="yes" \
    %else \
	--with-mmx-asm="no" \
	--with-3dnow-asm="no" \
    %endif \
    	--disable-mtrr \
  %endif \
%else \
	--with-x86-asm="no" \
	--with-mmx-asm="no" \
	--with-3dnow-asm="no" \
    	--disable-mtrr \
%endif
	
make depend
make

%install

install -d  $RPM_BUILD_ROOT/usr/X11R6/{include,lib/modules}

make install DESTDIR="$RPM_BUILD_ROOT"

gzip -9nd docs/{README.*,*.txt} CHANGELOG README LICENSE New-Bugs \
	Bugs-ToDo HISTORY || :
	
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz 
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/modules/*
