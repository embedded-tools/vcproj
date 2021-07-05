# vcproj
Visual Studio Project Creator

Sometimes you need to create visual studio project from existing source code files. It can be easy if project contains few files, but it can be time consuming if project contains few hundred or even few thounands source code files.

This tool creates Visual Studio 2008 project and adds all source code files into project definition.

Standard project in Visual studio looks like:

<Project name>
   -Header Files
   -Resource Files
   -Source Files
   
If you don't need all three sections, you can use switch /mix and all kinds of files will be added directly to project root node.

You can select source code directory with /src switch, target project directory can be changed by /target switch.

Project type can be switched by switch /exe /lib or /dll. Tool also supports Qt Meta-Object-Classes.

For basic help open command line and type "vcproj.py"
