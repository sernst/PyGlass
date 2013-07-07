; installer.nsi
; (C)2013
; Scott Ernst

!include "MUI2.nsh"
!include "x64.nsh"

;--------------------------------
;General

	; The name of the installer
	Name "##APP_NAME##"
	OutFile "##APP_NAME##_Installer.exe"

	; The default installation directory
	InstallDir "$PROGRAMFILES64\##APP_NAME##"

	; Registry key to check for directory (so if you install again, it will
	; overwrite the old one automatically)
	InstallDirRegKey HKLM "Software\##APP_GROUP_ID##_##APP_ID##" "Install_Dir"

	; Request application privileges for Windows Vista+
	RequestExecutionLevel admin

;--------------------------------
;Interface Settings

	!define MUI_ABORTWARNING

	;!define MUI_COMPONENTSPAGE_SMALLDESC ;No value
	!define MUI_INSTFILESPAGE_COLORS "FFFFFF 000000" ;Two colors

;--------------------------------
; Pages

	!insertmacro MUI_PAGE_COMPONENTS
	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_INSTFILES

	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

	!insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections
Section "##APP_NAME## (required)"

  SectionIn RO

  ; Install resource files
  SetOutPath "$LOCALAPPDATA\##APP_GROUP_ID##\##APP_ID##\resources"
  File /r "resources\*"

  ; Install application files and dependencies
  SetOutPath "$INSTDIR\##APP_NAME##"
  File /r "dist\*"

  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\##APP_GROUP_ID##_##APP_ID## "Install_Dir" "$INSTDIR"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\##APP_GROUP_ID##_##APP_ID##" "DisplayName" "##APP_NAME##"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\##APP_GROUP_ID##_##APP_ID##" "UninstallString" '"$INSTDIR\##APP_NAME##\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\##APP_GROUP_ID##_##APP_ID##" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\##APP_GROUP_ID##_##APP_ID##" "NoRepair" 1
  WriteUninstaller "##APP_NAME##\uninstall.exe"

SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcut"

  CreateDirectory "$SMPROGRAMS\##APP_NAME##"
  CreateShortCut "$SMPROGRAMS\##APP_NAME##\##APP_NAME##.lnk" "$INSTDIR\##APP_NAME##\##APP_NAME##.exe" "" "$INSTDIR\##APP_NAME##\##APP_NAME##.exe" 0
  CreateShortCut "$SMPROGRAMS\##APP_NAME##\Uninstall.lnk" "$INSTDIR\##APP_NAME##\uninstall.exe" "" "$INSTDIR\##APP_NAME##\uninstall.exe" 0

SectionEnd

; Optional section (can be disabled by the user)
Section "Desktop Shortcut"

	CreateShortcut "$DESKTOP\##APP_NAME##.lnk" "$INSTDIR\##APP_NAME##\##APP_NAME##.exe" "" "$INSTDIR\##APP_NAME##\##APP_NAME##.exe" 0

SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"

  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\##APP_NAME##"
  DeleteRegKey HKLM SOFTWARE\##APP_GROUP_ID##_##APP_ID##

  ; Remove files and uninstaller
  Delete "$INSTDIR\*.*"
  Delete "$LOCALAPPDATA\##APP_GROUP_ID##\##APP_ID##\resources\*.*"

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\##APP_NAME##\*.*"

  ; Remove desktop shortcut if it exists
  Delete "$DESKTOP\##APP_NAME##.lnk"

  ; Remove directories used
  RMDir /r "$INSTDIR"

  RMDir /r "$LOCALAPPDATA\##APP_GROUP_ID##\##APP_ID##\resources"

  RMDir "$SMPROGRAMS\##APP_NAME##"

SectionEnd
