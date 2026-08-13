import mdtraj as md

import time

import os

from .helper import save_timing_dict
from ReachClasses import ReachConfig, Reach


def run_test(
    input_path : str,
    out_path : str,
    struc_dir : str,
    struc_id : str,
    timing_dict : dict,
    reach : Reach, 
    n_repeat : int = 5
) -> None:

    times = []
    for i in range(n_repeat):
        start = time.time()

        reach.run(
            input_path = input_path,
            out_path = out_path,
            output_dir = struc_dir
        )

        elapsed = time.time() - start
        times.append(elapsed)

    timing_dict[struc_id] = times

def test_run_reach(
    traj_dir_path : str,
    timing_dir : str,
    r_choice : str,
    reach_exec_path : str
) -> None:

    traj_dir_path = os.path.abspath(traj_dir_path)
    
    config = ReachConfig(
        TRALEN=100000.,
        TEMPERA=300.,
        NCRYSTAL=1
    )

    # ITERATE STRUCTURE DIRECTORY

    reach_t = {}
    reach = Reach(reach_exec_path)

    for struc_id in os.listdir(traj_dir_path):
        print(struc_id)
        # DEFINE PATH NAMES

        struc_dir = os.path.join(traj_dir_path, struc_id)
        dcd_path = os.path.join(struc_dir, f"{struc_id}_{r_choice}_fit.dcd")
        pdb_path = os.path.join(struc_dir, f"{struc_id}.pdb")
        dssp_path = os.path.join(struc_dir, f"{struc_id}.dssp")
        config_path = os.path.join(struc_dir, f"{struc_id}.inp")
        out_path = os.path.join(struc_dir, f"{struc_id}.out")

        # GET STRUCTURE LENGTH
        struc = md.load(pdb_path)
        
        # WRITE CONFIG
        print(pdb_path)
        print(dssp_path)
        config.CRDPATH = pdb_path
        config.DSSPPATH = dssp_path
        config.DCDPATHS = [dcd_path]
        config.R2MAXFIT = struc.xyz.shape[0]
        
        config.write(config_path)

        # RUN TEST

        run_test(
            input_path = config_path,
            out_path = out_path,
            struc_dir = struc_dir,
            struc_id = struc_id,
            timing_dict = reach_t,
            reach = reach,
            n_repeat = 5
        )

        save_timing_dict(
            timing_dict = reach_t,
            out_path = os.path.join(timing_dir, "reach_t.json")
        )

if __name__ == "__main__":

    timing_dir = "timing"
    traj_dir_path = "trajectories"
    r_choice = "prod_R1"

    reach_exec_path = "/home/nag/repos/reach_testing/reach_cpu/source/reach"
    
    test_run_reach(
        traj_dir_path = traj_dir_path,
        timing_dir = timing_dir,
        r_choice = r_choice,
        reach_exec_path = reach_exec_path
    )