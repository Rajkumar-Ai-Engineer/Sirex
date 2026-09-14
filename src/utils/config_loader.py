from pathlib import Path
import yaml 
import os 

def _project_root() ->Path:
    return Path(__file__).resolve().parents[1]   

def load_config(config_path:str | None = None) ->dict:
    if config_path is None:
        config_path = _project_root() / "config" / "config.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = _project_root / path
    if not path.exists():
        raise FileNotFoundError("File is not found or not exists")
    
    with open(file=path,mode="r",encoding="utf-8") as file:
        return yaml.safe_load(file)