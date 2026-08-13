import json

def save_timing_dict(timing_dict:dict, out_path:str, indent:int=4) -> None:
    with open(out_path, "w") as f:
        json.dump(timing_dict, f, indent=indent)
