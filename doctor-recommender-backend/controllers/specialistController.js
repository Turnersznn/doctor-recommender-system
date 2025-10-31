import { getDiagnosesAndSpecialists } from '../utils/contentApi.js';
import fs from 'fs';
import path from 'path';

// Load ratings data
function loadRatings() {
  try {
    const ratingsPath = path.join(process.cwd(), 'data', 'ratings.json');
    const data = fs.readFileSync(ratingsPath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return {
      "ratings": {},
      "reviews": {},
      "statistics": {}
    };
  }
}

// Get doctor identifier
function getDoctorId(doctor) {
  return `${doctor.name}-${doctor.location}`.replace(/\s+/g, '-');
}

// Map model predictions to actual specialist names in the doctor database
const SPECIALIST_MAPPING = {
  // Direct matches
  "Dermatologist": "Dermatology",
  "Dermatologists": "Dermatology",
  "Cardiologist": "Internal Medicine, Cardiovascular Disease",
  "Gastroenterologist": "Internal Medicine, Gastroenterology",
  "Endocrinologist": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
  "Pulmonologist": "Internal Medicine, Pulmonary Disease",
  "Neurologist": "Psychiatry & Neurology, Neurology",  // Only fix this one
  "Allergist": "Allergy & Immunology",
  "Otolaryngologist": "Otolaryngology",
  "Gynecologist": "Obstetrics & Gynecology",
  "Pediatrician": "Pediatrics",
  "Rheumatologists": "Internal Medicine, Rheumatology",
  "Ophthalmologist": "Ophthalmology",
  
  // Close matches
  "Internal Medcine": "Internal Medicine",  // Typo in original data
  "Hepatologist": "Internal Medicine, Gastroenterology",  // Liver specialist
  "Phlebologist": "Internal Medicine, Cardiovascular Disease",  // Vein specialist
  "Osteopathic": "Family Medicine",  // General practice
  "Osteoarthristis": "Internal Medicine, Rheumatology",  // Joint specialist
  "Common Cold": "Family Medicine",  // General practice
};

export const predictSpecialist = async (req, res) => {
  const symptoms = req.body.symptoms;
  if (!symptoms || typeof symptoms !== 'object') {
    return res.status(400).json({ error: 'Symptoms must be provided as an object.' });
  }
  try {
    const diagnoses = await getDiagnosesAndSpecialists(symptoms); // Array of {disease, probability, specialist}
    // Map specialists using SPECIALIST_MAPPING if possible
    const mappedDiagnoses = diagnoses.map(d => ({
      ...d,
      specialist: SPECIALIST_MAPPING[d.specialist] || d.specialist
    }));
    // Optionally, filter doctors for the top specialist
    const topSpecialist = mappedDiagnoses[0]?.specialist;
    let doctors = [];
    if (topSpecialist) {
      const dataPath = path.join(process.cwd(), '..', 'ml-doctor-recommender', 'final_data.json');
      const raw = fs.readFileSync(dataPath, 'utf-8');
      const data = JSON.parse(raw);
      let allDoctors = [];
      for (const entry of data) {
        if (
          Array.isArray(entry) &&
          entry[1] &&
          entry[1].results &&
          Array.isArray(entry[1].results)
        ) {
          allDoctors = allDoctors.concat(entry[1].results);
        }
      }
      doctors = allDoctors
        .map(doc => {
          const taxonomy = (doc.taxonomies || []).find(t => t.primary) || (doc.taxonomies || [])[0];
          const specialty = taxonomy ? taxonomy.desc : '';
          let name = '';
          if (doc.basic) {
            name = doc.basic.organization_name || (doc.basic.first_name ? `${doc.basic.first_name} ${doc.basic.last_name}` : '');
          }
          let location = '';
          if (doc.addresses && Array.isArray(doc.addresses)) {
            const loc = doc.addresses.find(a => a.address_purpose === 'LOCATION');
            if (loc) location = `${loc.address_1 || ''} ${loc.city || ''} ${loc.state || ''}`.trim();
          }
          return { name, specialty, location };
        })
        .filter(doc => doc.specialty && doc.specialty.toLowerCase().includes(topSpecialist.toLowerCase()));
    }
    res.json({
      diagnoses: mappedDiagnoses,
      recommendedDoctors: doctors
    });
  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({ error: 'Server error' });
  }
}; 