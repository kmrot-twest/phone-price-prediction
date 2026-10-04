from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()

# Load model once at startup
try:
    model = joblib.load(BASE_DIR / "models" / "phone_price_pipeline_no_brand.pkl")
    EXPECTED_COLUMNS = list(model.feature_names_in_)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    EXPECTED_COLUMNS = []


class PhoneSpec(BaseModel):
    screen_size: float
    refresh_rate: float
    resolution_width: float
    resolution_height: float
    ram_gb: float
    storage_gb: float
    cpu_cores: float
    cpu_speed: float
    rear_camera_mp: float
    front_camera_mp: float
    rear_camera_count: float
    battery_mah: float
    charging_w: float
    has_5g: int
    has_4g: int
    has_3g: int
    has_wifi: int
    has_nfc: int


def build_result(price: float) -> dict:
    """Under 2,500: single value. Under 5,000: +/-500. Otherwise: +/-2,500."""
    price = max(price, 0.0)

    if price < 2500:
        return {"mode": "single", "value": int(round(price, -1))}

    spread = 500 if price < 5000 else 2500
    return {
        "mode": "range",
        "low": int(round(max(price - spread, 0), -2)),
        "high": int(round(price + spread, -2)),
    }


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "index.html", media_type="text/html")


@app.post("/predict")
def predict(spec: PhoneSpec):
    if model is None:
        return {"error": "Model not loaded"}
    
    # Build row with all expected columns
    row = {col: np.nan for col in EXPECTED_COLUMNS}
    row.update(spec.model_dump())

    X = pd.DataFrame([row], columns=EXPECTED_COLUMNS)
    price = float(model.predict(X)[0])

    return build_result(price)
