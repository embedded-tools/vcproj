import os, sys, binascii
from shutil import copyfile



def main():    
    
    #command line arguments:
    #  /exe (default)
    #  /lib
    #  projectName
    srcDir    = '.\\';    
    outputExe  = True;
    outputLib  = False;
    outputDll  = False;
    includeAdd = False;
    mocDir     = "";
    projectDir = srcDir;
    projectName = "Unnamed";
    mixFiles   = False;
    winNaming  = True;
    embNaming  = False;
    
    cfgType = 1;
    
    if (len(sys.argv)==1):
        print("");
        print("vcproj (c) 2021 Ondrej Sterba, osterba@atlas.cz");
        print("       (visual studio project generator)       ");
        print("");
        print('Command line arguments:');
        print('  /exe  - executable project');
        print('  /dll  - dynamic library project');
        print('  /lib  - static library project');
        print('  (choose just one from those three)');
        print('  ----------------------------------');
        print("  /incl - adds all header directories into project settings");
        print("  /mix  - dont separate header files and source files");
        print("  /win  - windows naming conventions");
        print("  /emb  - embedded systems naming conventions");
        print('  /moc:filepath - directory with qt moc_* files');
        print('  ----------------------------------');
        print("  projectname   - last parameter is a project name");        
        print("  -----------------------------------'");
        print("  Examples how to use vcproj.py:");
        print("  vcproj.py");      
        print("    -shows this help");
        print("  vcproj.py test");
        print("    -generates test.vcproj executable project file with default settings");
        print("  vcproj.py /lib test");       
        print("    -generates static library project named test.vcproj");
        print("  vcproj.py /dll /target:.\\ide\\vs2008");
        print("    -generates dll project and stores it into ide\\vs2008 directory");
        print("  vcproj.py /lib /moc:.\\build myproject");
        print("    -generates static lib and also adds Qt MOC files into project");
        print("  vcproj.py /lib /src:.\\lib_test /moc:.\\build");
        print("    -generates static lib, source codes from lib_test directory, qt moc files are read from .\\build directory");        
        return;
    
    
    first = True;
    for arg in sys.argv:
        if not first:
            if (arg.startswith('/')):
                if (arg.startswith('/src:')):
                    srcDir = arg[5:];
                    if (not srcDir.endswith('\\')):
                        srcDir = srcDir + '\\';
                if (arg.startswith('/target:')):
                    projectDir = arg[8:];
                    if (not projectDir.endswith('\\')):
                        projectDir = projectDir + '\\';
                if (arg=="/exe"):
                    outputExe = True;
                    cfgType = 1;
                if (arg=='/lib'):
                    outputLib = True;
                    cfgType = 4;
                if (arg=='/dll'):
                    outputDll = True;
                    cfgType = 2;
                if (arg=="/incl"):
                    includeAdd = True;
                if (arg=="/mix"):
                    mixFiles = True;                    
                if (arg=="/win"):
                    winNaming = True;
                    embNaming = False;
                if (arg=="/emb"):
                    embNaming = True;
                    winNaming = False;
                if (arg.startswith('/moc:')):
                    mocDir = arg[5:];
            else:
                projectName = arg;
        first = False;

    #debugging commands:

    
    #end of debugging commands    
    if (outputExe==False) and (outputLib==False) and (outputDll == False):
        outputExe=True;
        
    if (outputExe):
        cfgType = 1;
    if (outputLib):
        cfgType = 4;
    if (outputDll):
        cfgType = 2;
    
    if (len(srcDir) > 0):
        if (srcDir[-1]!='\\'):
            srcDir = srcDir + '\\';
            
    if (len(projectDir) > 0):
        if (projectDir[-1]!='\\'):
            projectDir = projectDir + '\\';
            
    if (len(mocDir) > 0):
        if (mocDir[-1]!='\\'):
            mocDir = mocDir + '\\';
            
    projectFile = projectName + ".vcproj";
    if (outputExe==True):
       outputFile = projectName + ".exe"
    if (outputLib==True):
        outputFile = projectName + ".lib"
    if (outputDll==True):
        outputFile = projectName + ".dll"
                
    #searhing for include directories
    dirs = [""];
    if (includeAdd):
        print("Scanning headers in ...");
        scanheaders(srcDir, dirs);
    
    #serching result is written to includeDirs variable
    includeDirs = "";
    first = True;
    basedir = "$(ProjectDir)";
    for dir in dirs:
        if not first:
            includeDirs = includeDirs + ";";
        if (len(dir)==0):
            includeDirs = includeDirs + basedir;
        else:
            includeDirs = includeDirs + basedir + dir[1:];
        first = False;
    
    includeLibs = "";
    includeLibDirs = ".\\libs";

    guid = "{";
    guid = guid + os.urandom(4).hex().upper() + '-';
    guid = guid + os.urandom(2).hex().upper() + '-';
    guid = guid + os.urandom(2).hex().upper() + '-';
    guid = guid + os.urandom(2).hex().upper() + '-';
    guid = guid + os.urandom(6).hex().upper() + '}';
                
    projectFile = projectDir + projectFile;      
            
    f = open(projectFile, "w+");   
    f.write('<VisualStudioProject\n');
    f.write('	ProjectType="Visual C++"\n');
    f.write('   Version="9.00"\n');
    f.write('   Name="' + projectName + '"\n');
    f.write('   ProjectGUID="' + guid + '"\n');
    f.write('   RootNamespace="' + projectName +'"\n');
    f.write('   Keyword="Win32Proj"\n');
    f.write('   TargetFrameworkVersion="196613">\n');
    f.write('   <Platforms>\n');
    f.write('   	<Platform Name="Win32" />\n');
    f.write('   </Platforms>\n');
    f.write('   <ToolFiles>\n');
    f.write('   </ToolFiles>\n');
    f.write('   <Configurations>\n');
    f.write('       <Configuration\n');
    f.write('           Name="Debug|Win32"\n');
    if (winNaming):
        f.write('           OutputDirectory="$(ProjectDir)\\$(ConfigurationName)"\n');
        f.write('           IntermediateDirectory="$(ProjectDir)\\$(ConfigurationName)\\obj"\n');
    if (embNaming):
        f.write('           OutputDirectory="$(ProjectDir)\\bin"\n');
        f.write('           IntermediateDirectory="$(ProjectDir)\\obj"\n');        
    f.write('           ConfigurationType="' + str(cfgType) + ' "\n');
    f.write('           CharacterSet="1">\n');
    f.write('           <Tool\n');
    f.write('               Name="VCCLCompilerTool"\n');
    f.write('               Optimization="0"\n');
    f.write('               AdditionalIncludeDirectories="' + includeDirs + '"\n');
    f.write('               PreprocessorDefinitions="WIN32;_DEBUG;_WINDOWS;_CRT_SECURE_NO_WARNINGS"\n');
    f.write('               MinimalRebuild="true"\n');
    f.write('               BasicRuntimeChecks="3"\n');
    f.write('               RuntimeLibrary="1"\n');
    f.write('               UsePrecompiledHeader="0"\n');
    f.write('               WarningLevel="3"\n');
    f.write('               DebugInformationFormat="4" />\n');
    f.write('           <Tool\n');
    f.write('               Name="VCLinkerTool"\n');
    f.write('               AdditionalDependencies="' + includeLibs + '"\n');
    f.write('               OutputFile="$(OutDir)\\' + outputFile + '"\n');
    f.write('               LinkIncremental="2"\n');
    f.write('               AdditionalLibraryDirectories="' + includeLibDirs + '"\n');
    f.write('               GenerateDebugInformation="true"\n');
    f.write('               SubSystem="2"\n');
    f.write('               TargetMachine="1" />\n');
    f.write('       </Configuration>\n');
    f.write('       <Configuration\n');
    f.write('           Name="Release|Win32"\n');
    if (winNaming):
        f.write('           OutputDirectory="$(ProjectDir)\\$(ConfigurationName)"\n');
        f.write('           IntermediateDirectory="$(ProjectDir)\\$(ConfigurationName)\\obj"\n');
    if (embNaming):
        f.write('           OutputDirectory="$(ProjectDir)\\bin"\n');
        f.write('           IntermediateDirectory="$(ProjectDir)\\obj"\n');        
    f.write('           ConfigurationType="' + str(cfgType) + '"\n');
    f.write('           CharacterSet="1"\n');
    f.write('           WholeProgramOptimization="1">\n');
    f.write('			<Tool\n');
    f.write('               Name="VCCLCompilerTool"\n');
    f.write('               Optimization="2"\n');
    f.write('               AdditionalIncludeDirectories="' + includeDirs + '"\n');
    f.write('               EnableIntrinsicFunctions="true"\n');
    f.write('               PreprocessorDefinitions="WIN32;NDEBUG;_WINDOWS;_CRT_SECURE_NO_WARNINGS"\n');
    f.write('               RuntimeLibrary="2"\n');
    f.write('               EnableFunctionLevelLinking="true"\n');
    f.write('               UsePrecompiledHeader="0"\n');
    f.write('               WarningLevel="3"\n');
    f.write('               DebugInformationFormat="3" />\n');
    f.write('           <Tool\n');
    f.write('               Name="VCLinkerTool"\n');
    f.write('               LinkIncremental="1"\n');
    f.write('               GenerateDebugInformation="true"\n');
    f.write('               SubSystem="2"\n');
    f.write('               OptimizeReferences="2"\n');
    f.write('               EnableCOMDATFolding="2"\n');
    f.write('               TargetMachine="1" />\n');
    f.write('       </Configuration>\n');    
    f.write('   </Configurations>\n');
    f.write('   <Files>\n');
    
    print("Project directory: " + projectDir);
    print("Source code directory: " + srcDir);
    if (len(mocDir) > 0):
        print("Meta-object-class directory: " + mocDir);
    
    baseDir = os.path.relpath(srcDir, projectDir);    
    if (len(baseDir)>0):
        if (baseDir[-1]!='\\'):
            baseDir = baseDir + '\\';
            
    os.chdir(projectDir);
                        
    #searching for moc files and copying them to source files
    if (len(mocDir)>0):
        mocDir  = os.path.relpath(mocDir, projectDir);    
    
    if (len(mocDir) > 0):
        if (mocDir[-1]!='\\'):
            mocDir = mocDir + '\\';
            
    mocFiles = {};   
    if (len(mocDir)>0):
        print("Scanning qt Meta-Object-Class files...");
        scanmocfiles(mocDir, mocFiles);

    print("Scanning source files...");
    if (mixFiles == True):        
        scansources(f, baseDir, mocFiles, {'.c', '.cpp', '.h', '.hpp'}, '    ');
    else:
        tabs = '    ';
        f.write(tabs+'<Filter\n'+tabs+'    Name="Header Files"\n'+tabs+'    >\n');        
        scansources(f, baseDir, mocFiles, {'.h', '.hpp'}, '        ');
        f.write(tabs+"</Filter>\n");
        f.write(tabs  +'<Filter\n'+tabs+'    Name="Resource Files"\n'+tabs+'    >\n');        
        scansources(f, baseDir, mocFiles, {'.bmp', '.ico', '.png', '.ico', '.jpg', '.jpeg'}, '        ');
        f.write(tabs+"</Filter>\n");
        f.write(tabs+'<Filter\n'+tabs+'    Name="Source Files"\n'+tabs+'    >\n');        
        scansources(f, baseDir, mocFiles, {'.c', '.cpp', '.s', '.txt', '.ico'}, '        ');
        f.write(tabs+"</Filter>\n");
        
    f.write('   </Files>\n');
    f.write('</VisualStudioProject>\n');
    f.close();    
    print("Project file created.");
    

def scanmocfiles(relpath, dirs):
    with os.scandir(relpath) as entries:
        for entry in entries:
            if (entry.is_dir()):
                if not (entry.name.startswith('.')):
                    scanmocfiles(relpath+entry.name+"\\", dirs);
            elif (entry.is_file()):         
                if (entry.name.startswith('moc_')):
                        name = entry.name[4:];
                        dirs[name] = relpath + entry.name;


def scanheaders(relpath, dirs):
    with os.scandir(relpath) as entries:
        for entry in entries:
            if (entry.is_dir()):
                if not (entry.name.startswith('.')):
                    scanheaders(relpath+entry.name+"\\", dirs);
            elif (entry.is_file()):         
                if (entry.name.endswith('.h')) or (entry.name.endswith('.hpp')):
                    if (not (relpath in dirs)):
                        dirs.append(relpath);

def filecount(path, extensions):
    count = 0;
    with os.scandir(path) as entries:
        for entry in entries:
            if (entry.is_dir()):
                count = count + filecount(path+entry.name+"\\", extensions);
            else:                             
                fileextpos = entry.name.rfind('.');
                fileext = entry.name[fileextpos:].lower();
                if (fileext in extensions):
                    count = count + 1;
    return count;
        
    
def scansources(projectFile, relpath, mocfiles, extensions, tabs):
    with os.scandir(relpath) as entries:        
        mocs  = {};
        files = [];
        #scanning src files and moc files
        for entry in entries:
            if (entry.is_dir()):
                if not (entry.name.startswith('.')):
                    if (filecount(relpath+entry.name+"\\", extensions)>0):                    
                        projectFile.write(tabs+'<Filter\n'+tabs+'    Name="' + entry.name + '"\n'+tabs+'    >\n');
                        scansources(projectFile, relpath+entry.name+"\\", mocfiles, extensions, tabs + "    ");
                        projectFile.write(tabs+"</Filter>\n");
                    #end if
            elif (entry.is_file()):      
                fileextpos = entry.name.rfind('.');
                fileext = entry.name[fileextpos:].lower();
                if (fileext in extensions):
                    files.append(relpath + entry.name);
                    if (entry.name in mocfiles.keys()):
                        mocs[entry.name] = mocfiles[entry.name];
                        
        #adding moc files to project file
        if (len(mocs)>0):
            projectFile.write(tabs+'<Filter\n'+tabs+'    Name=".moc"\n'+tabs+'    >\n');
            newdir = relpath + '.moc';
            if (not os.path.isdir(newdir)):
                os.mkdir(newdir);
            for mockey in mocs.keys():
                moc_copy = newdir+ '\\moc_' + mockey;
                copyfile(mocfiles[mockey], moc_copy);
                projectFile.write(tabs+'    <File\n' +tabs+ '        RelativePath="' + moc_copy + '"\n' + tabs +'        >\n' +tabs+ '        </File>\n');
            projectFile.write(tabs+"</Filter>\n");
            
        #adding src files to project file 
        if (len(files)>0):
            for file in files:
                projectFile.write(tabs+'<File\n' +tabs+ '    RelativePath="' + file + '"\n' + tabs +'    >\n' +tabs+ '</File>\n');
        #done
            
if __name__ == "__main__":
  main()