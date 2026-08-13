from ReachClasses import Reach

import time

import os

from .helper import save_timing_dict

def run_test(
    traj_dir_path : str,
    struc_id : str,
    r_choice : str,
    timing_dict : dict,
    reach : Reach,
    n_repeat : int = 5
):

    struc_dir = os.path.join(traj_dir_path, struc_id)
    xtc_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.xtc")
    dcd_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.dcd")
    pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")

    times = []

    for i in range(n_repeat):
        
        start = time.time()

        reach.process_xtc_to_input(
            xtc_path, dcd_path, pdb_path
        )

        elapsed = time.time() - start
        times.append(elapsed)

    timing_dict[struc_id] = times

def test_data_conversion(
    traj_dir_path : str,
    timing_dir : str,
    r_choice : str
) -> None:

    # init empty reach class

    reach = Reach("reach")

    # init empty timing dict

    conversion_t = {}

    # iterate directory and run speed test on each instance

    for struc_id in os.listdir(traj_dir_path):
        print(struc_id)
        run_test(
            traj_dir_path = traj_dir_path,
            struc_id = struc_id,
            r_choice = r_choice,
            timing_dict = conversion_t,
            reach = reach,
            n_repeat = 5
        )

    save_timing_dict(
        timing_dict = conversion_t,
        out_path = os.path.join(timing_dir, "setup_t.json"),
        indent = 4
    )

if __name__ == "__main__":

    timing_dir = "timing"

    os.makedirs(timing_dir, exist_ok=True)
        
    traj_dir_path = "trajectories"

    test_data_conversion(
        traj_dir_path = traj_dir_path,
        timing_dir = timing_dir,
        r_choice = "prod_R1",
    )
