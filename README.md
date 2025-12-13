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

---

## Explanation of Extrinsic Results

The file `extrinsics_result.json` contains the extrinsic transformation from the common world coordinate system to each camera’s coordinate system.

### A. The Coordinate System

* The **World Coordinate System** ($\mathbf{X}_W, \mathbf{Y}_W, \mathbf{Z}_W$) is defined by the 3D points in the `observations.json`. Since the $Z$ coordinate is $3.0$ for all points, the checkerboard is placed in the plane $Z=3.0$ meters.
* The **Camera Coordinate System** ($\mathbf{X}_C, \mathbf{Y}_C, \mathbf{Z}_C$) has its origin at the camera's optical center.

### B. Key Outputs

The relationship between a 3D point in the World ($\mathbf{X}_W$) and a 3D point in the Camera ($\mathbf{X}_C$) is given by:

$$\mathbf{X}_C = R \mathbf{X}_W + t$$

The `extrinsics_result.json` provides the components of this relationship for each camera:

| Key | Description | Units |
| :--- | :--- | :--- |
| **`rotation_matrix_R`** | The $3 \times 3$ rotation matrix. It describes the camera's orientation (or how to rotate a world point to be aligned with the camera's axes). | Dimensionless |
| **`translation_vector_t`** | The $3 \times 1$ translation vector. It is the position of the world origin ($\mathbf{X}_W=[0,0,0]$) expressed in the camera's coordinate system. | Meters (m) |
| **`T_homogeneous_matrix_4x4`** | The complete $4 \times 4$ extrinsic transformation matrix, $[R : t]$, used for homogeneous coordinate transformations. | Mixed (Dimensionless and Meters) |

### C. Example Interpretation (Cam0)

Looking at the output for `cam0`:
* **Translation $\mathbf{t}$:** `[-0.009, 2.096, 5.846]`
    * This means the World Origin $[0, 0, 0]$ is located at $X \approx 0 \text{m}$, $Y \approx 2.10 \text{m}$, and $Z \approx 5.85 \text{m}$ in *Cam0's frame*.
    * Since the checkerboard (the reference for $R$ and $t$) was placed at $Z=3.0$ meters, a large $Z$ translation value ($\approx 5.85$) is reasonable, indicating the camera is positioned significantly further back from the calibration plane than the calibration plane is from the origin of the world coordinate system.

