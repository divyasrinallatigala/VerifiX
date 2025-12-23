import { Link } from 'react-router-dom'

/**
 * Logo Component
 * 
 * VerifiX logo component for consistent branding
 * Clickable logo that navigates to upload page
 */

const Logo = ({ className = '', clickable = true }) => {
  const logoContent = (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="w-8 h-8 bg-primary-600 rounded flex items-center justify-center">
        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </div>
      <span className="text-xl font-bold text-gray-900">VerifiX</span>
    </div>
  )

  if (clickable) {
    return (
      <Link to="/upload" className="hover:opacity-80 transition-opacity">
        {logoContent}
      </Link>
    )
  }

  return logoContent
}

export default Logo

