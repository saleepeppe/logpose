# logpose
Log library for python (suitable for ML prototyping and jupyter projects in general).

- Do you prototype in jupyter before going in production with your code?
- Do you run several python simulations and after a while you forget to keep track of your trials?
- Would you like to have a python library to keep track of all your attempts tuning a ML algorithm?

**Logpose** is here for you! Logpose generates YAML files to track each simulation run. 
At the moment the library is under development. Structure and features will come soon.
Stay tuned!

# Install
Now logpose is on pip:
```
pip install logpose
```

# Usage
Let us assume you have a python script that resembles to:
```python
from random import random
def messy_code(a):
    print('Crazy python stuff here {}'.format(a))
# Sorry for trolling
my_params = random() 
messy_code(my_params)
my_params_2 = random()
messy_code(my_params_2)
```
You run this script several times per day and you need to keep track of what is happening.
Here it comes logpose.
```python
import logpose as lp
# Create your logpose
my_logpose = lp.Logpose('My Simulation', 'Try to rule the world')
# Add a trace
my_logpose.add_trace('Preprocessing', 'Kill all the enemies')
my_params = random()
# Keep track of your input parameters
my_logpose.add_parameter('Preprocessing', 'my_params', my_params)
messy_code(my_params)
# Get some benchmarks
my_logpose.bench_it('Preprocessing')
my_logpose.add_trace('Prototype', 'Conquer the Russia')
my_params_2 = random()
my_logpose.add_parameter('Prototype', 'my_params', my_params_2)
messy_code(my_params_2)
my_logpose.bench_it('Prototype')
my_logpose.bench_it()
```
You only need the patience of changing the parameters in `Logpose('name', 'description')` at each run, to make the logpose meaningful (for you) in the future.
Infact, at each run logpose saves a YAML file in the folder `.lp/{name}` of your project.

Basically, if you want to track a file you need to instantiate a `Logpose` object.
If you want to split your log in multiple parts, you add a trace to the logpose `add_trace('trace_name', 'trace_description')`. To save other kind of parameters, you may add a parameter to a created trace `add_parameter('trace_name', 'param_name', value)`.

# Access a logpose file
If you want to check what happened in a simulation, you just need to check in the **.lp** folder. Alternatively, it is possible to create a `History` object.
```python
history_log = lp.History('My Simulation')
my_simulations = history_log.events
```
The code attribute `events` provides the list of all the YAML files located in the logpose folder. To load an event:
```python
import pandas
history_log.load_event(my_simulations[0], pandas = True)
```
When the `pandas` parameter is `True`, the method `load_event` returns 2d-tuple where the second element is a pandas dataframe.