# Multi-Camera Calibration: Extrinsics Determination

This project contains the solution for calculating the extrinsic parameters (position and orientation) of the three cameras relative to the common world coordinate system, using the PnP (Perspective-n-Point) algorithm.

The primary output of this process is the file: `extrinsics_result.json`.

---

## 1. Environment Setup

The required environment is defined in the `environment.yml` file, ensuring perfect reproducibility across machines.

```bash
cd path/to/project/folder/              # navigate to project dir
conda env create -f environment.yml     # create conda env
conda activate calib_task               # activate conda env
```

## 2. Data
The script requires two input files in the project root:
`intrinsics.json` and `observations.json`

**Action Required:** Use the provided files for the initial result, or replace them with new calibration data for a subsequent run. The format must match the original structure.


## 3. Execution

With the environment active and data files in place, execute the main script:

```bash
python calibrate_extrinsics.py
```

The script will generate the output file `extrinsics_result.json`.

