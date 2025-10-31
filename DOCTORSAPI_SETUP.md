# 🩺 DoctorsAPI Integration Setup Guide

## 🔑 Step 1: Configure Your API Key

### Backend Configuration
1. **Copy the environment file**:
   ```bash
   cd doctor-recommender-backend
   cp .env.example .env
   ```

2. **Edit the .env file** and replace `your_actual_api_key_here` with your real API key:
   ```
   DOCTORS_API_KEY=your_actual_api_key_here
   ```

### Frontend Configuration (Alternative)
If you prefer to configure the API key in the frontend:

1. **Edit the frontend API file**:
   ```javascript
   // In doctor-recommender-frontend/src/api/doctorsApiIntegration.js
   const DOCTORS_API_CONFIG = {
     baseUrl: 'https://doctorsapi.com/api',
     apiKey: 'hk_mdx8spuncb661490ec7475302aea4f8a51dc9d7f2c1d29cb92ec23d0163f69c80bf7f972', // Replace this
     // ...
   };
   ```

## 🚀 Step 2: Test the Integration

### Quick Test
1. **Start all services**:
   ```bash
   # Terminal 1 - ML Service
   cd ml-doctor-recommender
   python simple_api.py

   # Terminal 2 - Backend
   cd doctor-recommender-backend
   node server.js

   # Terminal 3 - Frontend
   cd doctor-recommender-frontend
   npm start
   ```

2. **Test the system**:
   - Go to: http://localhost:3000/test
   - Click "Test Backend API"
   - Look for "DoctorsAPI returned X doctors" in the console

### Expected Behavior
- ✅ **With valid API key**: You'll see real doctors from DoctorsAPI
- ⚠️ **With invalid/missing API key**: System falls back to local mock data
- ❌ **If both fail**: Shows minimal fallback doctors

## 🔍 Step 3: Verify Integration

### Check Backend Logs
Look for these messages in your backend terminal:
```
🔍 Attempting to fetch doctors from DoctorsAPI...
📡 Backend: DoctorsAPI URL: https://doctorsapi.com/api/doctors
✅ DoctorsAPI returned 5 doctors
```

### Check Frontend Console
Open browser console (F12) and look for:
```
🔍 Searching DoctorsAPI for specialty: Cardiology
✅ DoctorsAPI returned 3 doctors (page 1 of total 15)
```

## 🛠️ Step 4: Customize the Integration

### Modify Search Parameters
Edit `doctor-recommender-backend/utils/doctorsApiService.js`:

```javascript
// Add more search parameters
const params = {
  specialty: specialty,
  limit: Math.min(limit, 25),
  page: 1,
  // Add these for more specific searches:
  state: 'NY',           // Filter by state
  city: 'New York',      // Filter by city
  radius: 10,            // Search radius in miles
  // credential: 'MD',   // Filter by credentials
};
```

### Add Location-Based Search
```javascript
// In the frontend, you can pass location:
const doctors = await searchDoctorsBySpecialty('Cardiology', 'New York, NY');
```

## 📊 Step 5: Monitor API Usage

### Check API Responses
The system logs detailed information about API calls:
- Request URLs and parameters
- Response status and data
- Error messages and fallbacks

### Rate Limiting
DoctorsAPI may have rate limits. The system handles this by:
- Using timeouts (10 seconds)
- Falling back to local data on errors
- Caching results (can be implemented)

## 🔧 Troubleshooting

### Common Issues

**Issue**: "DoctorsAPI error: 401 - Unauthorized"
**Solution**: Check your API key in the .env file

**Issue**: "DoctorsAPI error: 429 - Too Many Requests"
**Solution**: You've hit the rate limit, wait and try again

**Issue**: "No doctors returned from DoctorsAPI"
**Solution**: The specialty name might not match. Try broader terms like "Internal Medicine" instead of "Cardiology"

**Issue**: "Network error"
**Solution**: Check internet connection and API endpoint

### Debug Mode
Enable detailed logging by setting:
```javascript
// In doctorsApiService.js
console.log('📡 Backend: DoctorsAPI URL:', url, params);
```

## 🎯 Expected Results

Once properly configured, you should see:

### Disease Predictions
- Heart Disease - 85.0% - Cardiology
- Tension Headache - 85.0% - Family Medicine

### Real Doctors from DoctorsAPI
- Dr. Sarah Johnson - Cardiology - New York, NY
- Dr. Michael Chen - Cardiology - Brooklyn, NY
- Dr. Emily Rodriguez - Neurology - Manhattan, NY

### Enhanced Information
- Phone numbers, addresses, credentials
- NPI numbers, organization IDs
- Specialties and ratings

## 🚀 Next Steps

1. **Test with your API key**
2. **Verify real doctors appear**
3. **Customize search parameters**
4. **Add location-based filtering**
5. **Implement caching for better performance**

Your enhanced doctor recommender system will now show real doctors from DoctorsAPI! 🎉
