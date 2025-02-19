# Detector component of dissertation

This folder comtaines all the code necessary for the operation of the simulated GW detector.

Requires the dowload of [external files](https://drive.google.com/drive/folders/1RH8dodTgxTbXJND4NPkoTOEgNwhKtMST?usp=sharing) and to be saved in the same file location as the code.



## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

Necessary for ```bob-tracker.py```

```bash
!pip install ultralytics
!pip install opencv-python
```

## Files

```frame-extractor.py``` extracts the frames of a video of the simulated GW detector into a folder, the images are then used to train a machine learning algorithm and eventually simulate detection of a GW.

```training_set.ipynb``` trains a model of YOLOv8 to detect the presence of a small peice of blue foam on the surface of water, this represents the GW detector where the motion of the foam when a wave is propagated through the water indicates when a GW is detected.

```bob-tracker.py``` loads each frame extracted from the video and processes it via a trained ML algorithm to produce positional data of the foam.

```bob-trajectory.py``` calculates distance travelled by the foam between consecutive frames to determine when the waves interacts with the foam bob.
