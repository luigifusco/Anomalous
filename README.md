# ANOMALOUS
This is the official repository of the Anomalous project for the 2020
"Progetto di Ingegneria Informatica" exam. The authors are:
- Luigi Fusco (10601210)
- Ian Di Dio Lavore (10580652)
- Marco Di Gennaro (10596841)

Anomalous is a full stack ECG analysis system. It is capable of detecting tachycardia,
bradycardia and several other heartbeat anomalies, more specifically left bundlebranch
block beat, right bundle branch block beat, atrial premature beat, supraventricular
premature orectopic beat, premature ventricular contraction and R-on-T premature
ventricular contraction, with varying degree of precision.

## Installation
Anomalous is build using the `python` programming language and makes use of several
libraries and frameworks. It supports `pipenv` for the easy creation of ready to use
virtual environments. `pipenv` requires `python` and `pip` to be installed in your sistem,
and can be installed with:
```bash
python -m pip install pipenv
```

To download the project and setup the virtual environment type:
```bash
git clone https://github.com/luigifusco/Anomalous.git
cd Anomalous
pipenv install
```

To run the project go in the `Anomalous` folder and type:
```bash
pipenv shell
python main.py
```

### Special thanks
We would like to thank Eleonora D'Arnese and Marco D. Santambrogio for their continuous
support to the project.
