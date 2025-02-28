 # Backend code for dissertation

Contains all code needed to simulate a gravitational wave detector array to determine the location of the source of waves.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

Necessary for ```tracker.py```

```bash
!pip install ultralytics
!pip install opencv-python
```

and for ```json_editor.py```

```bash
!pip install tkinter
```

## Usage

After installing repository and external files from a [Google Drive](https://drive.google.com/drive/folders/1RH8dodTgxTbXJND4NPkoTOEgNwhKtMST?usp=sharing) and unzipping files, here is the process to correctly use the detector:
```bash
frame-extractor.py
tracker.py
trajectory.py
timing-model.py
triangulator.py
```

### Extra code
```json_editor.py``` allows one to edit data.json which contains constants for the positional data of the detectors along with the dimensions of the plane with their associated uncertainties. 
```ToA-calculator.py``` is able to calculate the ToA from a user inputted source position which can be used to verify ```trajectory.py``` and its mathematics as it should reproduce the same location.
```main.py``` uses the trained ML model to detect the motion of an object and visualise its motion live through a webcam. 
