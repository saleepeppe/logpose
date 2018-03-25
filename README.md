# logpose
Log library for python (suitable for ML prototyping and jupyter projects in general).

- Do you prototype in jupyter before going in production with your code?
- Do you run several python simulations and after a while you forget to keep track of your trials?
- Would you like to have a python library to keep track of all your attempts tuning a ML algorithm?

**Logpose** is here for you! Logpose generates YAML files to track each simulation run. 
At the moment the library is under development. Structure and features will come soon.
Stay tuned!

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
import logpose
# Create your logpose
my_logpose = Logpose('My Simulation', 'Try to rule the world')
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
my_logpose.add_parameter('Prototype', 'my_params_2', my_params_2)
messy_code(my_params_2)
my_logpose.bench_it('Prototype')
my_logpose.bench_it()
```
You only need the patience of changing the parameters in ```Logpose('My Simulation', 'Try to rule the world')``` at each run, to make the logpose meaningful (for you) in the future.
Infact, at each run logpose saves a YAML file in the ```.lp``` folder of your project.
Basically, if you want to track a file you need to instantiate a ```Logpose``` object.
If you want to split your log in multiple parts you add a trace to the logpose ```Logpose.add_trace```. Instead to save other kind of parameters you may add a parameter to the trace ```Logpose.add_parameter```.
# Access a logpose file
If you want to check what you have done in a simulation you just need to open them or as experimental feature you can create a ```History``` object.
```python
history_log = History()
my_history = history_log.history
```
The code attribute ```history``` provides the list of all the YAML files, which can be loaded via:
```python
import pandas
my_history.load_event(my_history[0], pandas = True)
```