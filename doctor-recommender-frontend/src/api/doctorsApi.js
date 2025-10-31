// External Doctors API Integration
const DOCTORS_API_BASE = 'YOUR_DOCTORS_API_URL'; // Replace with your actual API URL

export const fetchDoctorsBySpecialty = async (specialty, location = null) => {
  try {
    console.log(`🔍 Fetching doctors for specialty: ${specialty}`);
    
    // Example API call - adjust based on your API structure
    const params = new URLSearchParams();
    params.append('specialty', specialty);
    if (location) {
      params.append('location', location);
    }
    
    const response = await fetch(`${DOCTORS_API_BASE}/doctors?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add any required API keys or auth headers here
        // 'Authorization': 'Bearer YOUR_API_KEY',
      },
    });
    
    if (!response.ok) {
      throw new Error(`Doctors API error: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`✅ Found ${data.length || 0} doctors for ${specialty}`);
    
    // Normalize the response to match our expected format
    return normalizeDoctorsData(data);
    
  } catch (error) {
    console.error('❌ Error fetching doctors:', error);
    // Return mock data as fallback
    return getMockDoctors(specialty);
  }
};

// Normalize different API response formats to our standard format
const normalizeDoctorsData = (apiData) => {
  // Adjust this based on your API's response structure
  if (Array.isArray(apiData)) {
    return apiData.map(doctor => ({
      id: doctor.id || doctor.doctor_id || Math.random().toString(36),
      name: doctor.name || doctor.doctor_name || doctor.full_name || 'Dr. Unknown',
      specialty: doctor.specialty || doctor.specialization || doctor.field,
      location: doctor.location || doctor.address || doctor.city || 'Location not specified',
      rating: doctor.rating || doctor.average_rating || 4.0,
      experience: doctor.experience || doctor.years_experience || 'Not specified',
      availability: doctor.availability || doctor.available_times || 'Contact for availability',
      phone: doctor.phone || doctor.contact_number || doctor.telephone,
      email: doctor.email || doctor.contact_email,
      hospital: doctor.hospital || doctor.clinic || doctor.practice_name,
      image: doctor.image || doctor.photo || doctor.profile_picture,
      bio: doctor.bio || doctor.description || doctor.about
    }));
  }
  
  // Handle single doctor object
  if (apiData && typeof apiData === 'object') {
    return [normalizeDoctorsData([apiData])[0]];
  }
  
  return [];
};

// Mock doctors data as fallback
const getMockDoctors = (specialty) => {
  const mockDoctors = {
    'Cardiology': [
      {
        id: 'card1',
        name: 'Dr. Sarah Johnson',
        specialty: 'Cardiology',
        location: 'Downtown Medical Center',
        rating: 4.8,
        experience: '15 years',
        availability: 'Mon-Fri 9AM-5PM',
        phone: '(555) 123-4567',
        hospital: 'Heart Care Institute'
      },
      {
        id: 'card2',
        name: 'Dr. Michael Chen',
        specialty: 'Cardiology',
        location: 'University Hospital',
        rating: 4.7,
        experience: '12 years',
        availability: 'Tue-Sat 8AM-4PM',
        phone: '(555) 234-5678',
        hospital: 'Cardiac Specialists Group'
      }
    ],
    'Neurology': [
      {
        id: 'neuro1',
        name: 'Dr. Emily Rodriguez',
        specialty: 'Neurology',
        location: 'Brain & Spine Center',
        rating: 4.9,
        experience: '18 years',
        availability: 'Mon-Thu 10AM-6PM',
        phone: '(555) 345-6789',
        hospital: 'Neurological Institute'
      }
    ],
    'Gastroenterology': [
      {
        id: 'gastro1',
        name: 'Dr. David Kim',
        specialty: 'Gastroenterology',
        location: 'Digestive Health Clinic',
        rating: 4.6,
        experience: '10 years',
        availability: 'Mon-Fri 8AM-3PM',
        phone: '(555) 456-7890',
        hospital: 'GI Specialists'
      }
    ],
    'Family Medicine': [
      {
        id: 'family1',
        name: 'Dr. Lisa Thompson',
        specialty: 'Family Medicine',
        location: 'Community Health Center',
        rating: 4.5,
        experience: '8 years',
        availability: 'Mon-Sat 7AM-7PM',
        phone: '(555) 567-8901',
        hospital: 'Primary Care Associates'
      }
    ],
    'Dermatology': [
      {
        id: 'derm1',
        name: 'Dr. James Wilson',
        specialty: 'Dermatology',
        location: 'Skin Care Center',
        rating: 4.7,
        experience: '14 years',
        availability: 'Tue-Fri 9AM-4PM',
        phone: '(555) 678-9012',
        hospital: 'Dermatology Associates'
      }
    ]
  };
  
  return mockDoctors[specialty] || [
    {
      id: 'general1',
      name: 'Dr. General Practitioner',
      specialty: specialty,
      location: 'Medical Center',
      rating: 4.0,
      experience: '5 years',
      availability: 'Contact for availability',
      phone: '(555) 000-0000',
      hospital: 'General Hospital'
    }
  ];
};

// Function to search doctors by multiple criteria
export const searchDoctors = async (criteria) => {
  const { specialties = [], location = null, rating = null, availability = null } = criteria;
  
  try {
    const allDoctors = [];
    
    // Fetch doctors for each specialty
    for (const specialty of specialties) {
      const doctors = await fetchDoctorsBySpecialty(specialty, location);
      allDoctors.push(...doctors);
    }
    
    // Apply additional filters
    let filteredDoctors = allDoctors;
    
    if (rating) {
      filteredDoctors = filteredDoctors.filter(doctor => doctor.rating >= rating);
    }
    
    if (availability) {
      filteredDoctors = filteredDoctors.filter(doctor => 
        doctor.availability.toLowerCase().includes(availability.toLowerCase())
      );
    }
    
    // Remove duplicates based on doctor ID
    const uniqueDoctors = filteredDoctors.filter((doctor, index, self) =>
      index === self.findIndex(d => d.id === doctor.id)
    );
    
    // Sort by rating (highest first)
    uniqueDoctors.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    
    return uniqueDoctors;
    
  } catch (error) {
    console.error('❌ Error searching doctors:', error);
    return [];
  }
};

// Configuration for your specific doctors API
export const configureDoctorsAPI = (config) => {
  if (config.baseUrl) {
    DOCTORS_API_BASE = config.baseUrl;
  }
  // Add other configuration options as needed
};

export default {
  fetchDoctorsBySpecialty,
  searchDoctors,
  configureDoctorsAPI
};
