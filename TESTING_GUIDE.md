# Content-Based Filtering Testing Guide

## Prerequisites
1. Start backend server: `cd doctor-recommender-backend && npm start`
2. Start ML service: `cd ml-doctor-recommender && python multi_symptom_api.py`

## Test Scenarios

### Scenario 1: New User (No Preferences)
```bash
curl -X POST http://localhost:5000/api/specialist/enhanced-predict \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": {"eye_pain": true, "blurred_vision": true},
    "userId": "newuser001"
  }'
```
**Expected**: Basic recommendations, no personalization

### Scenario 2: Update User Preferences
```bash
curl -X POST http://localhost:5000/api/preferences/update \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "newuser001",
    "doctorId": "1605678901",
    "rating": 5,
    "specialty": "Ophthalmology",
    "doctorFeatures": {"gender": "M", "location": "Lagos"}
  }'
```
**Expected**: Success message

### Scenario 3: Get Personalized Recommendations
```bash
curl -X POST http://localhost:5000/api/specialist/enhanced-predict \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": {"eye_pain": true, "redness_of_eyes": true},
    "userId": "newuser001"
  }'
```
**Expected**: Higher scores for male doctors in Lagos

### Scenario 4: Check User Profile
```bash
curl http://localhost:5000/api/preferences/newuser001
```
**Expected**: User preferences with Ophthalmology specialty

## What to Look For

### ✅ Content-Based Features Working:
- `contentScore` field in doctor responses
- `recommendationReason` explaining why doctor was recommended
- Higher scores for doctors matching user preferences
- Different recommendations for different users

### ✅ Learning Behavior:
- User preferences update after ratings
- Preferred specialties added after positive ratings
- Gender/location preferences learned from high-rated doctors

### ✅ Personalization:
- Same symptoms → different doctor rankings for different users
- Recommendation reasons mention user preferences
- Content scores vary based on user profile

## Quick Test Commands

```bash
# Run automated test
node test_content_based.js

# Test with Postman/Insomnia
POST /api/specialist/enhanced-predict
{
  "symptoms": {"toothache": true, "jaw_pain": true},
  "userId": "dentist_lover"
}

# Rate a dentist highly
POST /api/preferences/update
{
  "userId": "dentist_lover",
  "doctorId": "1234567890",
  "rating": 5,
  "specialty": "Dentist, General Practice"
}

# Get recommendations again - should prefer dentists
POST /api/specialist/enhanced-predict
{
  "symptoms": {"bleeding_gums": true},
  "userId": "dentist_lover"
}
```