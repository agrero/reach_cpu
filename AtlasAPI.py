import requests
import tarfile
import zipfile
from pathlib import Path

class AtlasApi:

    def __init__(self) -> None:

        self.base_url = "https://www.dsimb.inserm.fr/ATLAS/api/ATLAS/protein"
        self.zip_chunk_size = 10485760 

    def __call__(self, pdb_chain_id:str, output_dir:str):

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        url = f"{self.base_url}/{pdb_chain_id}"
        req = requests.get(url=url, stream=True)
        req.raise_for_status()

        zip_path = out_path / f"{pdb_chain_id}.zip"

        with open(zip_path, "wb") as f:
            for chunk in req.iter_content(chunk_size=self.zip_chunk_size):
                f.write(chunk)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(out_path)

        zip_path.unlink()


if __name__ == "__main__":

    pdb_chain_ids = [
        # "1ab1",
        # "1a62",
        # "1ah7",
        # "4ny3",
        # "1s9r",
        # "2qcu",
        # "1ikp",
        # "6lrd",
        # "4ys0",
        # "3l4p",
        # "7zh9",
        # "2po4",
        "6qfk",
        "6sup"
    ]
    pdb_chain_ids = [f"{chain}_A" for chain in pdb_chain_ids]

    atlas = AtlasApi()

    for chain_id in pdb_chain_ids:
        out_dir = f"./trajectories/{chain_id}"
        atlas(chain_id, out_dir)