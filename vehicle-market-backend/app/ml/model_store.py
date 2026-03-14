"""
Model store — save and load trained .pkl model files.
"""

import pickle
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models_store"


def save_model(model, name: str = "price_model") -> Path:
    """Persist a trained model to disk as a pickle file."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    path = MODELS_DIR / f"{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(model, f)
    return path


def load_model(name: str = "price_model"):
    """Load a trained model from disk."""
    path = MODELS_DIR / f"{name}.pkl"
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return pickle.load(f)
