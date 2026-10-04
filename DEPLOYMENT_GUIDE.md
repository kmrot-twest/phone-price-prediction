# Deployment Guide

## Files You Have Now

After the rebuild, your project folder looks like:

```
D:\Projects\Mobile Price Range\
├── venv\                          # Virtual environment (don't commit)
├── models\
│   ├── phone_price_pipeline.pkl
│   └── phone_price_pipeline_no_brand.pkl
├── main.py                        # Local development server
├── index.html                     # Frontend
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation
```

## Step 1: Prepare for GitHub

### 1a. Create the API folder for Vercel
Vercel needs serverless functions in an `/api` folder. Create it:

```bash
mkdir api
```

Then move the provided `api_index.py` file to `api/index.py`:

```bash
# On Windows
move api_index.py api\index.py

# On macOS/Linux
mv api_index.py api/index.py
```

Your structure is now:

```
D:\Projects\Mobile Price Range\
├── venv\
├── models\
│   ├── phone_price_pipeline.pkl
│   └── phone_price_pipeline_no_brand.pkl
├── api\
│   └── index.py                   # Vercel serverless function
├── main.py                        # Local dev only
├── index.html
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

### 1b. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: Phone price predictor"
```

### 1c. Create GitHub repo

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository (name it `phone-price-predictor`)
3. Don't initialize with README (you already have one)
4. Copy the commands it shows and run them:

```bash
git remote add origin https://github.com/yourusername/phone-price-predictor.git
git branch -M main
git push -u origin main
```

Done! Your code is now on GitHub.

## Step 2: Deploy to Vercel

### 2a. Sign up (if needed)

Go to [vercel.com](https://vercel.com) and sign up with your GitHub account.

### 2b. Import your repo

1. Click **"New Project"**
2. Click **"Import Git Repository"**
3. Select your `phone-price-predictor` repo
4. Vercel auto-detects the `vercel.json` config
5. Click **"Deploy"**

Wait 2–3 minutes. Your app is live!

### 2c. Find your live URL

After deployment succeeds, you'll see a URL like `https://phone-price-predictor-abc123.vercel.app`. That's your live app.

## Step 3: Test

### Local (before pushing)
```bash
uvicorn main:app --reload
```

Open `http://localhost:8000` and test.

### Live (after deploying to Vercel)
Open your Vercel URL and test.

## How It Works

- **Local**: Uses `main.py` to run a regular FastAPI server.
- **Vercel**: Uses `api/index.py` (the same code, just named for Vercel's serverless format) and deploys it as functions.

Both load the same model and serve the same `index.html` frontend.

## Important Notes

### Don't commit:
- `venv/` folder (excluded by `.gitignore`)
- `__pycache__/` (excluded by `.gitignore`)
- Any `.env` files with secrets

### DO commit:
- `models/` folder with the `.pkl` files
- All Python files
- `index.html`
- `requirements.txt`
- `vercel.json`

### Model file size:
Each `.pkl` is ~20 MB, total ~40 MB. Vercel's limit is 512 MB, so you're fine.

## Troubleshooting

### Git error: "main.py" too large?
The `.pkl` files are in `models/`, not `main.py`. Make sure `models/` is in your repo.

### Vercel says "Module not found"?
Check that `requirements.txt` has all the packages and `models/` folder was pushed to GitHub.

### Vercel deploy is slow?
First deploy can take 2–3 minutes. Subsequent deploys are faster.

### Live site loads but shows error?
Check Vercel's function logs:
1. Go to your Vercel dashboard
2. Select your project
3. Go to "Functions" tab
4. Check the logs

## Making Changes Later

After you've deployed:

```bash
# Make changes to any file
# ...

# Push to GitHub
git add .
git commit -m "Your change description"
git push

# Vercel auto-deploys within 1–2 minutes
```

No manual redeploy needed!

## Questions?

- Vercel docs: https://vercel.com/docs
- FastAPI docs: https://fastapi.tiangolo.com
- GitHub docs: https://docs.github.com
