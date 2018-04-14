# logpose
Log library for Data Scientist written in Python (suitable for ML prototyping and jupyter projects in general).

- Do you prototype in jupyter before deploy your code?
- Do you run several python simulations and after a while you forget to keep track of your trials?
- Are you looking for a python library to store all the hyper-parameters tested tuning a ML algorithm?

**Logpose** is here for you! Logpose generates YAML files to track each simulation run. 
At the moment the library is under development. Use it but be aware that the API might change.

I daily use this library for work, so it might not have reached a stable point but it is usable.
Any suggestion, feature request or support is more than welcome.

# Install
Logpose is also installable via pip:
```
pip install logpose
```
It might land on conda in the future.

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
my_logpose.add_route('Preprocessing', 'Kill all the enemies')
my_params = random()
# Keep track of your input parameters
my_logpose.add_parameter('Preprocessing', ('my_params', my_params))
messy_code(my_params)
# Get some benchmarks
my_logpose.bench_it()
my_logpose.add_trace('Prototype', 'Conquer the Russia')
my_params_2 = random()
my_logpose.add_parameter('Prototype', ('my_params', my_params_2))
messy_code(my_params_2)
my_logpose.bench_it()
```
You only need the patience of changing the `'description'` parameter in `Logpose('name', 'description')` at each run, to make the logpose meaningful (for you) in the future.
Infact, at each run logpose saves a YAML file in the folder **.lp/{name}** of your project.

# More details
A jupyter notebook containing a script for data science can be summarised in:
1. **ETL**: retrive data from the source, loading data, feature selection, feature construction, etc.
2. **ML Model**: construction of the train, test set, adoption of serveral ML algorithms, cross validation 
3. **Results**: analysis over the metrics obtained via the previous step
This script might change several times, even during the same day. The dataset as well might change.

Whenever you run the script you have to keep track of many variables such as: the number of records in the dataset, the feature selected, the features constructed, the hyper-parameters of the ML algorithm, the metrics and so on.
Logpose creates a folder where all these information will be stored into YAML files and grouped by simulation name, which can be viewed and compared later on.

### The code
The logpose module contains mainly two relevant classes:
- `Logpose` generates logs with the help of its methods,
- `History` access the logs created via a `Logpose` object.

Let us assume we have a jupyter representing a simulation with a xgboost algorithm.

#### Logpose object
The `Logpose` object is a container which creates a folder named with the same name given to the object.
```python
import logpose as lp
# Create your logpose
my_logpose = lp.Logpose('xgboost', 'Attempt number 1 with xgboost, max_depth = 15')
```
The code above creates the path `/lp/xgboost` in the directory where the code file is located.

Since a `Logpose` instance is just an empty box, it is necessary to add task to log. A task is a unit piece of code to log, and in the framework of **logpose** is called a `Route`. A `Route` be created by calling the `add_route()` method.
```python
import logpose as lp
# Create your logpose
my_logpose = lp.Logpose('xgboost', 'Attempt number 1 with xgboost, max_depth = 15')
''' CODE MISSING '''
my_logpose.add_route('Model', 'No cross validation')
import xgboost as xgb
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic' }
num_round = 2
bst = xgb.train(param, dtrain, num_round)
my_logpose.bench_it('Model')
''' CODE MISSING '''
```
The code above shows how to create a `Route` and how to close it via the method `bench_it()`.
To summarise, the methods `add_route()` and `bench_it()` are respectively the opening and closing tag, wrapping the code we aim to log.

Now, the `Logpose` instance is aware of a task to log and it is also timing it. The code written above, would create a log file in the folder **./.lp/xgboost** in which are stored the description of the `Logpose`, the characteristics (name and description) of the `Route` and its execution time.
In order to track also the xgboost parameters, we have to use the method `add_parameters()`.
```python
import logpose as lp
# Create your logpose
my_logpose = lp.Logpose('xgboost', 'Attempt number 1 with xgboost, max_depth = 15')
''' CODE MISSING '''
my_logpose.add_route('Model', 'No cross validation')
import xgboost as xgb
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic' }
my_logpose.add_parameters('Model', param)
num_round = 2
my_logpose.add_parameters('Model', ('num_round', 2))
bst = xgb.train(param, dtrain, num_round)
my_logpose.bench_it('Model')
''' CODE MISSING '''
```
In this way also the parameters (`param` and `num_round`) would get saved inside the logfile.

Linked to the same logpose instance you can add multiple routes, structuring the log in the way you like. For example, following the scheme described above:

```python
import logpose as lp
# Create your logpose
my_logpose = lp.Logpose('xgboost', 'Attempt number 1 with xgboost, max_depth = 15')
my_logpose.add_route('Preprocessing', 'Remove missing values')
''' CODE MISSING '''
my_logpose.bench_it('Preprocessing')
my_logpose.add_route('Model', 'No cross validation')
import xgboost as xgb
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic' }
my_logpose.add_parameters('Model', param)
num_round = 2
my_logpose.add_parameters('Model', ('num_round', 2))
bst = xgb.train(param, dtrain, num_round)
my_logpose.bench_it('Model')
my_logpose.add_route('Results', 'Metrics over train and validation sets')
''' CODE MISSING '''
my_logpose.bench_it('Results')
```

#### History object
If you want to check what happened in a simulation where you have used a `Logpose`, you just need to check in the **./.lp** folder. 
Alternatively, it is possible to create a `History` object.
```python
history_log = lp.History('xgboost')
my_simulations = history_log.events
```
The `History` attribute `events` provides the list of all the YAML files located in the logpose folder **./.lp/xgboost/**. To load an event:
```python
import pandas
logpose_info, logpose_df = history_log.load_event(my_simulations[0], pandas = True)
```
When the `pandas` parameter is `True`, the method `load_event()` returns 2d-tuple where the second element is a pandas dataframe.

To compare all the events, the log files stored in the folder, you can use the method `compare()`.
```python
history_df = history_log.compare(pandas = True)
```