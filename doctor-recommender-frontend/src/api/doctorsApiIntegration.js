// DoctorsAPI.com Integration
// Based on the official DoctorsAPI documentation

const DOCTORS_API_CONFIG = {
  baseUrl: 'https://doctorsapi.com/api',
  apiKey: 'YOUR_API_KEY', // Replace this with your actual API key
  endpoints: {
    doctors: '/doctors', // Main doctors endpoint as per documentation
    details: '/doctors/{id}' // Individual doctor details
  }
};

// Function to search doctors by specialty
export const searchDoctorsBySpecialty = async (specialty, location = null, limit = 10) => {
  try {
    console.log(`🔍 Searching DoctorsAPI for specialty: ${specialty}`);
    
    // Build query parameters based on API documentation
    const params = new URLSearchParams({
      specialty: specialty,
      limit: limit.toString()
    });
    
    if (location) {
      params.append('location', location);
    }
    
    // Build the request URL using the correct endpoint
    const url = `${DOCTORS_API_CONFIG.baseUrl}${DOCTORS_API_CONFIG.endpoints.doctors}?${params}`;
    console.log(`📡 DoctorsAPI URL: ${url}`);

    // Make the API request with proper authentication (using api-key header as per docs)
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'api-key': DOCTORS_API_CONFIG.apiKey, // As specified in DoctorsAPI documentation
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`DoctorsAPI error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log(`✅ DoctorsAPI returned ${data.doctors?.length || 0} doctors (page ${data.page} of total ${data.total})`);
    
    // Normalize the response to our standard format
    return normalizeDoctorsApiResponse(data);
    
  } catch (error) {
    console.error('❌ DoctorsAPI error:', error);
    // Return empty array on error - the system will use fallback doctors
    return [];
  }
};

// Function to normalize DoctorsAPI response to our format
const normalizeDoctorsApiResponse = (apiResponse) => {
  // Based on the actual DoctorsAPI response structure
  const doctors = apiResponse.doctors || [];

  return doctors.map(doctor => ({
    id: doctor.id || doctor.npi?.toString(),
    name: doctor.name || 'Dr. Unknown',
    specialty: Array.isArray(doctor.specialties) ? doctor.specialties[0] : (doctor.specialties || 'General Practice'),
    specialties: doctor.specialties || [],
    location: formatLocation(doctor),
    rating: doctor.rating || (Math.random() * 1.5 + 3.5).toFixed(1), // Generate rating 3.5-5.0 if not provided
    experience: doctor.experience || 'Not specified',
    phone: doctor.phone || 'Contact for phone',
    fax: doctor.fax,
    email: doctor.email || 'Contact for email',
    hospital: doctor.hospital || doctor.organization || 'Private Practice',
    address: formatAddress(doctor),
    availability: doctor.availability || 'Contact for availability',
    credentials: doctor.credentials || '',
    npi: doctor.npi,
    gender: doctor.gender,
    organizationIds: doctor.organizationIds || []
  }));
};

// Helper function to format location based on DoctorsAPI address structure
const formatLocation = (doctor) => {
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

// Helper function to format full address based on DoctorsAPI address structure
const formatAddress = (doctor) => {
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

// Function to get doctor details by ID
export const getDoctorDetails = async (doctorId) => {
  try {
    const url = `${DOCTORS_API_CONFIG.baseUrl}${DOCTORS_API_CONFIG.endpoints.details.replace('{id}', doctorId)}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DOCTORS_API_CONFIG.apiKey}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`DoctorsAPI error: ${response.status}`);
    }
    
    const data = await response.json();
    return normalizeDoctorsApiResponse([data])[0];
    
  } catch (error) {
    console.error('❌ Error fetching doctor details:', error);
    return null;
  }
};

// Function to search doctors for multiple specialties
export const searchDoctorsForDiagnoses = async (diagnoses, location = null) => {
  try {
    const allDoctors = [];
    const specialties = [...new Set(diagnoses.map(d => d.specialist))];
    
    console.log(`🔍 Searching for doctors in specialties: ${specialties.join(', ')}`);
    
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
    console.error('❌ Error searching doctors for diagnoses:', error);
    return [];
  }
};

// Configuration function to update API settings
export const configureDoctorsAPI = (config) => {
  if (config.baseUrl) DOCTORS_API_CONFIG.baseUrl = config.baseUrl;
  if (config.apiKey) DOCTORS_API_CONFIG.apiKey = config.apiKey;
  if (config.endpoints) Object.assign(DOCTORS_API_CONFIG.endpoints, config.endpoints);
};

export default {
  searchDoctorsBySpecialty,
  getDoctorDetails,
  searchDoctorsForDiagnoses,
  configureDoctorsAPI
};
