import time
import datetime
import yaml
import pandas as pd
import os

class History(object):
    '''A history object allows to access the logs associated to a Logpose.

    Attributes:
        events (list): list of all the logfiles associated to the Logpose named {name}.

    Args:
        name (string): name of the Logpose file.
    '''
    def __init__(self, name):
        self.name = name
        if not os.path.exists('.lp/' + self.name):
            raise ValueError('No Logpose history found!')
        self.events = sorted([file for file in os.listdir('.lp/' + self.name + '/') if file.endswith('.yml')])
        
    def load_event(self, yaml_file = -1, pandas = False):
        '''Returns a Logpose file log provided the name.

        Check the attribute events to get the log file names.

        Args:
            yaml_file (string): name of the logpose file to load. Default -1, load the last log.
            pandas (bool): if True this method will return a tuple (a, b), where b is a pandas DataFrame.
                Default False.
        '''
        if yaml_file == -1:
            yaml_file = self.events[yaml_file]
        with open('.lp/' + self.name + '/' + yaml_file, 'r') as stream:
            if pandas:
                parsed_yaml = yaml.load(stream)
                return parsed_yaml['logpose'], pd.DataFrame(parsed_yaml['routes']).transpose()
            else:
                return yaml.load(stream)

    def compare(self, pandas = False):
        '''This method returns all the logpose files in a list or a pandas dataframe.

        When pandas is set to True, it is recommended that all the logpose files have the same
        structure.
        
        Args:
            pandas (bool, optional): if True it will return a pandas dataframe. Default False.
        '''
        history_dict = []
        for logpose in self.events:
            with open ('.lp/' + self.name + '/' + logpose, 'r') as stream:
                parsed_yaml = yaml.load(stream)
                history_dict.append(parsed_yaml)
        if pandas:
            routes = [*history_dict[0]['routes']]
            for i in history_dict[1::]:
                if routes != [*i['routes']]:
                    routes = []
                    raise ValueError('The logpose files must have the same structure.')
            history_df_dict = {}
            for i in routes:
                history_df_dict[i] = pd.DataFrame([x['routes'][i] for x in history_dict]).drop(['description'], axis = 1)
            history_df = pd.concat(history_df_dict, axis = 1)
            history_df['logpose'] = self.events
            history_df.set_index('logpose', inplace = True)
            return history_df
        else:
            return history_dict

class Logpose(object):
    '''A Logpose object is a logging container object. 

    It allows to create and to structure logpose files, which are YAML files, meant to serve as logs.
    Once it is instantiated, an empty list of tasks to log is created. Each of these task is defined
    as a logpose route. To add a route to the log, it is necessary to call the add_route() method.
    The call of this class will create the folder './.lp/{name}/' where the log file will be stored.
    If no other method is called, the file will only contain the name and the description of the object.

    See add_route(), add_parameters() and save() methods to compose the log.

    Args:
        name (str): name of the Logpose.
            This name will be used to identify the logs. Logs sharing same will live in the same folder. 
        description (str): description of the log.
            The description should be relevant to discriminate logs having the same name.
        debug (bool, optional): if True no log will be created. Default False.
            Set it to true when the code to be logged is under development or you do not want to store a log.
    '''
    def __init__(self, name, description, debug = False):
        self._debug = debug
        self._routes = {}
        self._open_routes = []
        self._parameters = {}
        self._stats = {
            'name': name,
            'description': description,
            'time': ''
        }
        if not os.path.exists('.lp/' + self._stats['name'] + '/'):
            os.makedirs('.lp/' + self._stats['name'])
        self._saved = False

    def add_route(self, name, description):
        '''This method adds a Route object to a Logpose.

        A route is a unit of code doing a task to be logged.
        Once a route is added, a timer starts and counts till the bench_it({name}) method is called.
        This method can be regarded as the opening tag defining the creation of a route, meanwhile the
        bench_it({name}) method represents the closing one.
        If no other method is called the route will only store the description and time elapsed to
        excute the code contained between the call of add_parameter() and bench_it().
        
        See add_parameters() method to store other parameters into the log.

        Example:
            my_lp = Logpose('Log', 'I am a log')        # create a Logpose 
            my_lp.add_route('Route', 'I am a route')    # open a Route
                'Unit of code doing stuff to 
                log and to benchmark'
            my_lp.bench_it('Route')                      # close the Route
        
        Args:
            name (str): name of the Route.
                This name will be used to identify the route.
            description (str): description of the route.
                The description should characterise the task achieved by the route.
        '''
        if name in self._routes.keys():
            raise ValueError('The name {} is already taken!'.format(name))
        if not self._debug:
            print('\n')
            print(name)
            self._routes[name] = Route(description)
        self._open_routes.append(name)
        self._parameters[name] = {'description': description}
    
    def add_parameters(self, route_name, parameters):
        '''Add parameters to a Logpose, linked to a specific Route.

        This method allows to store other parameters to the logfile.
        Add a parameter whenever a variable's value needs to be tracked for future evaluations.

        Args:
            route_name (string): name of the route to which the parameter is linked. 
            parameters (dict, 2d-tuple): dictionary of names and values of parameters or tuple of name and parameter value.
                Ex: {'Param_name1': param_value1, 'Param_name2': param_value2} or ('Param_name, param_value)
        '''
        if route_name not in self._open_routes:
            raise ValueError('The route {} does not exist or has been closed!'.format(route_name)) 
        if type(parameters) == dict:
            for name, parameter in parameters.items():
                self._parameters[route_name][name] = parameter
        elif type(parameters) == tuple and len(parameters) == 2:
            self._parameters[route_name][parameters[0]] = parameters[1]
        else:
            raise ValueError('The variable parameters must be a dict or a 2d tuple!')
        
    def bench_it(self, name):
        '''Close a Route given the Route name.

        Args:
            name (string): name of the Route to close and benchmark.
        '''
        if name not in self._open_routes:
            raise ValueError('The route named {} is not in the logpose!'.format(name))
        else:
            if not self._debug:
                self._routes[name].close()
                self.add_parameters(name, ('time', self._routes[name].time))
            self._open_routes.remove(name)

    def save(self):
        '''Store the logpose file.
        '''
        if self._open_routes:
            raise RuntimeError('You must close all the open routes before to save the log!')
        if not self._parameters:
            raise RuntimeError('You cannot save a logpose without any route in it!')
        if not self._saved and not self._debug:
            self._stats['time'] = sum([x['time'] for x in self._parameters.values()])
            now = datetime.datetime.now()
            yaml_file = {'logpose': self._stats, 'routes': self._parameters}
            name_file = str(now.date()).replace('-', '') + '_' + str(now.time()).replace(':', '').replace('.', '_')
            with open('.lp/' + self._stats['name'] + '/' + name_file + '.yml', 'w') as outfile:
                yaml.dump(yaml_file, outfile)
            self._saved = True
        else:
            raise RuntimeError('You have already saved this log!')

class Route(object):
    '''
        Create an instance of a Route object.

    Args:
        description (string, optional): description of the Route. Default 'Running'.
        timing (bool, optional): whether to time the route execution or not. Default True.
        verbose (bool, optional): whether to print out the results. Default False.
    '''
    def __init__(self, description = 'Running', timing = True, verbose = True):
        if timing:
            self.timer = Timer()
            self.time = ''
        if verbose:
            print('\n-------------------------------------------')
            print(description + '...')
    
    def close(self):
        '''Close a route instance by getting the elapsed time.
        '''
        print('OK!')
        print('-------------------------------------------', end = '\n')
        self.time = self.timer.get_time()

class Timer(object):
    '''A simple time object.
    '''
    def __init__(self):
        self.start = time.time()
        self.time = ''
    
    def get_time(self, verbose = True):
        '''Get the time elapsed from the instantiation of a Timer object.
        
        Args:
            verbose (bool, optional): whether to print out the result of not. Default True.
        '''
        self.time = time.time() - self.start
        if verbose:
            if self.time < 60:
                time_to_print = self.time
            elif self.time < 3600:
                minutes = round(self.time / 60, 0)
                time_to_print = str(minutes) + ' m ' + str(self.time - minutes * 60)
            else:
                hours = round(self.time / 3600, 0)
                minutes = round(self.time / 60 - hours)
                seconds = (self.time / 60 - hours) / 60 - minutes
                time_to_print = str(hours) + ' h ' + str(self.time - minutes) + ' m ' + str(seconds)
            print('\n-------------------------------------------')
            print('Run in: {} s'.format(time_to_print))
            print('-------------------------------------------', end = '\n')
            return self.time
        else:
            return self.time