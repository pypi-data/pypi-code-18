# charset=utf-8

from uuid import uuid3, UUID
from collections import namedtuple as nt
from xml.sax.saxutils import escape as xml_escape
import re

_Shortcut = nt('Shortcut', ['name', 'directory', 'icon_source_path', 'arguments'])
class Shortcut(_Shortcut):
    def __new__(cls, name, directory, icon_source_path, arguments=''):
        return _Shortcut.__new__(cls, name, directory, icon_source_path, arguments)

class InstallFile(nt('InstallFile', ['dest_path', 'source_path', 'shortcuts'])):
    '''
        dest_path - Path under root directory..
        source_path - Path relative to the wxs to get source file from.
        shortcuts - List of Shortcuts
    '''
    def __new__(cls, dest_path, source_path, shortcuts = []):
        return super(InstallFile, cls).__new__(cls, dest_path, source_path, shortcuts)
    
class IniAddLine(nt('IniAddLine', ['path', 'section', 'key', 'value'])): pass
    
def escape(name):
    if not isinstance(name, unicode):
        name = unicode(name, 'utf-8')
    chars = [ ]
    for c in name:
        if not c.isalnum():
            chars.extend(['_'] + list('%05x' % ord(c)))
        else:
            chars.append(c)
    id = ''.join(chars)
    if len(id) > 72:
        id = id[:56] + ('%016x' % (abs(hash(id)),))
    return id

def shorten(str):
    if len(str) > 53:
        return str[:53-16] + ('%016x' % (abs(hash(str)),))
    else:
        return str

def make_wix(guid, manufacturer, name, version, files, bits=32):
    '''
        guid - GUID of product.
        manufacturer - Manufacturer of product.
        name - Name of product.
        version - Version in form a.b.c (eg 1.23.6)
        files - List of InstallFiles (see InstallFile).
        bits - 32 or 64
    '''
    platform = 'x64' if bits == 64 else 'x86'
    
    for file in files:
        if not (isinstance(file, InstallFile) or isinstance(file, IniAddLine)):
            raise TypeError('Files must be list of InstallFile or IniAddLine; found %s.' % (type(file),))
    
    ini_lines = set([])
    for file in files:
        if isinstance(file, IniAddLine):
            line = (file.path, file.section, file.key)
            if line in ini_lines:
                raise ValueError('Duplicate INI line %s %s:%s' % line)
            ini_lines.add(line)
    
    guid = UUID(str(guid))
    
    upgrade_guid = uuid3(uuid3(guid, 'special'), 'upgrade')

    product_name = name
    
    def file_tokens(file):
        return re.split(r'[/\\]', file)
    
    def file_id(file):
        if file.startswith('/') or file.startswith('\\'): file = file[1:]
        if file == 'SourceDir':
            return 'TARGETDIR'
        elif file == 'SourceDir/PFiles':
            if bits == 32:
                return 'ProgramFilesFolder'
            elif bits == 64:
                return 'ProgramFiles64Folder'
            else:
                raise ValueError('Bits is not 32 or 64')
        elif file == 'SourceDir/PFiles/ApplicationRoot':
            return 'APPLICATIONROOTDIRECTORY'
        elif file == 'SourceDir/Desktop':
            return 'DesktopFolder'
        else:
            return shorten(escape('/'.join(map(str, file_tokens(file)))))
    
    def source_id(source_path):
        return shorten('SRC' + escape('/'.join(map(str, file_tokens(source_path)))))
    
    def file_parent(file):
        return '/'.join(file_tokens(file)[:-1])
    
    # <Directory Id="c" Name="c"/>
    directories = { }
    def touch_in(search_in, tokens):
        if len(tokens) > 0:
            if tokens[0] not in search_in:
                search_in[tokens[0]] = { }
            touch_in(search_in[tokens[0]], tokens[1:])
    def touch(tokens):
        touch_in(directories, tokens)
    
    for file in files:
        if isinstance(file, InstallFile):
            touch(file_tokens(file.dest_path)[:-1])
            for shortcut in file.shortcuts:
                touch(file_tokens(shortcut.directory))
        elif isinstance(file, IniAddLine):
            touch(file_tokens(file.path)[:-1])
    
    def declare_directories_in(full_path, root):
        children = [ ]
        for file_name in root.keys():
            next_full_path = full_path+'/'+file_name
            child_declarations = declare_directories_in(next_full_path, root[file_name])
            id = file_id(next_full_path)
            wix_name = name if next_full_path in ['SourceDir/PFiles/ApplicationRoot', '/SourceDir/PFiles/ApplicationRoot'] else file_name
            children.append(
                '''<Directory Id="{id}" Name="{name}">\n{child_declarations}</Directory>\n'''.format(id=id, child_declarations=child_declarations, name=wix_name)
            )
        return ''.join(children)
    
    directory_declarations = declare_directories_in('', directories)
    
    # <DirectoryRef Id="APPLICATIONROOTDIRECTORY">
    #     <Component Id="ATXT" Guid="62259BEC-902D-4D16-A9B3-D37771A36CF5">
    #         <File Id="ATXT" Source="tree/a.txt" KeyPath="yes"/>
    #     </Component>
    # </DirectoryRef>
    component_ids = [ ]
    component_declarations = [ ]
    for file in files:
        if isinstance(file, InstallFile):
            dir = file_id(file_parent(file.dest_path))
            id = file_id(file.dest_path)
            component_guid = uuid3(uuid3(guid, 'files'), unicode(file.dest_path).encode('utf-8'))
            component_ids.append(id)
            
            source = file.source_path
                    
            shortcut_xml = ''
            for shortcut in file.shortcuts:
                dot_i = file.dest_path.rfind('.')
                if dot_i != -1:
                    ext = file.dest_path[dot_i:]
                else:
                    ext = ''
                if not (ext == '.exe' or ext == '.ico'):
                    raise ValueError("Can't associate icon with extension '" + ext + "'")
                icon_id = source_id(shortcut.icon_source_path) + ext
                shortcut_id = file_id(file.dest_path+'/shortcut/'+shortcut.name)
                shortcut_dir = file_id(shortcut.directory)
                shortcut_xml += '''<Shortcut 
                            Id="{shortcut_id}"
                            Directory="{shortcut_dir}"
                            Icon="{icon_id}"
                            Advertise="yes"
                            Name="{name}"
                            {arguments}
                            WorkingDirectory="{dir}">
                            <Icon Id="{icon_id}" SourceFile="{icon_source}"/>
                            </Shortcut>\n'''.format(shortcut_id=shortcut_id, shortcut_dir=shortcut_dir, icon_id=icon_id, icon_source=shortcut.icon_source_path, name=shortcut.name, arguments='Arguments="'+shortcut.arguments+'"' if len(shortcut.arguments)>0 else '', dir=dir)
                
            component_declarations.append('''
                <DirectoryRef Id="{dir}">
                    <Component Id="{id}" Guid="{component_guid}" Win64="{win64}">
                        <File Id="{id}" Source="{source}" Name="{name}" KeyPath="yes">
                            {shortcut_xml}
                        </File>
                    </Component>
                </DirectoryRef>
              '''.format(dir=dir, id=id, component_guid=component_guid, source=source, name=file_tokens(file.dest_path)[-1], shortcut_xml=shortcut_xml, win64=('yes' if bits==64 else 'no')))
            
        elif isinstance(file, IniAddLine):
            dir = file_id(file_parent(file.path))
            id = file_id(file.path+'/'+file.section+'/'+file.key)
            ini_id = file_id(file.path+'/'+file.section+'/'+file.key+'/file')
            component_guid = str(uuid3(uuid3(guid, 'files'), unicode(id).encode('utf-8')))
            component_ids.append(id)
            
            # http://stackoverflow.com/questions/16990759/wix-modify-an-existing-ini-file
            component_declarations.append('''
                <Component Id="{id}" Guid="{component_guid}" Directory="{dir}">
                    <CreateFolder/>
                    <IniFile
                        Id="{ini_id}"
                        Action="addLine"
                        Directory="{dir}"
                        Name="{name}"
                        Section="{section}"
                        Key="{key}"
                        Value="{value}"
                    />
                </Component>
              '''.format(id=xml_escape(id), component_guid=xml_escape(component_guid), ini_id=xml_escape(ini_id), dir=xml_escape(dir), name=xml_escape(file_tokens(file.path)[-1]), section=xml_escape(file.section), key=xml_escape(file.key), value=xml_escape(file.value))
            )
            
        else:
            raise TypeError
    
    component_declarations = '\n'.join(component_declarations)
    
    # <ComponentRef Id="ATXT"/>
    # <ComponentRef Id="BTXT"/>
    # <ComponentRef Id="CTXT"/>
    feature_components = [ ]
    for component_id in component_ids:
        feature_components.append('<ComponentRef Id="{component_id}"/>'.format(component_id=component_id))
    feature_components = '\n'.join(feature_components)

    return '''<?xml version="1.0" encoding="utf-8"?>

<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product 
        Name="{name}"
        Id="*"
        UpgradeCode="{upgrade_guid}"
        Language="1033"
        Codepage="1252"
        Version="{version}"
        Manufacturer="{manufacturer}">
        
        <Package
            Id="*"
            Keywords="Installer"
            Description="{name} Installer"
            InstallerVersion="200"
            Languages="1033"
            Compressed="yes"
            Platform="{platform}"
            SummaryCodepage="1252"/>
        
        <Property Id="PREVIOUSVERSIONSINSTALLED" Secure="yes"/>
        
        <Upgrade Id="{upgrade_guid}">
           <UpgradeVersion
              Minimum="1.0.0.0" Maximum="99.0.0.0"
              Property="PREVIOUSVERSIONSINSTALLED"
              IncludeMinimum="yes" IncludeMaximum="no"/>
        </Upgrade>  
        
        <Media Id='1' Cabinet='Everything.cab' EmbedCab='yes'/>
        
        {directory_declarations}
        
        {component_declarations}
        
        <Feature Id="MainApplication" Title="Main Application" Level="1">
            {feature_components}
        </Feature>

        <InstallExecuteSequence>
            <RemoveExistingProducts Before="InstallInitialize"/> 
        </InstallExecuteSequence>
    </Product>
</Wix>
'''.format(name=name, manufacturer=manufacturer, version=version, guid=guid, upgrade_guid=upgrade_guid, directory_declarations=directory_declarations, component_declarations=component_declarations, feature_components=feature_components, platform=platform)

