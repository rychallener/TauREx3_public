from functools import wraps, partial


def fitparam(f=None,param_name=None,param_latex=None,default_mode='linear',default_fit=False,default_bounds=None):
    """This informs the Fittable class that this particular
    method is fittable and provides extra properties
    to the function
    """
    if f is None:
        return partial(fitparam, param_name=param_name,param_latex=param_latex,default_mode=default_mode,default_fit=default_fit,default_bounds=default_bounds)
    
    def wrapper(self, *args, **kwargs):
        
        return f(self, *args, **kwargs)
    wrapper.param_name = param_name
    wrapper.param_latex = param_latex
    wrapper.default_fit = default_fit
    wrapper.default_bounds = default_bounds
    wrapper.default_mode = default_mode
    wrapper.decorated = 'fitparam'
    pwrap = property(wrapper)


    return pwrap



class Fittable(object):
    """
    
    An object that has items that can be fit. Its main
    task is to collected all properties that are fittable
    and present them to the fitting code in a nice way

    """
    def __init__(self):
        self._param_dict = {}

        self.compile_fitparams()


    def add_fittable_param(self,param_name,param_latex,fget,fset,default_mode,default_fit,default_bounds):
        if param_name in self._param_dict:
            raise AttributeError('param name {} already exists'.format(param_name))

        self._param_dict[param_name] = (param_name,param_latex,
                        fget.__get__(self),fset.__get__(self),
                                default_mode,default_fit,default_bounds)
        
    def compile_fitparams(self):

        for fitparams in self.find_fitparams():

            get_func = fitparams.fget
            set_func = fitparams.fset
            param_name = get_func.param_name
            param_latex = get_func.param_latex
            def_mode = get_func.default_mode
            def_fit = get_func.default_fit
            def_bounds = get_func.default_bounds
            self.add_fittable_param(param_name,param_latex,get_func,set_func,def_mode,def_fit,def_bounds)


    def __getitem__(self,key):
        param = self._param_dict[key]

        return param[2]()

    def __setitem__(self,key,value):
        return self._param_dict[key][3](value)        

    def find_fitparams(self):
        """ 
        Finds and returns fitting parameters
        """
    
        for klass in self.__class__.mro():

            for method in klass.__dict__.values():
                if hasattr(method, 'fget'):
                    prop = method.fget
                    if hasattr(prop,'decorated'):
                        if prop.decorated == 'fitparam':
                            yield method      

    def fitting_parameters(self):
        return self._param_dict

    
    def recalculate(self):
        pass