import time
import datetime
import yaml
import pandas as pd
import os

class History:
    
    def __init__(self, name):
        '''
        Create a history object based on the logpose name

        - name (string): name of the logpose
        '''
        self.name = name
        print(self.name)
        if not os.path.exists('.lp/' + self.name):
            raise ValueError('No Logpose history found!')
        self.events = sorted([file for file in os.listdir('.lp/' + self.name + '/') if file.endswith('.yml')])
        
    def load_event(self, yaml_file, pandas = True):
        '''
        Return a logpose file log.

        - yaml_file (string): name of the logpose file to load
        - pandas (boolean): if True this function will return a tuple (a, b), where b is a pandas DataFrame
        '''
        with open('.lp/' + self.name + '/' + yaml_file, 'r') as stream:
            if pandas:
                parsed_yaml = yaml.load(stream)
                return parsed_yaml['logpose'], pd.DataFrame(parsed_yaml['traces']).transpose()
            else:
                return yaml.load(stream)

    def compare(self, pandas = False):
        '''
        This method returns all the logpose files in a list.
        
        - pandas (bool, default = False): if True it will return a pandas dataframe.
        !!!WARNING!!
        When pandas is set True the all the logpose files must have the same structure, meaning same parameters'
        and traces' names.
        '''
        history_dict = []
        for logpose in self.events:
            with open ('.lp/' + self.name + '/' + logpose, 'r') as stream:
                parsed_yaml = yaml.load(stream)
                history_dict.append(parsed_yaml)
        if pandas:
            traces = [*history_dict[0]['traces']]
            for i in history_dict[1::]:
                if traces != [*i['traces']]:
                    traces = []
                    raise ValueError('The logpose files must have the same structure.')
            history_df_dict = {}
            for i in traces:
                history_df_dict[i] = pd.DataFrame([x['traces'][i] for x in history_dict]).drop(['description'], axis = 1)
            history_df = pd.concat(history_df_dict, axis = 1)
            history_df['logpose'] = self.events
            history_df.set_index('logpose', inplace = True)
            return history_df
        else:
            return history_dict

class Logpose:
    
    def __init__(self, name, description, debug = False):
        '''
        Create an istance of a Logpose object.

        - name (string): name of the Logpose
        - description (string): description of the Logpose
        - debug (bool): if True pause the logpose
        '''
        self.debug = debug
        if not self.debug:
            self.timer = Timer()
        self.traces = {}
        self.open_traces = []
        self.parameters = {}
        self.stats = {
            'name': name,
            'description': description,
            'time': ''
        }
        if not os.path.exists('.lp/' + self.stats['name'] + '/'):
            os.makedirs('.lp/' + self.stats['name'])
        

    def add_trace(self, name, description):
        '''
        Add a trace to the logpose.
        
        - name (string): name which identifies the trace
        - description (string): short description which qualifies the trace
        '''
        if name in self.traces.keys():
            raise ValueError('The name {} is already taken!'.format(name))
        if not self.debug:    
            print('\n')
            print(name)
            self.traces[name] = Trace(description)
        self.open_traces.append(name)
        self.parameters[name] = {'description': description}
    
    def add_parameters(self, trace_name, parameters):
        '''
        Add parameters to the trace.

        - trace_name (string): name which identifies the trace
        - parameters (dict, 2d tuple): dictionary of name and values of parameters or tuple of name and parameter value
        '''
        if trace_name not in self.traces.keys():
            raise ValueError('The trace {} does not exist!'.format(trace_name)) 
        if type(parameters) == dict:
            for name, parameter in parameters:
                self.parameters[trace_name][name] = parameter
        elif type(parameters) == tuple and parameters.shape == 2:
            self.parameters[trace_name][parameters[0]] = parameters[1]
        else:
            raise ValueError('The variable parameters must be a dict or a 2d tuple!')
        
    def __save(self):
        '''
        Store the logpose file.
        '''
        if not self.debug:
            now = datetime.datetime.now()
            yaml_file = {'logpose': self.stats, 'traces': self.parameters}
            name_file = str(now.date()).replace('-', '') + '_' + str(now.time()).replace(':', '').replace('.', '_')
            with open('.lp/' + self.stats['name'] + '/' + name_file + '.yml', 'w') as outfile:
                yaml.dump(yaml_file, outfile)
        
    def bench_it(self, name = False):
        '''
        Get the time elapsed to evaluate a trace, given the trace name. 
        When no parameter is passed it evaluates the total time elapsed.

        - name (string, default = False): name of the trace to benchmark 
        '''
        if not self.debug:
            if name:
                if name in self.open_traces:
                    self.traces[name].close()
                    self.add_parameters(name, ('time', self.traces[name].time))
                    self.open_traces.remove(name)
                else:
                    raise ValueError('The trace named {} is not in the logpose!'.format(name))
            elif self.open_traces:
                last_trace = self.open_traces[-1]
                self.bench_it(last_trace)
            if not self.open_traces:
                self.stats['time'] = self.timer.get_time()
                self.__save()
        
class Trace:
    
    def __init__(self, description = 'Running', timing = True, verbose = True):
        '''
        Create an instance of a Trace object.

        - description (string): description of the trace
        - timing (bool, default = True): whether to time the trace execution or not
        - verbose (bool, default = True): whether to print out the results 
        '''
        if timing:
            self.timer = Timer()
            self.time = ''
        if verbose:
            print('\n-------------------------------------------')
            print(description + '...')
    
    def close(self):
        '''
        Close a trace instance by getting the elapsed time.
        '''
        print('OK!')
        print('-------------------------------------------', end = '\n')
        self.time = self.timer.get_time()

class Timer:
    
    def __init__(self):
        self.start = time.time()
        self.time = ''
    
    def get_time(self, verbose = True):
        '''
        Get the time elapsed from the instantiation of a Timer object.
        
        - verbose (bool, default = True): whether to print out the result.
        '''
        self.time = time.time() - self.start
        if verbose:
            print('\n-------------------------------------------')
            print('Run in: {}s'.format(self.time))
            print('-------------------------------------------', end = '\n')
            return self.time
        else:
            return self.time