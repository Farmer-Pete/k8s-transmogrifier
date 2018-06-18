## K8S Transmogrifier ##

![transmogrifier](https://disemvowel.files.wordpress.com/2010/05/trans-1-5.gif)

```
usage: transmogrifier.py [-h] [--code DIRECTORY] [--code-language {java}]
                         [--code-java-package JAVA-PACKAGE]
                         [--code-loader LOADER] [--report FILE]
                         [--report-layout {web}] [--report-title TITLE]
                         CONFIG_DIR

Transmogrifier: Reads Kubernetes configmaps and secrets, generating all kinds
of useful things

positional arguments:
  CONFIG_DIR            the directory to the k8s config files

optional arguments:
  -h, --help            show this help message and exit

Code Generation:
  --code DIRECTORY      generates code libraries
  --code-language {java}
                        target language for code generation

Code Generation Options:
  --code-java-package JAVA-PACKAGE
                        package name of the generated files
  --code-loader LOADER  Generated stub interface to grab and parse files

Report Generation:
  --report FILE         generates reports
  --report-layout {web}
                        layout to use for report generation
  --report-title TITLE  title displayed on report
```
