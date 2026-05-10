from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict_demand

app = FastAPI(
    title="Real-Time Operations Intelligence API",
    description="Predicts high operational demand using weather, IoT, geospatial, and capacity features.",
    version="1.0"
)

class DemandInput(BaseModel):
    latitude: float
    longitude: float
    historical_job_volume: int
    avg_response_time_minutes: int
    estimated_revenue_exposure: int
    rainfall_24hr: float
    wind_speed_max: float
    storm_severity_score: float
    moisture_sensor_avg: float
    humidity_sensor_avg: float
    sensor_alert_count: int
    crew_availability: int
    equipment_units_available: int
    current_workload: int
    capacity_gap: int
    equipment_gap: int
    weather_risk_index: float
    sensor_risk_index: float
    operational_pressure_score: float
    revenue_exposure_level: str

@app.get("/")
def home():
    return {"message": "Real-Time Operations Intelligence API is running."}

@app.post("/predict")
def predict(input_data: DemandInput):
    result = predict_demand(input_data.dict())
    return result