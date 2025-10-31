// User Profile for Content-Based Filtering
export class UserProfile {
  constructor(userId) {
    this.userId = userId;
    this.preferences = {
      preferredSpecialties: [], // ["Cardiology", "Internal Medicine"]
      doctorAttributes: {
        gender: null, // "M" or "F" 
        experience: null, // "high", "medium", "low"
        location: null, // preferred city/state
        hospital: null // preferred hospital type
      },
      pastConsultations: [], // history of specialists visited
      ratings: {}, // doctorId -> rating
      medicalHistory: [] // chronic conditions, allergies
    };
  }

  // Update preferences based on user interactions
  updatePreferences(doctorId, rating, specialty) {
    this.preferences.ratings[doctorId] = rating;
    
    // If high rating, boost specialty preference
    if (rating >= 4) {
      if (!this.preferences.preferredSpecialties.includes(specialty)) {
        this.preferences.preferredSpecialties.push(specialty);
      }
    }
    
    this.preferences.pastConsultations.push({
      doctorId,
      specialty,
      rating,
      timestamp: new Date()
    });
  }

  // Calculate similarity score between user and doctor
  calculateDoctorSimilarity(doctor) {
    let score = 0;
    
    // Specialty preference (40% weight)
    if (this.preferences.preferredSpecialties.includes(doctor.specialty)) {
      score += 0.4;
    }
    
    // Gender preference (20% weight)
    if (this.preferences.doctorAttributes.gender === doctor.gender) {
      score += 0.2;
    }
    
    // Location preference (30% weight)
    if (this.preferences.doctorAttributes.location === doctor.location) {
      score += 0.3;
    }
    
    // Past positive experiences (10% weight)
    const pastRating = this.preferences.ratings[doctor.id];
    if (pastRating && pastRating >= 4) {
      score += 0.1;
    }
    
    return score;
  }
}