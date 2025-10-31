// Service to fetch available symptoms from backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8007';

export const fetchAvailableSymptoms = async () => {
  try {
    console.log('🔍 Fetching available symptoms from backend...');
    
    const response = await fetch(`${API_BASE_URL}/available-symptoms`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('✅ Received symptoms from backend:', data);
    
    return {
      success: true,
      symptoms: data.symptoms || [],
      totalCount: data.total_count || 0,
      message: data.message || 'Symptoms loaded successfully'
    };
    
  } catch (error) {
    console.error('❌ Error fetching symptoms from backend:', error);
    
    // Return fallback empty list
    return {
      success: false,
      symptoms: [],
      totalCount: 0,
      error: error.message,
      message: 'Failed to load symptoms from backend'
    };
  }
};

// Transform backend symptoms into frontend format
export const transformSymptomsForFrontend = (backendSymptoms) => {
  const categorizedSymptoms = {};
  
  backendSymptoms.forEach(symptom => {
    const category = symptom.category || 'Other';
    
    if (!categorizedSymptoms[category]) {
      categorizedSymptoms[category] = {
        icon: getCategoryIcon(category),
        color: getCategoryColor(category),
        symptoms: []
      };
    }
    
    categorizedSymptoms[category].symptoms.push(symptom.value);
  });
  
  return categorizedSymptoms;
};

// Get icon for category
const getCategoryIcon = (category) => {
  const icons = {
    'Respiratory': '🫁',
    'Gastrointestinal': '🍽️',
    'Neurological': '🧠',
    'Cardiovascular': '❤️',
    'Musculoskeletal': '🦴',
    'Dermatological': '🧴',
    'Ophthalmological': '👁️',
    'ENT': '👂',
    'Dental': '🦷',
    'General': '🌡️',
    'Other': '📋'
  };
  return icons[category] || '📋';
};

// Get color for category
const getCategoryColor = (category) => {
  const colors = {
    'Respiratory': '#3B82F6',
    'Gastrointestinal': '#10B981',
    'Neurological': '#8B5CF6',
    'Cardiovascular': '#EF4444',
    'Musculoskeletal': '#F59E0B',
    'Dermatological': '#EC4899',
    'Ophthalmological': '#06B6D4',
    'ENT': '#84CC16',
    'Dental': '#F97316',
    'General': '#6B7280',
    'Other': '#9CA3AF'
  };
  return colors[category] || '#9CA3AF';
};
