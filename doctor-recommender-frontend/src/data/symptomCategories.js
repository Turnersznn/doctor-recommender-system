// Comprehensive Symptom Categories for Better User Experience
export const SYMPTOM_CATEGORIES = {
  "Respiratory": {
    icon: "🫁",
    color: "#3B82F6",
    symptoms: [
      "cough", "breathlessness", "shortness_of_breath", "chest_pain", 
      "wheezing", "sputum", "throat_irritation", "sore_throat", 
      "runny_nose", "nasal_congestion", "sneezing"
    ]
  },
  "Digestive": {
    icon: "🍽️",
    color: "#10B981",
    symptoms: [
      "nausea", "vomiting", "diarrhoea", "constipation", "abdominal_pain",
      "stomach_pain", "loss_of_appetite", "indigestion", "bloating",
      "heartburn", "acid_reflux", "bloody_stool"
    ]
  },
  "Neurological": {
    icon: "🧠",
    color: "#8B5CF6",
    symptoms: [
      "headache", "dizziness", "seizures", "confusion", "memory_loss",
      "blurred_and_distorted_vision", "visual_disturbances", "hearing_loss",
      "numbness", "tingling", "weakness", "paralysis"
    ]
  },
  "Cardiovascular": {
    icon: "❤️",
    color: "#EF4444",
    symptoms: [
      "chest_pain", "palpitations", "fast_heart_rate", "irregular_heartbeat",
      "breathlessness", "swelling", "leg_swelling", "fatigue", "dizziness"
    ]
  },
  "Musculoskeletal": {
    icon: "🦴",
    color: "#F59E0B",
    symptoms: [
      "joint_pain", "back_pain", "muscle_weakness", "muscle_pain",
      "stiffness", "swelling_joints", "neck_pain", "shoulder_pain",
      "knee_pain", "hip_pain"
    ]
  },
  "Skin & Dermatological": {
    icon: "🧴",
    color: "#EC4899",
    symptoms: [
      "skin_rash", "itching", "redness_of_eyes", "skin_peeling",
      "dry_skin", "acne", "bruising", "skin_discoloration",
      "wounds", "ulcers"
    ]
  },
  "Mental Health": {
    icon: "🧘",
    color: "#6366F1",
    symptoms: [
      "anxiety", "depression", "mood_swings", "irritability",
      "sleep_disturbances", "insomnia", "stress", "panic_attacks",
      "concentration_problems"
    ]
  },
  "Endocrine & Metabolic": {
    icon: "⚖️",
    color: "#14B8A6",
    symptoms: [
      "irregular_sugar_level", "excessive_hunger", "excessive_thirst",
      "frequent_urination", "weight_loss", "weight_gain", "fatigue",
      "heat_intolerance", "cold_intolerance"
    ]
  },
  "Genitourinary": {
    icon: "🚻",
    color: "#F97316",
    symptoms: [
      "painful_urination", "burning_micturition", "blood_in_urine",
      "dark_urine", "frequent_urination", "urinary_incontinence",
      "abnormal_menstruation", "pelvic_pain"
    ]
  },
  "General Symptoms": {
    icon: "🌡️",
    color: "#6B7280",
    symptoms: [
      "fever", "mild_fever", "high_fever", "fatigue", "weakness",
      "night_sweats", "sweating", "chills", "malaise", "body_aches"
    ]
  },
  "Eye & Vision": {
    icon: "👁️",
    color: "#0EA5E9",
    symptoms: [
      "eye_pain", "redness_of_eyes", "blurred_vision", "halos_around_lights"
    ]
  },
  "Ear, Nose & Throat": {
    icon: "👂",
    color: "#84CC16",
    symptoms: [
      "hearing_loss", "ear_pain", "tinnitus", "sore_throat",
      "throat_irritation", "runny_nose", "nasal_congestion",
      "loss_of_smell", "loss_of_taste"
    ]
  },
  "Dental & Oral Health": {
    icon: "🦷",
    color: "#8B5CF6",
    symptoms: [
      "toothache", "tooth_sensitivity", "jaw_pain", "facial_swelling",
      "bleeding_gums", "swollen_gums", "bad_breath", "jaw_clicking"
    ]
  }
};

// Severity levels for symptoms
export const SEVERITY_LEVELS = {
  "mild": {
    label: "Mild",
    color: "#10B981",
    description: "Barely noticeable, doesn't interfere with daily activities"
  },
  "moderate": {
    label: "Moderate", 
    color: "#F59E0B",
    description: "Noticeable and somewhat bothersome, may affect some activities"
  },
  "severe": {
    label: "Severe",
    color: "#EF4444", 
    description: "Very bothersome, significantly affects daily activities"
  }
};

// Function to get category for a symptom
export const getSymptomCategory = (symptom) => {
  for (const [categoryName, categoryData] of Object.entries(SYMPTOM_CATEGORIES)) {
    if (categoryData.symptoms.includes(symptom)) {
      return {
        name: categoryName,
        ...categoryData
      };
    }
  }
  return {
    name: "Other",
    icon: "❓",
    color: "#6B7280",
    symptoms: []
  };
};

// Function to organize symptoms by category
export const organizeSymptomsByCategory = (symptoms) => {
  const organized = {};
  
  symptoms.forEach(symptom => {
    const category = getSymptomCategory(symptom);
    if (!organized[category.name]) {
      organized[category.name] = {
        ...category,
        symptoms: []
      };
    }
    organized[category.name].symptoms.push(symptom);
  });
  
  return organized;
};

// Common symptom display names
export const SYMPTOM_DISPLAY_NAMES = {
  "itching": "Itching",
  "skin_rash": "Skin Rash", 
  "cough": "Cough",
  "headache": "Headache",
  "chest_pain": "Chest Pain",
  "abdominal_pain": "Abdominal Pain",
  "nausea": "Nausea",
  "vomiting": "Vomiting",
  "diarrhoea": "Diarrhea",
  "constipation": "Constipation",
  "joint_pain": "Joint Pain",
  "back_pain": "Back Pain",
  "muscle_weakness": "Muscle Weakness",
  "fatigue": "Fatigue",
  "dizziness": "Dizziness",
  "breathlessness": "Shortness of Breath",
  "palpitations": "Heart Palpitations",
  "loss_of_appetite": "Loss of Appetite",
  "weight_loss": "Weight Loss",
  "weight_gain": "Weight Gain",
  "anxiety": "Anxiety",
  "depression": "Depression",
  "irregular_sugar_level": "Irregular Blood Sugar",
  // Dental symptoms
  "tooth_pain": "Tooth Pain",
  "toothache": "Toothache",
  "tooth_sensitivity": "Tooth Sensitivity",
  "dental_pain": "Dental Pain",
  "gum_pain": "Gum Pain",
  "jaw_pain": "Jaw Pain",
  "bleeding_gums": "Bleeding Gums",
  "swollen_gums": "Swollen Gums",
  "bad_breath": "Bad Breath",
  "mouth_sores": "Mouth Sores",
  "broken_tooth": "Broken Tooth",
  "wisdom_tooth_pain": "Wisdom Tooth Pain",
  // Eye symptoms
  "eye_pain": "Eye Pain",
  "double_vision": "Double Vision",
  "vision_loss": "Vision Loss",
  "eye_redness": "Eye Redness",
  "eye_discharge": "Eye Discharge",
  "dry_eyes": "Dry Eyes",
  "light_sensitivity": "Light Sensitivity",
  "floaters": "Floaters",
  "flashing_lights": "Flashing Lights",
  "watering_from_eyes": "Watery Eyes",
  "sunken_eyes": "Sunken Eyes",
  "pain_behind_the_eyes": "Pain Behind Eyes",
  "excessive_hunger": "Excessive Hunger",
  "abnormal_menstruation": "Irregular Periods",
  "burning_micturition": "Painful Urination",
  "dark_urine": "Dark Urine",
  "sweating": "Excessive Sweating",
  "fever": "Fever",
  "mild_fever": "Mild Fever",
  "high_fever": "High Fever",
  "blurred_and_distorted_vision": "Blurred Vision",
  "redness_of_eyes": "Red Eyes",
  "hearing_loss": "Hearing Loss",
  "throat_irritation": "Sore Throat",
  "runny_nose": "Runny Nose",
  "swelling_joints": "Joint Swelling",
  "night_sweats": "Night Sweats",
  "blood_in_urine": "Blood in Urine",
  "painful_urination": "Painful Urination",
  "visual_disturbances": "Vision Problems",
  "sore_throat": "Sore Throat",
  "red_eyes": "Red Eyes",
  "fast_heart_rate": "Rapid Heart Rate",
  "shortness_of_breath": "Shortness of Breath"
};

// Function to get display name for symptom
export const getSymptomDisplayName = (symptom) => {
  return SYMPTOM_DISPLAY_NAMES[symptom] || symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};
