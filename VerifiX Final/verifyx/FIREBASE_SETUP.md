# Firebase Authentication Setup Guide

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard

## Step 2: Enable Email/Password Authentication

1. In Firebase Console, go to **Authentication** > **Sign-in method**
2. Click on **Email/Password**
3. Enable the first toggle (Email/Password)
4. Click **Save**

## Step 3: Get Your Firebase Configuration

1. In Firebase Console, click the gear icon ⚙️ next to "Project Overview"
2. Select **Project settings**
3. Scroll down to **Your apps** section
4. If you don't have a web app, click **</>** (Web icon) to add one
5. Copy the configuration values:
   - `apiKey`
   - `authDomain`
   - `projectId`
   - `storageBucket`
   - `messagingSenderId`
   - `appId`

## Step 4: Configure Your App

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and paste your Firebase credentials:
   ```
   VITE_FIREBASE_API_KEY=your-actual-api-key
   VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your-project-id
   VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   VITE_FIREBASE_APP_ID=your-app-id
   ```

3. **Important:** Never commit `.env` to git (it's already in `.gitignore`)

## Step 5: Install Dependencies

```bash
npm install
```

## Step 6: Create a Test User (Optional)

1. In Firebase Console, go to **Authentication** > **Users**
2. Click **Add user**
3. Enter email and password
4. Click **Add user**

## Step 7: Test the Login

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Go to the login page
3. Try logging in with the test user credentials

## Troubleshooting

### "Firebase: Error (auth/invalid-api-key)"
- Check that your API key in `.env` is correct
- Make sure `.env` file is in the root directory
- Restart the dev server after changing `.env`

### "Firebase: Error (auth/unauthorized-domain)"
- Go to Firebase Console > Authentication > Settings
- Add your domain to **Authorized domains**

### Environment variables not loading?
- Make sure variable names start with `VITE_`
- Restart the dev server after changing `.env`
- Check that `.env` is in the project root

## Security Notes

- Never commit `.env` file to version control
- API keys in `.env` are exposed to the client (this is normal for Firebase)
- For production, use Firebase App Check for additional security
- Consider setting up Firebase Security Rules for your database

