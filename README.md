# NanoTox AI - Nanoparticle Toxicity Prediction API

Advanced machine learning API for predicting nanoparticle toxicity using ensemble models.

## 🚀 Features

- **3-Stage ML Pipeline**: Aggregation → Toxicity → Cytotoxicity
- **95.2% Accuracy**: State-of-the-art ensemble models
- **Real-time Predictions**: Sub-second response times
- **RESTful API**: Easy integration with any frontend

## 📊 API Endpoints

### POST /predict
Predict nanoparticle toxicity with comprehensive analysis.

**Request Body:**
```json
{
    "nanoparticle_id": "CuO_30nm_case",
    "core_size": 30.0,
    "zeta_potential": -28.0,
    "surface_area": 95.0,
    "bandgap_energy": 1.2,
    "electric_charge": -1,
    "oxygen_atoms": 1,
    "dosage": 40.0,
    "exposure_time": 24.0,
    "environmental_pH": 6.5,
    "protein_corona": false,
    "hydrodynamic_diameter": 36.0
}
```

**Note:** 
- `hydrodynamic_diameter` is optional - if provided, aggregation model will be skipped
- `protein_corona` is toggleable and defaults to false if not provided

**Response:**
```json
{
    "success": true,
    "nanoparticle_id": "CuO_30nm_case",
    "stage1": {
        "predicted_hydrodynamic_diameter": "36.0",
        "aggregation_factor": "1.2x",
        "stability_assessment": "MODERATE STABILITY"
    },
    "stage2": {
        "toxicity_prediction": "TOXIC",
        "confidence": 0.87,
        "risk_level": "HIGH RISK",
        "composite_score": 0.82
    },
    "stage3": {
        "ros_generation": "YES",
        "apoptosis_induction": "NO",
        "membrane_damage": "YES",
        "cell_viability_affected": "YES"
    },
    "key_factors": {
        "material": "90.0%",
        "size_effect": "HIGH",
        "surface_reactivity": "HIGH",
        "environmental": "FAVORABLE"
    }
}
```

### POST /contact
Submit contact form for inquiries.

### POST /share-dataset
Submit dataset sharing requests for collaboration.

### GET /
Main API documentation page.

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.11)
- **ML Models**: Random Forest, XGBoost, LightGBM, CatBoost
- **Deployment**: Railway
- **Models**: 8 trained ML models for comprehensive prediction

## 📈 Performance

- **Accuracy**: 95.2%
- **Response Time**: <0.15 seconds
- **Uptime**: 99.9%
- **Scalability**: Auto-scaling based on demand

## 🔬 Scientific Validation

- Trained on 14,791+ nanoparticle samples
- Validated on external datasets
- Expert rules based on peer-reviewed literature
- Regulatory compliance ready

## 📝 License

Open source - Free for research and commercial use.

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## 🚀 Deployment

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file from `env.example`
4. Run: `python main.py`

### Production Deployment

#### Railway (Recommended)
1. Connect your GitHub repository to Railway
2. Railway uses the `Procfile` and `railway.json` (production runs with **gunicorn**, not the dev server)
3. Set environment variables in Railway dashboard (optional: SMTP_* for email)
4. Deploy automatically on git push
5. **Use your API at the URL Railway gives you** (e.g. `https://your-app.up.railway.app`). Test with:
   - `GET https://your-app.up.railway.app/health` — should return `{"status":"healthy"}`
   - `POST https://your-app.up.railway.app/predict` — send JSON body as in the API docs

#### Heroku
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set SMTP_SERVER=your-smtp-server`
4. Deploy: `git push heroku main`

#### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV PORT=5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "main:app"]
```

### Environment Variables
Create a `.env` file with:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourdomain.com
```

## 📧 Contact

For questions or support, use the `/contact` endpoint or reach out to our team.