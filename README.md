# A faster approach to ECG analysis in emergency situations
This is the official repository of the "A faster approach to ECG analysis in emergency situations" project for the 2020
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

To download the project and setup and start the virtual environment type:
```bash
git clone https://github.com/luigifusco/Anomalous.git
cd Anomalous
pipenv install
pipenv shell
```

Alternatively all libraries can be installed in the current `python` environment with:
```bash
python -m pip install -r requirements.txt
```

A full version of the `data` folder is available [here](https://polimi365-my.sharepoint.com/:f:/g/personal/10601210_polimi_it/Emj2B52XqjRGhQeFKiAx9EgBn-obS18bqhYUAccYyfPw6A?e=zmia3C). Please replace the folder coming with this repo before running the demos.

To run a demo of the anomaly detection go in the `Anomalous` folder and type:
```bash
python main.py
```

To see she WIP GUI type
```bash
python gui_launcher.py
```

The project was build with and tested on `python 3.7`. At the time of writing
`tensorflow` does not support `python 3.8`.

### Special thanks
We would like to thank Eleonora D'Arnese and Marco D. Santambrogio for their continuous
support to the project.
