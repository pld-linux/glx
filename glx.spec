%define		mesa_version	3.1
Summary:	Utah-GLX modules and libraries
Summary(pl):	Moduły i biblioteki Utah-GLX
Name:		glx
Version:	20000407
Release:	1
Copyright:	Custom
Group:		X11/Libraries
Group(de):	X11/Libraries
Group(es):	X11/Bibliotecas
Group(pl):	X11/Biblioteki
Source0:	%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.mesa3d.org/mesa/MesaLib-%{mesa_version}.tar.bz2
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-no_glut_headers.patch
URL:		http://utah-glx.sourceforge.net
Requires:	XFree86 >= 3.3.5
Provides:	OpenGL 
BuildRequires:	XFree86-devel
BuildRequires:	perl	
BuildRequires:	tcl	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Utah-GLX is a module providing GLX protocol support to XFree 3.3.x.
The package contains also OpenGL libraries making use of it. Hardware
acceleration for following chipsets is supported:
 - nVidia's Riva 128, Riva TNT and Riva TNT2
 - Matrox's G200 and G400
 - ATI's 3D Rage Pro
 - i810
 - S3 ViRGE
 - SiS 6326

%description -l pl
Utah-GLX jest modułem implementującym protokół GLX dla XFree 3.3.x
Pakiet zawiera także biblioteki OpenGL wykożystujące GLX. Sprzętowa
akceleracja jest obsługiwana dla następujących układów:
 - nVidia's Riva 128, Riva TNT oraz Riva TNT2
 - Matrox's G200 and G400
 - ATI's 3D Rage Pro
 - i810
 - S3 ViRGE
 - SiS 6326

%package devel
Summary:	Development environment for Utah-GLX
Summary(pl):	Środowisko programistyczne Utah-GLX
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Provides:	Mesa-devel

%description devel
Header files and documentation needed for development.

%description -l pl devel
Pliki nagłówkowe i dokumentacja do Utah-GLX.

%prep
%setup -q -a 1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{rpmcflags}" \
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
	
%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}/modules,%{_sysconfdir}/X11}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf docs/{README.*,*.txt} CHANGELOG README LICENSE New-Bugs \
	Bugs-ToDo HISTORY
	
%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz 
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/modules/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/X11/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_includedir}/*
