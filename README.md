# Multi-Camera Calibration: Extrinsics Determination

This project contains the solution for calculating the extrinsic parameters (position and orientation) of the three cameras relative to the common world coordinate system, using the PnP (Perspective-n-Point) algorithm.

The primary output of this process is the file: `extrinsics_result.json`.

---

## 1. Environment Setup

The required environment is defined in the `environment.yml` file, ensuring perfect reproducibility across machines.

```bash
cd path/to/root/folder/                 # navigate to project dir
conda env create -f environment.yml     # create conda env
conda activate calib_task               # activate conda env
```

## 2. Execution

To run the calibration, ensure `intrinsics.json` and `observation.json` are in the project folder, and then execute the main script:

```bash
python calibrate_extrinsics.py