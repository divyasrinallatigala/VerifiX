# How to Start the Development Server

## Quick Start

1. Open a terminal in the project directory
2. Run: `npm run dev`
3. Open your browser to the URL shown (usually http://localhost:5173)

## If you see errors:

### "npm: command not found"
- Install Node.js from https://nodejs.org/

### Port already in use
- Vite will automatically try the next port (5174, 5175, etc.)
- Check the terminal output for the actual URL

### Pages not loading
- Make sure you're accessing the correct route:
  - Login: http://localhost:5173/login
  - Upload: http://localhost:5173/upload
  - Results: http://localhost:5173/results
- The root path (/) automatically redirects to /login

### Clear browser cache
- Press Ctrl+Shift+R (or Cmd+Shift+R on Mac) to hard refresh

## Troubleshooting

If pages are blank:
1. Open browser DevTools (F12)
2. Check the Console tab for errors
3. Check the Network tab to see if files are loading

