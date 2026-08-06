import subprocess

import os

class PyDssp:

    def __init__(self, dssp_path:str="mkdssp") -> None:
        
        self.dssp_path = dssp_path

    def __call__(self, pdb_in:str, out_path:str):

        abs_out = os.path.abspath(out_path)

        with open(abs_out, "w") as stdout_file:

            subprocess.run(
                args = ["mkdssp", "-i", pdb_in, "-o", out_path],
                stdout=stdout_file
            )

if __name__ == "__main__":
    
    pdb_path = os.path.join("trajectories", "1a62_A", "1a62_A.pdb")

    pydssp = PyDssp("mkdssp")

    pydssp(pdb_path, "dssp_test.dssp")