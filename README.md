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

1.  **Navigate** to the project directory.
2.  **Create and activate** the environment using Conda:
    ```bash
    # Creates 'calib_env' and installs all dependencies (Python 3.10, NumPy, OpenCV)
    conda env create -f environment.yml
    
    # Activates the environment
    conda activate calib_env
    ```

## 2. Execution

To run the calibration, ensure `intrinsics.json` and `observation.json` are in the project folder, and then execute the main script:

```bash
python calibrate_extrinsics.py