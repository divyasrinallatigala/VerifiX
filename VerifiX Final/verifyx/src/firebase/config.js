import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

/**
 * Firebase Configuration
 * 
 * Firebase project credentials for VerifiX
 */

const firebaseConfig = {
  apiKey: "Your API key",
  authDomain: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
  measurementId: ""
}

// Initialize Firebase
let app
let auth

try {
  app = initializeApp(firebaseConfig)
  auth = getAuth(app)

  // Verify Firebase is initialized correctly
  if (!auth) {
    console.error('Firebase Auth initialization failed')
  }
} catch (error) {
  console.error('Firebase initialization error:', error)
  throw error
}

// Initialize Firebase Authentication and get a reference to the service
export { auth }
export default app

