#==============================================================================
# Copyright (C) 2018 Marchand Basile
# 
# This file is part of pyfetra.
# 
# pyfetra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# pyfetra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyfetra.  If not, see <http://www.gnu.org/licenses/>
#==============================================================================


import os
import sys 

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
        except KeyError as e:
            print("The object {} of type {} doesn't exists in the Factory".format(alias, base_obj))
            print(e)
            sys.exit(1)


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
