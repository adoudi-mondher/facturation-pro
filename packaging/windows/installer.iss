; Script Inno Setup pour Easy Facture
; Version 1.7.0
; Par Mondher ADOUDI - Sidr Valley AI

#define MyAppName "Easy Facture"
#define MyAppVersion "1.7.0"
#define MyAppPublisher "Sidr Valley AI"
#define MyAppURL "https://easyfacture.mondher.ch"
#define MyAppExeName "EasyFacture.exe"
#define MyAppContact "adoudi@mondher.ch"

[Setup]
; Informations de base
AppId={{A7B8C9D0-1234-5678-90AB-CDEF12345678}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppContact={#MyAppContact}

; Dossiers d'installation
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Sortie
OutputDir=output
OutputBaseFilename=EasyFacture-Setup-v{#MyAppVersion}
SetupIconFile=..\..\icons\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=2

; Mode
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

; Licence et informations
LicenseFile=..\..\LICENSE.txt

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Application complète (sauf dossier data qui contient la base de données utilisateur)
Source: "dist\EasyFacture\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "data\*"
; NOTE: Ne pas utiliser "Flags: ignoreversion" sur les fichiers système

[Icons]
; Icônes menu démarrer
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Désinstaller {#MyAppName}"; Filename: "{uninstallexe}"
; Icône bureau (optionnelle)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Lancer l'application après installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Supprimer les fichiers temporaires lors de la désinstallation
Type: filesandordirs; Name: "{app}\data\.last_api_check"
Type: filesandordirs; Name: "{app}\logs"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  OldVersion: String;
begin
  Result := True;

  // Vérifier si une ancienne version est installée
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1',
    'DisplayVersion', OldVersion) then
  begin
    if MsgBox('Une version précédente d''Easy Facture (' + OldVersion + ') est installée.' + #13#10 +
              'Voulez-vous la désinstaller avant de continuer ?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Lancer la désinstallation de l'ancienne version
      if not Exec(ExpandConstant('{uninstallexe}'), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode) then
      begin
        MsgBox('Erreur lors de la désinstallation de l''ancienne version.', mbError, MB_OK);
        Result := False;
      end;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Créer le dossier data s'il n'existe pas déjà
    if not DirExists(ExpandConstant('{app}\data')) then
      CreateDir(ExpandConstant('{app}\data'));
  end;
end;

[Messages]
; Messages personnalisés
WelcomeLabel1=Bienvenue dans l'assistant d'installation d'[name/ver]
WelcomeLabel2=Ceci installera [name/ver] sur votre ordinateur.%n%nIl est recommandé de fermer toutes les autres applications avant de continuer.
