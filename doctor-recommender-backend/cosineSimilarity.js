// Cosine Similarity Implementation
export class CosineSimilarityRecommender {
  
  // Convert user preferences to vector
  userToVector(userProfile) {
    return [
      userProfile.preferences.preferredSpecialties.length / 10, // Normalized specialty count
      userProfile.preferences.doctorAttributes.gender === 'M' ? 1 : 0,
      userProfile.preferences.doctorAttributes.gender === 'F' ? 1 : 0,
      this.locationToNumber(userProfile.preferences.doctorAttributes.location),
      this.averageRating(userProfile.preferences.ratings)
    ];
  }
  
  // Convert doctor to vector
  doctorToVector(doctor) {
    return [
      this.specialtyToNumber(doctor.specialty),
      doctor.gender === 'M' ? 1 : 0,
      doctor.gender === 'F' ? 1 : 0,
      this.locationToNumber(doctor.location),
      doctor.rating / 5 // Normalize rating to 0-1
    ];
  }
  
  // Calculate cosine similarity
  cosineSimilarity(vectorA, vectorB) {
    const dotProduct = vectorA.reduce((sum, a, i) => sum + a * vectorB[i], 0);
    const magnitudeA = Math.sqrt(vectorA.reduce((sum, a) => sum + a * a, 0));
    const magnitudeB = Math.sqrt(vectorB.reduce((sum, b) => sum + b * b, 0));
    
    return magnitudeA && magnitudeB ? dotProduct / (magnitudeA * magnitudeB) : 0;
  }
  
  specialtyToNumber(specialty) {
    const specialtyMap = {
      'Internal Medicine': 0.1, 'Cardiology': 0.2, 'Ophthalmology': 0.3,
      'Dentist': 0.4, 'Pediatrics': 0.5, 'Surgery': 0.6
    };
    return specialtyMap[specialty] || 0;
  }
  
  locationToNumber(location) {
    const locationMap = {
      'Lagos': 0.1, 'Abuja': 0.2, 'Kano': 0.3, 'Port Harcourt': 0.4
    };
    return locationMap[location] || 0;
  }
  
  averageRating(ratings) {
    const values = Object.values(ratings);
    return values.length ? values.reduce((a, b) => a + b, 0) / values.length / 5 : 0;
  }
}