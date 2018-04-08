import time
import datetime
import yaml
import pandas as pd
import os

class History:
    
    def __init__(self):
        if not os.path.exists('.lp'):
            raise ValueError('No Logpose history found!')
        self.history = sorted([file for file in os.listdir('.lp/') if file.endswith('.yml')])
        
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

    def compare(self, pandas = False):
        '''
        This method return all the logpose files in a list.
        
        - pandas (bool, default = False): if True it will return a pandas dataframe.
        !!!WARNING!!
        When pandas is set True the all the logpose files must have the same structure, meaning same parameters'
        and traces' names.
        '''
        history_dict = []
        for logpose in self.history:
            with open ('.lp/' + logpose, 'r') as stream:
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
            return history_df_dict
        return history_dict

class Logpose:
    
    def __init__(self, name, description):
        '''
        Create an istance of a Logpose object.

        - name (string): name of the Logpose
        - description (string): description of the Logpose
        '''
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
        now = datetime.datetime.now()
        yaml_file = {'logpose': self.stats, 'traces': self.parameters}
        name_file = str(now.date()).replace('-', '') + '_' + str(now.time()).replace(':', '').replace('.', '_')
        with open('.lp/' + name_file +'.yml', 'w') as outfile:
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