from PyDssp import PyDssp

import time

import os

from .helper import save_timing_dict


def run_test(
    pydssp : PyDssp,
    pdb_in_path : str,
    out_path : str,
    timing_dict : dict,
    struc_id : str,
    n_repeat : int = 5
) -> None:

    times = []

    for i in range(n_repeat):
        start = time.time()

        pydssp(
            pdb_in = pdb_in_path, 
            out_path = out_path
        )

        elapsed = time.time() - start
        times.append(elapsed)

    timing_dict[struc_id] = times

def test_pydssp(
    traj_dir_path : str,
    timing_dir : str
) -> None:
    
    pydssp = PyDssp()

    conversion_t = {}

    for struc_id in os.listdir(traj_dir_path):
        
        struc_dir = os.path.join(traj_dir_path, struc_id)
        pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")
        print(pdb_path)
        out_path = os.path.join(struc_dir, f"{struc_id}.dssp")

        run_test(
            pydssp = pydssp,
            pdb_in_path = pdb_path,
            out_path = out_path,
            timing_dict = conversion_t,
            struc_id = struc_id,
            n_repeat = 5
        )

    save_timing_dict(
        timing_dict = conversion_t,
        out_path = os.path.join(timing_dir, "pydssp_t.json"),
        indent = 4
    )
        

if __name__ == "__main__":

    timing_dir = "timing"
    traj_dir_path = "trajectories"

    test_pydssp(
        traj_dir_path = traj_dir_path,
        timing_dir = timing_dir
    )

