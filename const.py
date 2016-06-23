import sys
class const(object):
    """常量类"""
    class ConstError(TypeError):pass 
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const {0}".format(name))
        else:
            self.__dict__[name]=value 
sys.modules[__name__] = const() 

