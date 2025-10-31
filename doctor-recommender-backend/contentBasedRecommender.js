import { UserProfile } from './userProfile.js';

export class ContentBasedRecommender {
  constructor() {
    this.userProfiles = new Map(); // userId -> UserProfile
  }

  // Get or create user profile
  getUserProfile(userId) {
    if (!this.userProfiles.has(userId)) {
      this.userProfiles.set(userId, new UserProfile(userId));
    }
    return this.userProfiles.get(userId);
  }

  // Extract doctor features for similarity calculation
  extractDoctorFeatures(doctor) {
    return {
      specialty: doctor.specialty,
      gender: doctor.gender || 'Unknown',
      location: doctor.location,
      rating: doctor.rating || 0,
      experience: this.categorizeExperience(doctor.credential),
      hospital: doctor.hospital || 'Private Practice'
    };
  }

  categorizeExperience(credential) {
    if (!credential) return 'medium';
    if (credential.includes('FWACS') || credential.includes('FMCS')) return 'high';
    if (credential.includes('MBBS') && credential.includes('F')) return 'high';
    return 'medium';
  }

  // Content-based recommendation algorithm
  recommendDoctors(userId, availableDoctors, requiredSpecialty, limit = 5) {
    const userProfile = this.getUserProfile(userId);
    
    // Filter doctors by required specialty first
    const relevantDoctors = availableDoctors.filter(doctor => 
      doctor.specialty.toLowerCase().includes(requiredSpecialty.toLowerCase())
    );

    // Calculate content-based similarity scores
    const scoredDoctors = relevantDoctors.map(doctor => {
      const features = this.extractDoctorFeatures(doctor);
      const similarityScore = userProfile.calculateDoctorSimilarity(features);
      
      // Combine similarity with doctor rating
      const contentScore = (similarityScore * 0.7) + (features.rating / 5 * 0.3);
      
      return {
        ...doctor,
        contentScore,
        similarityScore,
        recommendationReason: this.generateRecommendationReason(userProfile, features)
      };
    });

    // Sort by content score and return top recommendations
    return scoredDoctors
      .sort((a, b) => b.contentScore - a.contentScore)
      .slice(0, limit);
  }

  // Generate explanation for why doctor was recommended
  generateRecommendationReason(userProfile, doctorFeatures) {
    const reasons = [];
    
    if (userProfile.preferences.preferredSpecialties.includes(doctorFeatures.specialty)) {
      reasons.push(`You've had positive experiences with ${doctorFeatures.specialty} specialists`);
    }
    
    if (userProfile.preferences.doctorAttributes.gender === doctorFeatures.gender) {
      reasons.push(`Matches your preferred doctor gender`);
    }
    
    if (userProfile.preferences.doctorAttributes.location === doctorFeatures.location) {
      reasons.push(`Located in your preferred area: ${doctorFeatures.location}`);
    }
    
    if (doctorFeatures.rating >= 4.5) {
      reasons.push(`Highly rated doctor (${doctorFeatures.rating}/5.0)`);
    }
    
    return reasons.length > 0 ? reasons.join(', ') : 'Recommended based on your profile';
  }

  // Update user profile based on interactions
  updateUserProfile(userId, doctorId, rating, specialty, doctorFeatures) {
    const userProfile = this.getUserProfile(userId);
    userProfile.updatePreferences(doctorId, rating, specialty);
    
    // Learn from user preferences
    if (rating >= 4) {
      if (doctorFeatures.gender) {
        userProfile.preferences.doctorAttributes.gender = doctorFeatures.gender;
      }
      if (doctorFeatures.location) {
        userProfile.preferences.doctorAttributes.location = doctorFeatures.location;
      }
    }
  }
}