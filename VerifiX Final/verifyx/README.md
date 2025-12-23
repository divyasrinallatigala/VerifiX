# VerifiX - Financial Document Auditing Frontend

A clean, desktop-first React application for auditing financial documents with future AI agent integration support.

## Tech Stack

- **React 18** with Vite
- **Tailwind CSS** for styling
- **React Router** for navigation
- Frontend-only (no backend logic)
- Mock data (no Firebase/API integration)

## Project Structure

```
verifyx/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Logo.jsx
│   │   ├── StatusBadge.jsx
│   │   └── RiskLevelBadge.jsx
│   ├── pages/              # Page components
│   │   ├── Login.jsx
│   │   ├── Upload.jsx
│   │   └── Results.jsx
│   ├── data/               # Mock data
│   │   └── mockAgentResponse.js
│   ├── App.jsx             # Router setup
│   ├── main.jsx            # Entry point
│   └── index.css           # Tailwind imports
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Features

### 1. Login Page (`/login`)
- Email and password form
- Social login UI (Google, Email OTP) - UI only
- Navigates to `/upload` on submit

### 2. Upload Page (`/upload`)
- Drag-and-drop file upload interface
- File preview after selection
- Status box showing "Waiting for agent analysis..."
- "Analyze Documents" button navigates to `/results`
- Supported formats: PDF, JPG, PNG, CSV

### 3. Results Page (`/results`) - **Most Important**
- **Desktop-first split layout (70/30)**
- **Left Panel (70%):**
  - Searchable receipt table
  - Columns: Receipt ID, Vendor, Amount, Date, Status
  - Click row to select receipt
  - Pagination controls
- **Right Panel (30%, fixed):**
  - "Agent Risk Analysis" section
  - Displays selected receipt's agent analysis:
    - Risk Level badge
    - Reasons (bullet list)
    - Confidence Score (progress bar)
    - Notes from Agent
    - Evidence Preview (image slot - auto-fits if URL exists)

## Agent Integration Points

The application is designed for easy AI agent integration. Key integration points are marked with `TODO` comments:

1. **`src/data/mockAgentResponse.js`**: Replace mock data with API calls
2. **`src/pages/Results.jsx`**: Replace `getAllReceipts()` with API call
3. **`src/pages/Upload.jsx`**: Add file upload API integration
4. **`src/pages/Login.jsx`**: Add authentication API integration

### Agent Response Structure

The agent should return JSON matching this structure:

```javascript
{
  receipts: [
    {
      id: 'INV-2023-1825',
      vendor: 'ABC Supplies',
      amount: 16000,
      date: '2023-10-15',
      status: 'risky', // 'safe' | 'risky' | 'fake'
      agentAnalysis: {
        riskLevel: 'high', // 'low' | 'medium' | 'high' | 'critical'
        reasons: ['Reason 1', 'Reason 2'],
        confidenceScore: 0.92, // 0-1
        notes: 'Agent-generated analysis text',
        evidenceImageUrl: 'https://...' // or null
      }
    }
  ]
}
```

## Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Design Principles

- **Desktop-first**: Optimized for desktop viewing
- **Light theme**: Clean, minimal color palette
- **Enterprise look**: Professional, business-appropriate styling
- **No unnecessary animations**: Focus on functionality
- **Fixed sections**: Agent content areas are clearly marked and ready for API injection

## Future API Integration

When integrating with the agent API:

1. Replace mock data imports with API calls
2. Add loading states
3. Add error handling
4. Update the evidence image URL when agent provides it
5. Real-time updates if using WebSockets

All integration points are clearly marked with `TODO` comments in the code.

