# 📱 Phone Price Predictor

A web app that predicts phone prices based on specifications using a trained Random Forest model.

## Features

- **Beautiful slider interface** - Full-width sliders with number inputs for precise control
- **Smart pricing tiers** - Shows single price, ±₹500 range, or ±₹2,500 range based on predicted value
- **Responsive design** - Works on desktop, tablet, and mobile
- **Fast predictions** - Real-time price estimation

## Tech Stack

- **Backend**: FastAPI + scikit-learn
- **Frontend**: HTML + CSS + Vanilla JavaScript
- **Deployment**: Vercel (serverless)

## Local Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phone-price-predictor.git
   cd phone-price-predictor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure models are in place**
   ```
   models/
   ├── phone_price_pipeline.pkl
   └── phone_price_pipeline_no_brand.pkl
   ```

5. **Run locally**
   ```bash
   uvicorn main:app --reload
   ```
   
   Open `http://localhost:8000` in your browser.

## Project Structure

```
phone-price-predictor/
├── main.py                      # FastAPI app (local development)
├── api/
│   └── index.py                 # FastAPI app (Vercel serverless)
├── index.html                   # Frontend (HTML + CSS + JS)
├── models/
│   ├── phone_price_pipeline.pkl
│   └── phone_price_pipeline_no_brand.pkl
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

## How It Works

1. User enters phone specifications via sliders or number inputs
2. Frontend sends data as JSON to `/predict` endpoint
3. Backend loads model and predicts price
4. Price range is calculated based on tiers:
   - **Under ₹2,500**: Single value only
   - **₹2,500 – ₹5,000**: ±₹500 range
   - **Over ₹5,000**: ±₹2,500 range
5. Result displays at the bottom of the page

## Deployment on Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier works)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your GitHub repository
   - Vercel auto-detects `vercel.json` config
   - Click "Deploy"

3. **That's it!** Your app is live

### Important Notes for Vercel

- Model files are included in the deployment (total ~40 MB, within Vercel's 512 MB limit)
- Serverless functions have a default 10-second timeout (extended to 60 seconds in `vercel.json`)
- First request may take a few seconds (cold start) as the model loads
- Subsequent requests are fast

## API Endpoints

### GET `/`
Returns the HTML frontend.

### POST `/predict`
Accepts JSON with phone specs, returns predicted price.

**Request:**
```json
{
  "screen_size": 6.1,
  "refresh_rate": 90,
  "resolution_width": 1080,
  "resolution_height": 2400,
  "ram_gb": 8,
  "storage_gb": 128,
  "cpu_cores": 8,
  "cpu_speed": 2.8,
  "rear_camera_mp": 50,
  "front_camera_mp": 16,
  "rear_camera_count": 2,
  "battery_mah": 5000,
  "charging_w": 33,
  "has_5g": 1,
  "has_4g": 1,
  "has_3g": 1,
  "has_wifi": 1,
  "has_nfc": 0
}
```

**Response (single price):**
```json
{
  "mode": "single",
  "value": 24500
}
```

**Response (range):**
```json
{
  "mode": "range",
  "low": 24900,
  "high": 29900
}
```

## Troubleshooting

### Local: "Module not found" errors
```bash
pip install -r requirements.txt
```

### Local: Model not loading
Ensure `models/phone_price_pipeline_no_brand.pkl` exists in the models folder.

### Vercel: 502 Bad Gateway
Usually a cold start timeout. Wait 30 seconds and try again. Consider upgrading Vercel plan for faster cold starts.

### Vercel: Model file not found
Check that the `models/` folder is committed to GitHub. `.gitignore` should NOT exclude `models/`.

## Development

### Testing Locally
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"screen_size": 6.1, "refresh_rate": 90, ...}'
```

### Updating Dependencies
```bash
pip freeze > requirements.txt
```

## License

MIT

## Author

Built with ❤️ for phone enthusiasts.
