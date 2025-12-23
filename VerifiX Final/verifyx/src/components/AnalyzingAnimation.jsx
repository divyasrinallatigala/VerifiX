import { useEffect } from 'react'
import './AnalyzingAnimation.css'

/**
 * Analyzing Animation Component
 * 
 * 3D animation showing documents being analyzed under a magnifying glass
 * Plays after clicking "Analyze Documents"
 * 
 * Note: Visibility is controlled by the parent component.
 * Calls onComplete after the minimum animation duration (10s).
 */
const AnalyzingAnimation = ({ onComplete }) => {
  useEffect(() => {
    // Animation plays for 10 seconds, then calls onComplete
    const timer = setTimeout(() => {
      if (onComplete) {
        onComplete()
      }
    }, 10000) // 10 seconds for a "deep analysis" feel

    return () => clearTimeout(timer)
  }, [onComplete])

  return (
    <div className="analyzing-animation-container">
      {/* Magnifying Glass */}
      <div className="magnifying-glass-3d">
        <div className="glass-lens">
          <div className="lens-reflection"></div>
          <div className="lens-highlight"></div>
        </div>
        <div className="glass-handle"></div>
      </div>

      {/* Flying Documents */}
      {Array.from({ length: 15 }).map((_, index) => (
        <div
          key={index}
          className="flying-document"
          style={{
            animationDelay: `${index * 0.25}s`,
            top: `${45 + (index % 5) * 2.5}%`
          }}
        >
          <div className="document-page">
            <div className="document-lines">
              <div className="line"></div>
              <div className="line"></div>
              <div className="line short"></div>
              <div className="line"></div>
              <div className="line"></div>
            </div>
            <div className="document-content">
              <div className="content-box"></div>
              <div className="content-box small"></div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default AnalyzingAnimation
