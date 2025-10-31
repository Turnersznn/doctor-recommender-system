import fs from 'fs';
import path from 'path';

const RATINGS_FILE = path.join(process.cwd(), 'data', 'ratings.json');
const FAVORITES_FILE = path.join(process.cwd(), 'data', 'favorites.json');

function clearTestData() {
  try {
    console.log('Clearing test data...');
    
    // Clear ratings
    if (fs.existsSync(RATINGS_FILE)) {
      const ratingsData = JSON.parse(fs.readFileSync(RATINGS_FILE, 'utf-8'));
      
      // Remove test doctor ratings
      const testDoctorIds = Object.keys(ratingsData.ratings).filter(id => 
        id.startsWith('test-doctor')
      );
      
      testDoctorIds.forEach(id => {
        delete ratingsData.ratings[id];
        delete ratingsData.reviews[id];
        delete ratingsData.statistics[id];
      });
      
      fs.writeFileSync(RATINGS_FILE, JSON.stringify(ratingsData, null, 2));
      console.log('✅ Test ratings cleared');
    }
    
    // Clear favorites
    if (fs.existsSync(FAVORITES_FILE)) {
      const favoritesData = JSON.parse(fs.readFileSync(FAVORITES_FILE, 'utf-8'));
      // Remove test favorites
      if (favoritesData.favorites.DemoUser) {
        favoritesData.favorites.DemoUser = favoritesData.favorites.DemoUser.filter(fav => 
          !fav.doctorId.startsWith('test-doctor')
        );
      }
      fs.writeFileSync(FAVORITES_FILE, JSON.stringify(favoritesData, null, 2));
      console.log('✅ Test favorites cleared');
    }
    
    console.log('✅ All test data cleared successfully!');
    
  } catch (error) {
    console.error('❌ Error clearing test data:', error);
  }
}

clearTestData(); 