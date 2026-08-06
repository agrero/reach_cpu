import mdtraj as md

import os
from typing import Literal, Any, List
import subprocess

Binary = Literal[0, 1]

class ReachConfig:
    def __init__(
        self,
        NCRDFMT : Binary = 0,
        CRDPATH : str = "mb_ca.pdb",
        NSECOND : Binary = 1,
        DSSPPATH : str = "1a6g.dssp",
        DCDPATHS : List[str] = ["mb_ca.dcd"],
        TRALEN : float = 1000.0,
        NCRYSTAL : Binary = 0,
        TEMPERA : float = 120.0,
        RBINFIT : float = 1.0,
        RMINFIT : float = 6.0,
        RMAXFIT : float = 12.0,
        NSLOW : Binary = 1,
        R2MINFIT : float = 11.0,
        R2MAXFIT : float = 20.0,
        NARROW : Literal[0, 1, 2] = 1,
        NMAMODE : int = 1
    ):
        """Python Class for REACH data input

        Parameters
        ----------
        NCRDFMT : 'Binary'
            1.CHRAMM 0.PDB coordinate file format
        CRDPATH : 'str' 
            ref coordinates path/filename.crd,pdb
        NSECOND : 'Binary'
            1.yes  0.no include secondary structure information?
        DSSPPATH : 'str'
            DSSP file path/filename.dssp
        NUMDCD : 'int'
            number of dcd files
        DCDPATHS : 'List["str"]'
            dcd files [path/filename1.dcd, path/filename2.dcd]
        TRALEN : 'float'
            trajectory length for each dcd file [ps] 
        NCRYSTAL : 'Binary'
            1.yes  0.no  dcd(s) include crystal information?
        TEMPERA : 'float'
            temperatue at which MD simulation was performed 
        RBINFIT : 'float'
            bin length for average
        RMINFIT : 'float'
            minimum length for fitting 
        RMAXFIT : 'float'
            maximum length for fitting 
        NSLOW : 'Binary'
            1.yes  0.no fitting using additional slower component?
        R2MINFIT : 'float'
            minimum length for slower component fitting 
        R2MAXFIT : 'float'
            maximum length for slower component fitting 
        NARROW : 'Literal[0,1,2]'
            0.no  1. draw molscript normal-mode vector 2. generate dcd for normal-mode motion
        NMAMODE : 'int'
            number of normal-mode for drawing
        """
        
        self.NCRDFMT = NCRDFMT
        self.CRDPATH = CRDPATH
        self.NSECOND = NSECOND
        self.DSSPPATH = DSSPPATH
        self.DCDPATHS = DCDPATHS
        self.TRALEN = TRALEN
        self.NCRYSTAL = NCRYSTAL
        self.TEMPERA = TEMPERA
        self.RBINFIT = RBINFIT
        self.RMINFIT = RMINFIT
        self.RMAXFIT = RMAXFIT
        self.NSLOW = NSLOW
        self.R2MINFIT = R2MINFIT
        self.R2MAXFIT = R2MAXFIT
        self.NARROW = NARROW
        self.NMAMODE = NMAMODE

    def _format_key_value(self, key:str, value:Any) -> str:
        return f"{key} = {value}"

    def format_dict(self) -> str:     

        lines = []
        for key, value in self.__dict__.items():
            # unpack DCDPATHS
            if key == "DCDPATHS":

                lines.append(self._format_key_value("NUMDCD", len(self.DCDPATHS)))
                lines.append("!DCDPATH(n)")
                for ndx, line in enumerate(self.DCDPATHS):
        
                    lines.append(
                        self._format_key_value(f"DCDPATH(n)", line)
                    )

            else:

                lines.append(self._format_key_value(key, value))

        return "\n".join(lines)
    
    def write(self, path:str) -> None:
        with open(path, "w") as w:
            w.write(str(self))

    def __str__(self):
        return self.format_dict()

class Reach:
    def __init__(
            self,
            reach_path : str
        ) -> None:

        self.reach_path = reach_path

    def run(self, input_path:str, out_path:str, output_dir:str) -> None:

        os.makedirs(output_dir, exist_ok=True)

        abs_input = os.path.abspath(input_path)
        abs_out = os.path.abspath(out_path)

        with open(abs_input, "r") as stdin_file:
            with open(abs_out, "w") as stdout_file:

                subprocess.run(
                    args = [self.reach_path],
                    stdin = stdin_file,
                    stdout = stdout_file,
                    cwd = output_dir
                )

    def convert_xtc_to_dcd(self, xtc_path:str, dcd_path:str, pdb_path:str) -> None:
        md.load(xtc_path, top=pdb_path).save_dcd(dcd_path)

if __name__ == "__main__":

    test_dir = os.path.join("..", "test")

    reach_exec_path = os.path.join("..", "source", "reach")
    
    output_dir = os.path.join("test_out")
    reach_input_path = os.path.join(output_dir, "pyreach.inp")
    reach_out_path = os.path.join(output_dir, "pyreach.out")

    config = ReachConfig(
        CRDPATH=os.path.join(test_dir, "mb_ca.pdb"),
        DSSPPATH=os.path.join(test_dir, "1a6g.dssp"),
        DCDPATHS=[os.path.join(test_dir, "mb_ca.dcd")],
    )
    config.write(os.path.join(output_dir, "pyreach.inp"))

    reach = Reach(reach_exec_path)
    reach.run(reach_input_path, reach_out_path, output_dir)