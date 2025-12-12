import json
import numpy as np
import cv2 # OpenCV is the core library for the solvePnP function

# --- 1. Data Loading and Structuring Function (Step 1 Refined) ---

def load_calibration_data(intrinsics_path: str, observations_path: str) -> dict:
    """
    Loads camera calibration data (intrinsics and observations) from JSON files.
    
    This function specifically handles the input structure:
    - Intrinsics: uses the 'K' and 'distortion' keys.
    - Observations: pulls data from the 'cameras' nested dictionary.
    
    It converts relevant lists to NumPy arrays, which are the required input 
    format for OpenCV's solvePnP function.
    """
    print(f"Loading data from {intrinsics_path} and {observations_path}...")
    try:
        with open(intrinsics_path, 'r') as f:
            intrinsics_data = json.load(f)
        
        with open(observations_path, 'r') as f:
            observations_data = json.load(f)
    except FileNotFoundError as e:
        print(f"ERROR: Missing file {e.filename}. Aborting.")
        return {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in a file. {e}. Aborting.")
        return {}

    structured_data = {}
    
    # We iterate over the cameras listed inside the 'cameras' key of observation data
    obs_cameras = observations_data.get('cameras', {})
    
    for cam_id, obs_data in obs_cameras.items():
        if cam_id not in intrinsics_data:
            print(f"Warning: Intrinsics for {cam_id} not found. Skipping.")
            continue

        int_data = intrinsics_data[cam_id]

        structured_data[cam_id] = {
            # K matrix (3x3): Converted to float32 NumPy array
            "K": np.array(int_data['K'], dtype=np.float32),
            
            # Distortion Coefficients: Uses 'distortion' key, converted to float32
            # OpenCV's PnP expects this as a 1xN array.
            "dist": np.array(int_data['distortion'], dtype=np.float32),
            
            # 3D World Points (N x 3): The 'Object Points' (X_W)
            "points_3d": np.array(obs_data['points_3d'], dtype=np.float32),
            
            # 2D Image Points (N x 2): The 'Image Points' (p)
            "points_2d": np.array(obs_data['points_2d'], dtype=np.float32)
        }
        
        # Validation check
        if structured_data[cam_id]["points_3d"].shape[0] != structured_data[cam_id]["points_2d"].shape[0]:
            print(f"Error: Mismatch in 3D/2D point count for {cam_id}. Skipping.")
            del structured_data[cam_id]

    return structured_data


# --- 2. Extrinsics Calculation Function (Step 2) ---

def calculate_extrinsics(camera_data: dict) -> dict:
    """
    Calculates the extrinsic parameters (Rotation Matrix R and Translation Vector t) 
    using the Perspective-n-Point (PnP) algorithm.
    """
    K = camera_data['K']
    dist = camera_data['dist']
    object_points = camera_data['points_3d']
    image_points = camera_data['points_2d']
    
    # 1. Solve the PnP problem (Finds the pose that minimizes the reprojection error)
    # The output rvec (Rodrigues vector) and tvec define the pose of the 
    # world coordinate system with respect to the camera coordinate system.
    success, rvec, tvec = cv2.solvePnP(
        object_points, 
        image_points, 
        K, 
        dist, 
        flags=cv2.SOLVEPNP_ITERATIVE # Iterative method is robust and accurate
    )

    if not success:
        raise RuntimeError("cv2.solvePnP failed to converge.")

    # 2. Convert the Rotation Vector (rvec) to a 3x3 Rotation Matrix (R)
    R_matrix, _ = cv2.Rodrigues(rvec)

    # 3. Construct the 4x4 Homogeneous Transformation Matrix (T)
    # This matrix T represents the full extrinsic pose [R | t]
    T_matrix = np.identity(4, dtype=np.float64)
    T_matrix[:3, :3] = R_matrix
    T_matrix[:3, 3] = tvec.flatten()
    
    # Return results as standard Python lists for JSON serialization
    return {
        "rotation_matrix_R": R_matrix.tolist(),
        "translation_vector_t": tvec.flatten().tolist(),
        "T_homogeneous_matrix_4x4": T_matrix.tolist(),
        "R_Rodrigues_vector": rvec.flatten().tolist() # Include rvec for completeness
    }


# --- 3. Main Execution Script ---

def main():
    INTRINSICS_FILE = 'intrinsics.json'
    OBSERVATIONS_FILE = 'observations.json'
    OUTPUT_FILE = 'extrinsics_result.json'
    
    # 1. Load and structure data
    all_camera_data = load_calibration_data(INTRINSICS_FILE, OBSERVATIONS_FILE)
    
    if not all_camera_data:
        print("No valid camera data loaded. Exiting.")
        return
        
    results = {"cameras": {}}
    
    # 2. Process each camera
    for cam_id, cam_data in all_camera_data.items():
        print(f"\nProcessing {cam_id}...")
        try:
            extrinsics = calculate_extrinsics(cam_data)
            results["cameras"][cam_id] = extrinsics
            print(f"SUCCESS: Extrinsics calculated for {cam_id}.")
        except Exception as e:
            print(f"FAILURE: Could not calculate extrinsics for {cam_id}. Error: {e}")
            results["cameras"][cam_id] = {"error": str(e)}

    # 3. Save final results
    with open(OUTPUT_FILE, 'w') as f:
        # Use indent=4 for clean, human-readable JSON output for your colleague
        json.dump(results, f, indent=4)
        
    print(f"\n--- Processing Complete ---")
    print(f"Results saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()