"""
Placeholder script for downloading datasets.
Fill in download links / instructions per dataset.
"""

DATASETS = {
    "ai_city_2021_track4": {
        "description": "AI City Challenge 2021 Track 4 — evaluation + Stage 1 tune",
        "url": None,  # requires registration
        "target": "data/raw/ai_city_2021_track4/",
    },
    "so_tad": {
        "description": "SO-TAD — Stage 2 train",
        "url": None,
        "target": "data/raw/so_tad/",
    },
    "cadp": {
        "description": "CADP — Stage 2 train",
        "url": None,
        "target": "data/raw/cadp/",
    },
    "tum_accid3nd": {
        "description": "TUM Accid3nD — Stage 2 train",
        "url": None,
        "target": "data/raw/tum_accid3nd/",
    },
    "floodnet": {
        "description": "FloodNet — Flood model",
        "url": None,
        "target": "data/raw/floodnet/",
    },
}

if __name__ == "__main__":
    for name, info in DATASETS.items():
        print(f"[{name}] {info['description']}")
        if info["url"]:
            print(f"  → {info['url']}")
        else:
            print("  → URL not yet configured. Add manually.")
