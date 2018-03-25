import time
import yaml
import pandas as pd
import os

class History:
    
    def __init__(self):
        if not os.path.exists('.lp'):
            raise ValueError('No Logpose history found!')
        self.history = [file for file in os.listdir('.lp/') if file.endswith('.yml')]
        
    def load_event(self, yaml_file, pandas = True):
        '''
        Return a logpose file log.

        - yaml_file (string): name of the logpose file to load
        - pandas (boolean): if True this function will return a tuple (a, b), where b is a pandas DataFrame
        '''
        with open('.lp/' + yaml_file, 'r') as stream:
            if pandas:
                parsed_yaml = yaml.load(stream)
                return parsed_yaml['logpose'], pd.DataFrame(parsed_yaml['traces']).transpose()
            else:
                return yaml.load(stream)

class Logpose:
    
    def __init__(self, name, description):
        self.timer = Timer()
        self.traces = {}
        self.open_traces = []
        self.parameters = {}
        self.stats = {
            'name': name,
            'description': description,
            'time': ''
        }
        if not os.path.exists('.lp'):
            os.makedirs('.lp')

    def add_trace(self, name, description):
        '''
        Add a trace to the logpose.
        
        - name (string): name which identifies the trace
        - description (string): short description which qualifies the trace
        '''
        if name in self.traces.keys():
            raise ValueError('The name ' + str(name) + ' is already taken!')
        print('\n' + name)
        self.traces[name] = Trace(description)
        self.open_traces.append(name)
        self.parameters[name] = {'description': description}
    
    def add_parameter(self, trace_name, param_name, value):
        '''
        Add a parameter to the trace.

        - trace_name (string): name which identifies the trace
        - param_name (string): name which identifies the parameter
        - value (any type): value of the parameter to log
        '''
        self.parameters[trace_name][param_name] = value
        
    def save(self):
        '''
        Store the logpose file.
        '''
        yaml_file = {'logpose': self.stats, 'traces': self.parameters}
        with open('.lp/' + str(time.time()) +'.yml', 'w') as outfile:
            yaml.dump(yaml_file, outfile)
        
    def bench_it(self, name = False):
        '''
        Get the time elapsed to evaluate a trace, given the trace name. 
        When no parameter is passed it evaluates the total time elapsed.

        - name (string, default = False): name of the trace to benchmark 
        '''
        if name:
            if name in self.open_traces:
                self.traces[name].close()
                self.add_parameter(name, 'time', self.traces[name].time)
                self.open_traces.remove(name)
            else:
                raise ValueError('The trace named ' + str(name) + ' is not in the logpose!')
        else:
            self.stats['time'] = self.timer.get_time()
            self.save()
        
class Trace:
    
    def __init__(self, description = 'Running', timing = True, verbose = True):
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
        '''
        self.time = time.time() - self.start
        if verbose:
            print('\n-------------------------------------------')
            print('Run in: {}s'.format(self.time))
            print('-------------------------------------------', end = '\n')
            return self.time
        else:
            return self.time