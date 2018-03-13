import os

class Factory(object):
    __instance = None
    def __init__(self):
        self._registar = dict()
        self._index = dict()
        pass

    @staticmethod
    def Instance():
        if Factory.__instance == None:
            Factory.__instance = Factory()
        return Factory.__instance

    @staticmethod
    def Register(base_obj, obj_ , alias, f=__file__):
        if( not Factory.Instance().Exists(base_obj) ):
            Factory.Instance()._registar[base_obj] = dict()
            Factory.Instance()._index[base_obj] = dict()
        Factory.Instance()._registar[base_obj][alias] = obj_
        Factory.Instance()._index[base_obj][alias] = os.path.basename(f)

    @staticmethod
    def Create(base_obj, alias ):
        try:
            return Factory.Instance()._registar[base_obj][alias]()
        except KeyError:
            print("The object {} of type {} doesn't exists in the Factory".format(alias, base_obj))

    @staticmethod
    def Catalog():
        print("----------------------------------------------------" )
        print("---------------- Factory Catalog -------------------" )
        print("----------------------------------------------------" )
        for key, values in Factory.Instance()._registar.items():
            print("* Derived from {}".format(key))
            for name in values.keys():
                print("   -> {} implemented in {}".format(name,Factory.Instance()._index[key][name]))
        print("----------------------------------------------------" )


    def Exists(self, base):
        return base in self._registar.keys()
