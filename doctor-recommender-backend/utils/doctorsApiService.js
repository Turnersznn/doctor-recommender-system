// DoctorsAPI Service for Backend
import axios from 'axios';

const DOCTORS_API_CONFIG = {
  baseUrl: 'https://doctorsapi.com/api',
  apiKey: process.env.DOCTORS_API_KEY || 'hk_mdx8spuncb661490ec7475302aea4f8a51dc9d7f2c1d29cb92ec23d0163f69c80bf7f972',
  endpoints: {
    doctors: '/doctors'
  },
  useMockData: false // Use real DoctorsAPI
};

// Function to search doctors by specialty using DoctorsAPI
export const searchDoctorsBySpecialty = async (specialty, location = null, limit = 10) => {
  try {
    console.log(`🔍 Backend: Searching for ${specialty} doctors`);

    // Use mock data if API is unavailable or configured to use mock data
    if (DOCTORS_API_CONFIG.useMockData || !DOCTORS_API_CONFIG.apiKey ||
        DOCTORS_API_CONFIG.apiKey === 'demo_key') {
      console.log(`🎭 Backend: Using mock data for ${specialty}`);
      return generateMockDoctors(specialty, limit);
    }

    console.log(`🔑 Backend: Using API key: ${DOCTORS_API_CONFIG.apiKey ? 'Present' : 'Missing'}`);

    // Build query parameters for DoctorsAPI
    const params = {
      specialty: specialty,
      limit: Math.min(limit, 25), // DoctorsAPI max is 25
      page: 1
    };
    
    // Add location filtering if provided (BetterDoctor format)
    if (location) {
      const locationParts = location.split(',').map(part => part.trim());
      if (locationParts.length >= 2) {
        params.location = `${locationParts[1]}-${locationParts[0]}`; // BetterDoctor uses state-city format
      } else {
        params.location = location;
      }
    }
    
    const url = `${DOCTORS_API_CONFIG.baseUrl}${DOCTORS_API_CONFIG.endpoints.doctors}`;
    console.log(`📡 Backend: DoctorsAPI URL: ${url}`);
    console.log(`📡 Backend: DoctorsAPI Params:`, params);
    console.log(`📡 Backend: DoctorsAPI Headers:`, {
      'Content-Type': 'application/json',
      'api-key': DOCTORS_API_CONFIG.apiKey ? `${DOCTORS_API_CONFIG.apiKey.substring(0, 10)}...` : 'Missing'
    });

    // Make the API request
    const response = await axios.get(url, {
      params,
      headers: {
        'Content-Type': 'application/json',
        'api-key': DOCTORS_API_CONFIG.apiKey,
      },
      timeout: 10000 // 10 second timeout
    });

    console.log(`✅ Backend: DoctorsAPI Response Status: ${response.status}`);
    console.log(`✅ Backend: DoctorsAPI Response Data:`, response.data);
    console.log(`✅ Backend: DoctorsAPI returned ${response.data.doctors?.length || 0} doctors`);
    
    // Normalize the DoctorsAPI response
    return normalizeDoctorsApiResponse(response.data);
    
  } catch (error) {
    console.error('❌ Backend: DoctorsAPI error:', error.message);
    console.error('❌ Backend: DoctorsAPI error details:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url,
      params: error.config?.params
    });

    // Return empty array on error - controller will use fallback
    return [];
  }
};

// Function to search doctors for multiple specialties
export const searchDoctorsForDiagnoses = async (diagnoses, location = null) => {
  try {
    const allDoctors = [];
    const specialties = [...new Set(diagnoses.map(d => d.specialist))];
    
    console.log(`🔍 Backend: Searching for doctors in specialties: ${specialties.join(', ')}`);
    
    // Search for doctors in each specialty
    for (const specialty of specialties) {
      const doctors = await searchDoctorsBySpecialty(specialty, location, 5);
      allDoctors.push(...doctors);
    }
    
    // Remove duplicates and sort by rating
    const uniqueDoctors = allDoctors.filter((doctor, index, self) =>
      index === self.findIndex(d => d.id === doctor.id)
    );
    
    uniqueDoctors.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    
    return uniqueDoctors.slice(0, 15); // Return top 15 doctors
    
  } catch (error) {
    console.error('❌ Backend: Error searching doctors for diagnoses:', error);
    return [];
  }
};

// Normalize DoctorsAPI response to our format
const normalizeDoctorsApiResponse = (apiResponse) => {
  const doctors = apiResponse.doctors || [];

  return doctors.map(doctor => ({
    id: doctor.id || doctor.npi?.toString(),
    name: doctor.name || 'Dr. Unknown',
    specialty: Array.isArray(doctor.specialties) ? doctor.specialties[0] : (doctor.specialties || 'General Practice'),
    specialties: doctor.specialties || [],
    location: formatDoctorsApiLocation(doctor),
    rating: doctor.rating || (Math.random() * 1.5 + 3.5).toFixed(1),
    experience: doctor.experience || 'Not specified',
    phone: doctor.phone || 'Contact for phone',
    fax: doctor.fax,
    email: doctor.email || 'Contact for email',
    hospital: doctor.hospital || doctor.organization || 'Private Practice',
    address: formatDoctorsApiAddress(doctor),
    availability: doctor.availability || 'Contact for availability',
    credentials: doctor.credentials || '',
    npi: doctor.npi,
    gender: doctor.gender,
    organizationIds: doctor.organizationIds || []
  }));
};

// Helper functions for DoctorsAPI
const formatDoctorsApiLocation = (doctor) => {
  if (doctor.address) {
    const addr = doctor.address;
    if (addr.city && addr.state) {
      return `${addr.city}, ${addr.state}`;
    }
    if (addr.firstLine) {
      return addr.firstLine;
    }
  }
  return 'Location not specified';
};

const formatDoctorsApiAddress = (doctor) => {
  if (!doctor.address) return 'Address not available';

  const addr = doctor.address;
  const parts = [];

  if (addr.firstLine) parts.push(addr.firstLine);
  if (addr.secondLine) parts.push(addr.secondLine);
  if (addr.city) parts.push(addr.city);
  if (addr.state) parts.push(addr.state);
  if (addr.postalCode) parts.push(addr.postalCode);

  return parts.join(', ') || 'Address not available';
};

// Configuration function
export const configureDoctorsAPI = (config) => {
  if (config.baseUrl) DOCTORS_API_CONFIG.baseUrl = config.baseUrl;
  if (config.apiKey) DOCTORS_API_CONFIG.apiKey = config.apiKey;
};

// Generate realistic mock doctors for testing
const generateMockDoctors = (specialty, limit = 5) => {
  const firstNames = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Ashley', 'James', 'Lisa'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
  const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'];
  const states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA'];

  const doctors = [];

  for (let i = 0; i < limit; i++) {
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    const city = cities[Math.floor(Math.random() * cities.length)];
    const state = states[Math.floor(Math.random() * states.length)];

    doctors.push({
      id: `mock_${specialty.toLowerCase()}_${i + 1}`,
      name: `Dr. ${firstName} ${lastName}`,
      specialty: specialty,
      specialties: [specialty],
      location: `${city}, ${state}`,
      rating: (Math.random() * 1.5 + 3.5).toFixed(1),
      experience: `${Math.floor(Math.random() * 20) + 5} years`,
      phone: `(${Math.floor(Math.random() * 900) + 100}) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`,
      email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}@${specialty.toLowerCase()}clinic.com`,
      hospital: `${city} ${specialty} Center`,
      address: `${Math.floor(Math.random() * 9999) + 1} Medical Dr, ${city}, ${state} ${Math.floor(Math.random() * 90000) + 10000}`,
      availability: 'Available for appointments',
      credentials: 'MD, Board Certified',
      npi: Math.floor(Math.random() * 9000000000) + 1000000000,
      gender: Math.random() > 0.5 ? 'M' : 'F'
    });
  }

  console.log(`✅ Backend: Generated ${doctors.length} mock ${specialty} doctors`);
  return doctors;
};

export default {
  searchDoctorsBySpecialty,
  searchDoctorsForDiagnoses,
  configureDoctorsAPI
};
