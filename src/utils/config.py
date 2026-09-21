"""Utility helpers for loading OmegaConf YAML configs."""
from pathlib import Path
from omegaconf import OmegaConf, DictConfig


def load_config(path: str | Path) -> DictConfig:
    """Load a YAML config file and return an OmegaConf DictConfig."""
    return OmegaConf.load(path)


def merge_configs(*paths: str | Path) -> DictConfig:
    """Merge multiple YAML config files (later files override earlier)."""
    cfgs = [OmegaConf.load(p) for p in paths]
    return OmegaConf.merge(*cfgs)
