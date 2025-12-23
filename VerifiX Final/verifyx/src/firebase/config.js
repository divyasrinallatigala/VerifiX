import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

/**
 * Firebase Configuration
 * 
 * Firebase project credentials for VerifiX
 */

const firebaseConfig = {
  apiKey: "AIzaSyBO2RJ94eU189bnO_6YFAA1hq-sAcMZMjc",
  authDomain: "verifyx-84715.firebaseapp.com",
  projectId: "verifyx-84715",
  storageBucket: "verifyx-84715.firebasestorage.app",
  messagingSenderId: "130315840382",
  appId: "1:130315840382:web:33727e3247d308af22612f",
  measurementId: "G-TW5WQ8RD9M"
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

