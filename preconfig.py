import pip
import importlib
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def installAndImport(libs=[]):
    libsAs=[None]*len(libs)
    for lib in libs:
        libsAs[libs.index(lib)]=installOrImport(libname=lib)
    return libsAs
    
def installOrImport(libname):
    try:
        lib=importlib.import_module(libname)
        return lib 
    except:
        install(libname)
        lib=importlib.import_module(libname)
        return lib

installAndImport(libs=["pandas"])