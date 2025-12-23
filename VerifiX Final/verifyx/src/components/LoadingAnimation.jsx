import { useEffect, useState } from 'react'
import './LoadingAnimation.css'

/**
 * Loading Animation Component
 * 
 * Professional loading animation with AI bot walking on progress bar
 * Displays before login page
 */
const LoadingAnimation = ({ onComplete }) => {
  const [progress, setProgress] = useState(0)
  const [currentSegment, setCurrentSegment] = useState(0)
  const [isPaused, setIsPaused] = useState(false)
  const [isLookingAhead, setIsLookingAhead] = useState(false)
  const totalSegments = 8

  useEffect(() => {
    // Ensure animation starts from 0
    setProgress(0)
    setCurrentSegment(0)
    
    // Fixed 3 seconds duration
    const duration = 3000 // Exactly 3 seconds
    const interval = 30 // Update every 30ms for smoother animation
    const totalSteps = duration / interval
    const baseIncrement = 100 / totalSteps
    
    // Select one of 10 different patterns randomly
    const patternType = Math.floor(Math.random() * 10)
    
    let speedVariations = []
    let pausePoints = []
    let pauseDurations = []
    
    // Pattern 1: Slow start, fast middle, slow end
    if (patternType === 0) {
      speedVariations = [0.4, 0.6, 1.0, 1.5, 1.8, 1.5, 1.0, 0.6]
      pausePoints = [3, 6]
      pauseDurations = [400, 500]
    }
    // Pattern 2: Fast start, slow middle, fast end
    else if (patternType === 1) {
      speedVariations = [1.8, 1.5, 0.5, 0.4, 0.6, 1.2, 1.6, 1.8]
      pausePoints = [2, 5]
      pauseDurations = [350, 450]
    }
    // Pattern 3: Steady with one long pause
    else if (patternType === 2) {
      speedVariations = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
      pausePoints = [4]
      pauseDurations = [600]
    }
    // Pattern 4: Variable speed throughout
    else if (patternType === 3) {
      speedVariations = [0.7, 1.3, 0.8, 1.5, 0.9, 1.2, 0.6, 1.4]
      pausePoints = [2, 5, 7]
      pauseDurations = [300, 400, 350]
    }
    // Pattern 5: Accelerating throughout
    else if (patternType === 4) {
      speedVariations = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7]
      pausePoints = [3]
      pauseDurations = [450]
    }
    // Pattern 6: Decelerating throughout
    else if (patternType === 5) {
      speedVariations = [1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3]
      pausePoints = [5]
      pauseDurations = [500]
    }
    // Pattern 7: Fast-slow-fast-slow rhythm
    else if (patternType === 6) {
      speedVariations = [1.5, 0.6, 1.4, 0.7, 1.3, 0.8, 1.2, 0.9]
      pausePoints = [1, 4, 7]
      pauseDurations = [250, 350, 300]
    }
    // Pattern 8: Slow-fast-slow-fast rhythm
    else if (patternType === 7) {
      speedVariations = [0.5, 1.6, 0.6, 1.5, 0.7, 1.4, 0.8, 1.3]
      pausePoints = [2, 6]
      pauseDurations = [400, 450]
    }
    // Pattern 9: Two speed bursts
    else if (patternType === 8) {
      speedVariations = [0.8, 1.8, 1.8, 0.7, 0.6, 1.7, 1.7, 0.9]
      pausePoints = [1, 4]
      pauseDurations = [300, 400]
    }
    // Pattern 10: Smooth wave pattern
    else {
      speedVariations = [0.7, 1.0, 1.3, 1.5, 1.3, 1.0, 0.7, 0.5]
      pausePoints = [3, 6]
      pauseDurations = [350, 400]
    }
    
    let currentSpeedIndex = 0
    let pauseTimer = null
    let paused = false
    let stepCount = 0
    let pauseIndex = 0

    const timer = setInterval(() => {
      if (paused) return

      stepCount++
      
      // Calculate current segment to determine speed
      const currentSegmentIndex = Math.floor((stepCount / totalSteps) * totalSegments)
      if (currentSegmentIndex < speedVariations.length) {
        currentSpeedIndex = currentSegmentIndex
      }
      
      const increment = baseIncrement * speedVariations[currentSpeedIndex]
      
      setProgress((prev) => {
        const newProgress = Math.min(prev + increment, 100)
        
        // Calculate which segment the bot is on
        const segment = Math.floor((newProgress / 100) * totalSegments)
        setCurrentSegment(segment)

        // Check if we should pause at this segment
        if (pausePoints.includes(segment) && !paused && stepCount > 5 && pauseIndex < pausePoints.length) {
          paused = true
          setIsPaused(true)
          setIsLookingAhead(true)
          
          const pauseDuration = pauseDurations[pauseIndex] || 400
          pauseIndex++
          
          pauseTimer = setTimeout(() => {
            paused = false
            setIsPaused(false)
            setIsLookingAhead(false)
          }, pauseDuration)
        }

        if (newProgress >= 100) {
          clearInterval(timer)
          if (pauseTimer) clearTimeout(pauseTimer)
          // Wait a moment before calling onComplete
          setTimeout(() => {
            if (onComplete) onComplete()
          }, 200)
          return 100
        }
        return newProgress
      })
    }, interval)

    return () => {
      clearInterval(timer)
      if (pauseTimer) clearTimeout(pauseTimer)
    }
  }, [onComplete, totalSegments])

  // Calculate bot position (0 to 100%)
  const botPosition = (progress / 100) * 100

  return (
    <div className="loading-animation-container">
      <div className="loading-animation">
        {/* Loading Text */}
        <div className="loading-text">
          LOADING<span className="loading-dots">
            <span className="dot">.</span>
            <span className="dot">.</span>
            <span className="dot">.</span>
          </span>
        </div>

        {/* Loading Bar */}
        <div className="loading-bar-container">
          <div className="loading-bar-outline">
            {Array.from({ length: totalSegments }).map((_, index) => (
              <div
                key={index}
                className={`loading-segment ${
                  index < currentSegment ? 'filled' : ''
                } ${index === currentSegment && progress % (100 / totalSegments) > 0 ? 'filling' : ''}`}
                style={{
                  width: `${100 / totalSegments}%`
                }}
              />
            ))}
          </div>
        </div>

        {/* AI Bot Character - Cartoon Style */}
        <div
          className={`ai-bot ${isPaused ? 'paused' : ''} ${isLookingAhead ? 'looking-ahead' : ''}`}
          style={{
            left: `${botPosition}%`,
            transform: 'translateX(-50%)'
          }}
        >
          {/* Head */}
          <div className="bot-head">
            <div className="bot-face">
              {/* Forehead Lines */}
              <div className="bot-forehead-lines"></div>
              
              {/* Blue Eyes */}
              <div className="bot-eye left-eye"></div>
              <div className="bot-eye right-eye"></div>
              
              {/* Smile */}
              <div className="bot-mouth"></div>
            </div>
            
            {/* Antennae */}
            <div className="bot-antenna left"></div>
            <div className="bot-antenna right"></div>
          </div>

          {/* Body */}
          <div className="bot-body">
            {/* Right Arm with Magnifying Glass */}
            <div className="bot-arm right">
              <div className="bot-hand">
                {/* Magnifying Glass */}
                <div className="magnifying-glass">
                  <div className="magnifying-lens"></div>
                  <div className="magnifying-handle"></div>
                </div>
              </div>
              <div className="bot-wave-lines"></div>
            </div>
          </div>

          {/* Shadow */}
          <div className="bot-shadow"></div>
        </div>
      </div>
    </div>
  )
}

export default LoadingAnimation

