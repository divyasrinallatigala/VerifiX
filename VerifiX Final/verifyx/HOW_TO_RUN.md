# How to Run VerifiX Application

## Option 1: Development Server (Recommended)

This is the best option for development with hot-reload:

```bash
npm run dev
```

- Opens automatically at: `http://localhost:5173`
- Hot module replacement (changes appear instantly)
- Best for development

## Option 2: Preview Production Build

Build the app and preview the production version:

```bash
# Step 1: Build the app
npm run build

# Step 2: Preview the built app
npm run preview
```

- Opens automatically at: `http://localhost:3000`
- Shows production-optimized version
- Good for testing before deployment

## Option 3: Using VS Code Live Server

**Note:** VS Code Live Server won't work directly with React/Vite because:
- React needs to be compiled (JSX → JavaScript)
- ES modules need proper server handling
- Vite handles this automatically

**Instead, use one of the options above.**

## Option 4: Serve Built Files with Any HTTP Server

After building, you can serve the `dist` folder with any HTTP server:

```bash
# Build first
npm run build

# Then serve the dist folder with:
# - Python: python -m http.server 8000 (in dist folder)
# - Node: npx serve dist
# - PHP: php -S localhost:8000 (in dist folder)
```

## Quick Start

1. **Install dependencies** (if not done):
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Open browser** to the URL shown (usually `http://localhost:5173`)

## Troubleshooting

### Port already in use?
- Vite will automatically try the next port (5174, 5175, etc.)
- Check the terminal output for the actual URL

### Pages not loading?
- Make sure you're using the correct route:
  - `/login` - Login page
  - `/upload` - Upload page  
  - `/results` - Results page
- The root `/` automatically redirects to `/login`

### Need to access from another device?
- The server is configured to listen on all network interfaces
- Use your computer's IP address: `http://YOUR_IP:5173`

