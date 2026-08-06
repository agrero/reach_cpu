from ReachClasses import ReachConfig, Reach

import timeit

import json

import os

def save_timing_dict(timing_dict:dict, out_path:str, indent:int=4) -> None:
    with open(out_path, "w") as f:
        json.dump(timing_dict, f, indent=indent)

def test_data_conversion(
    traj_dir_path:str,
    r_choice:str    
    ) -> None:

    def _run_test(
            traj_dir_path:str,
            struc_id:str,
            r_choice:str,
            timing_dict:dict 
        ) -> None:

        struc_dir = os.path.join(traj_dir_path, struc_id)
        xtc_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.xtc")
        dcd_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.dcd")
        pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")

        t = timeit.Timer(
            lambda: reach.convert_xtc_to_dcd(
                xtc_path, dcd_path, pdb_path
            )
        )
        timing_dict[struc_id] = t

    # init empty dict repo
    conversion_t = {}

    # iterate directory and run speed test on each instance
    for struc_id in os.listdir(traj_dir_path):
        _run_test(traj_dir_path, struc_id, r_choice, conversion_t)

    # save dict to json
    save_timing_dict(conversion_t, os.path.join(timing_dir, "conversion_t.json"))

def test_running_reach(traj_dir_path:str) -> None:

    # will need to time this one for generating configs + running reach
    # IE use timeit on this function rather that the reach method
    def _run_test(
            traj_dir_path:str, 
            struc_id:str, 
            r_choice:str
        ):
        struc_dir = os.path.join(traj_dir_path, struc_id)
        dcd_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.dcd")
        pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")
        reach_out_path = os.path.join(struc_dir, "reach")

        os.makedirs(reach_out_path, exist_ok=True)

        config = ReachConfig(
            NCRDFMT=0,
            CRDPATH=pdb_path,
            NSECOND=1,
            DSSPPATH="" # need to have a working installation of pydssp first
        )

    running_t = {}

    for struc_id in os.listdir(traj_dir_path):
        _run_test()


if __name__ == "__main__":

    # Paths

    timing_dir = "timing"
    os.makedirs(timing_dir, exist_ok=True)

    reach_path = os.path.join("source", "reach")
    reach_path = os.path.abspath(reach_path)
    reach = Reach(reach_path)

    traj_dir_path = "trajectories"
    r_choice = "prod_R1"

    # Data conversion

    conversion_t = {}

    test_data_conversion(
        traj_dir_path=traj_dir_path,

    )

    for struc_id in os.listdir(traj_dir_path):

        struc_dir = os.path.join(traj_dir_path, struc_id)

        xtc_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.xtc")
        dcd_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.dcd")
        pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")

        t = timeit.Timer(
            lambda: reach.convert_xtc_to_dcd(
                xtc_path, dcd_path, pdb_path
            )
        )
        conversion_t[struc_id] = t

    save_timing_dict(
        conversion_t, 
        os.path.join(timing_dir, "conversion_t.json")
    )

    # Reach running
    for struc_id in os.listdir(traj_dir_path):
        struc_dir = os.path.join(traj_dir_path, struc_id)

        xtc_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}")
        out_path = os.path.join(struc_dir, "reach", )

        t = timeit.Timer(
            lambda: reach.run(
                xtc_path, 
            )
        )

    # Pulling constants
