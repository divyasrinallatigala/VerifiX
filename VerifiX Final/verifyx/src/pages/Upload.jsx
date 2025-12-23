import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { signOut, onAuthStateChanged } from 'firebase/auth'
import { auth } from '../firebase/config'
import { FiUploadCloud, FiFileText, FiCheck, FiAlertCircle, FiLogOut } from 'react-icons/fi'
import Logo from '../components/Logo'
import AnalyzingAnimation from '../components/AnalyzingAnimation'

/**
 * Upload Page
 * 
 * Handles uploading of Invoice (Required) and Reference PO (Optional).
 * Theme: Clean White/Light Gray (Smooth UI)
 */
const Upload = () => {
  const navigate = useNavigate()
  const [uploadedFile, setUploadedFile] = useState(null)
  const [poFile, setPoFile] = useState(null)
  const [isDraggingInvoice, setIsDraggingInvoice] = useState(false)
  const [isDraggingPO, setIsDraggingPO] = useState(false)
  const [loading, setLoading] = useState(false)
  const [showAnimation, setShowAnimation] = useState(false)
  const [auditData, setAuditData] = useState(null)
  const [error, setError] = useState(null)
  const [isAnimationComplete, setIsAnimationComplete] = useState(false)
  const [user, setUser] = useState(null)

  // Auth protection
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (!user) {
        navigate('/login')
      } else {
        setUser(user)
      }
    })
    return () => unsubscribe()
  }, [navigate])

  const handleInvoiceChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setUploadedFile(file)
      setError(null)
    }
  }

  const handlePoFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setPoFile(file)
    }
  }

  // Navigate when BOTH analysis is done AND animation is complete
  useEffect(() => {
    if (auditData && isAnimationComplete) {
      // Small delay before navigation to ensure the overlay stays for the full transition
      const timer = setTimeout(() => {
        navigate('/results', { state: { auditResult: auditData } })
      }, 500)
      return () => clearTimeout(timer)
    }
  }, [auditData, isAnimationComplete, navigate])

  const handleAnalyze = async () => {
    if (!uploadedFile) {
      setError('Please select an invoice to upload.')
      return
    }

    setLoading(true)
    setShowAnimation(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', uploadedFile)
    if (poFile) {
      formData.append('po_file', poFile)
    }

    try {
      const response = await fetch('/api/audit/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `Error: ${response.statusText}`)
      }

      const data = await response.json()
      setAuditData(data)
    } catch (err) {
      console.error('Audit failed:', err)
      setError(err.message || 'Failed to analyze document. Please try again.')
      setShowAnimation(false) // Hide animation on error so user can try again
    } finally {
      setLoading(false)
    }
  }

  const handleLoadingComplete = () => {
    setIsAnimationComplete(true)
  }

  return (
    <>
      {showAnimation && <AnalyzingAnimation onComplete={handleLoadingComplete} />}
      <div className="min-h-screen bg-gray-50 pt-20 pb-12 px-4 sm:px-6 lg:px-8 font-sans">
        <div className="max-w-5xl mx-auto">

          {/* Header */}
          <header className="bg-white border-b border-gray-200 fixed top-0 left-0 right-0 z-10 shadow-sm">
            <div className="max-w-7xl mx-auto px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Logo />
                  <span className="h-6 w-px bg-gray-300"></span>
                  <span className="text-gray-500 text-sm font-medium">Document Audit</span>
                </div>

                <nav className="flex items-center gap-6">
                  <button
                    onClick={async () => {
                      try {
                        await signOut(auth)
                        navigate('/login')
                      } catch (err) {
                        console.error('Logout failed:', err)
                      }
                    }}
                    className="text-gray-500 hover:text-red-600 font-medium transition-colors flex items-center gap-2"
                  >
                    <FiLogOut className="w-4 h-4" /> Sign Out
                  </button>
                </nav>
              </div>
            </div>
          </header>

          {/* Page Title Section */}
          <div className="text-center mb-16 space-y-4 pt-8">
            <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
              Document Audit
            </h1>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
              Upload your invoices and optional reference POs. Our AI will automatically extract, match, and audit them for compliance.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">

            {/* Invoice Upload Card (Required) */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-shadow duration-300">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 text-sm font-bold">1</span>
                  Invoice
                </h2>
                {uploadedFile && <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full flex items-center gap-1"><FiCheck /> Ready</span>}
              </div>

              <div
                className={`
                relative group cursor-pointer
                border-2 border-dashed rounded-xl p-8 transition-all duration-300
                flex flex-col items-center justify-center text-center
                min-h-[240px]
                ${isDraggingInvoice
                    ? 'border-blue-500 bg-blue-50'
                    : uploadedFile
                      ? 'border-green-300 bg-green-50/30'
                      : 'border-gray-200 hover:border-blue-400 hover:bg-gray-50'
                  }
              `}
                onDragOver={(e) => { e.preventDefault(); setIsDraggingInvoice(true) }}
                onDragLeave={() => setIsDraggingInvoice(false)}
                onDrop={(e) => {
                  e.preventDefault()
                  setIsDraggingInvoice(false)
                  const file = e.dataTransfer.files[0]
                  if (file) setUploadedFile(file)
                }}
              >
                <input
                  type="file"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  onChange={handleInvoiceChange}
                  accept=".pdf,.jpg,.jpeg,.png"
                />

                {uploadedFile ? (
                  <div className="space-y-3 animate-in fade-in zoom-in duration-300">
                    <div className="w-16 h-16 mx-auto rounded-full bg-green-100 flex items-center justify-center text-green-600">
                      <FiFileText className="w-8 h-8" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 truncate max-w-[200px]">{uploadedFile.name}</p>
                      <p className="text-sm text-gray-500">{(uploadedFile.size / 1024).toFixed(1)} KB</p>
                    </div>
                    <button
                      onClick={(e) => { e.stopPropagation(); setUploadedFile(null) }}
                      className="text-xs text-red-500 hover:text-red-700 font-medium z-10 relative"
                    >
                      Remove File
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="w-16 h-16 mx-auto rounded-full bg-blue-50 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <FiUploadCloud className={`w-8 h-8 ${isDraggingInvoice ? 'text-blue-600' : 'text-blue-500'}`} />
                    </div>
                    <div>
                      <p className="text-lg font-medium text-gray-700">Drop Invoice Here</p>
                      <p className="text-sm text-gray-400 mt-1">or click to browse</p>
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-4 flex gap-2 justify-center">
                {['PDF', 'JPG', 'PNG'].map(ext => (
                  <span key={ext} className="px-2 py-1 bg-gray-100 text-gray-500 text-xs rounded-md font-medium">{ext}</span>
                ))}
              </div>
            </div>

            {/* PO Upload Card (Optional) */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-shadow duration-300">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-purple-100 text-purple-600 text-sm font-bold">2</span>
                  Reference PO <span className="text-gray-400 text-sm font-normal ml-1">(Optional)</span>
                </h2>
                {poFile && <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full flex items-center gap-1"><FiCheck /> Ready</span>}
              </div>

              <div
                className={`
                relative group cursor-pointer
                border-2 border-dashed rounded-xl p-8 transition-all duration-300
                flex flex-col items-center justify-center text-center
                min-h-[240px]
                ${isDraggingPO
                    ? 'border-purple-500 bg-purple-50'
                    : poFile
                      ? 'border-green-300 bg-green-50/30'
                      : 'border-gray-200 hover:border-purple-400 hover:bg-gray-50'
                  }
              `}
                onDragOver={(e) => { e.preventDefault(); setIsDraggingPO(true) }}
                onDragLeave={() => setIsDraggingPO(false)}
                onDrop={(e) => {
                  e.preventDefault()
                  setIsDraggingPO(false)
                  const file = e.dataTransfer.files[0]
                  if (file) setPoFile(file)
                }}
              >
                <input
                  type="file"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  onChange={handlePoFileChange}
                  accept=".pdf,.jpg,.jpeg,.png"
                />

                {poFile ? (
                  <div className="space-y-3 animate-in fade-in zoom-in duration-300">
                    <div className="w-16 h-16 mx-auto rounded-full bg-green-100 flex items-center justify-center text-green-600">
                      <FiFileText className="w-8 h-8" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 truncate max-w-[200px]">{poFile.name}</p>
                      <p className="text-sm text-gray-500">{(poFile.size / 1024).toFixed(1)} KB</p>
                    </div>
                    <button
                      onClick={(e) => { e.stopPropagation(); setPoFile(null) }}
                      className="text-xs text-red-500 hover:text-red-700 font-medium z-10 relative"
                    >
                      Remove File
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="w-16 h-16 mx-auto rounded-full bg-purple-50 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <FiFileText className={`w-8 h-8 ${isDraggingPO ? 'text-purple-600' : 'text-purple-500'}`} />
                    </div>
                    <div>
                      <p className="text-lg font-medium text-gray-700">Drop PO Here</p>
                      <p className="text-sm text-gray-400 mt-1">to compare directly</p>
                    </div>
                  </div>
                )}
              </div>
              <div className="mt-4 flex gap-2 justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="px-2 py-1 text-transparent text-xs select-none">.</span>
              </div>
            </div>
          </div>

          {/* Action Section */}
          <div className="flex flex-col items-center space-y-6">
            <button
              onClick={handleAnalyze}
              disabled={!uploadedFile || loading || showAnimation}
              className={`
              relative px-12 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300
              ${!uploadedFile || loading || showAnimation
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed shadow-none hover:transform-none'
                  : 'bg-indigo-600 text-white hover:bg-indigo-700 ring-4 ring-indigo-50'
                }
            `}
            >
              {(loading || showAnimation) ? (
                <span className="flex items-center gap-3">
                  <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing Document...
                </span>
              ) : (
                'Start Audit Analysis'
              )}
            </button>

            {error && (
              <div className="flex items-center gap-2 px-4 py-3 bg-red-50 text-red-700 rounded-lg border border-red-200 animate-in fade-in slide-in-from-top-2">
                <FiAlertCircle className="w-5 h-5" />
                <p className="font-medium">{error}</p>
              </div>
            )}

            <p className="text-sm text-gray-400">
              Securely processed. Data is never shared with third parties.
            </p>
          </div>

        </div>
      </div>
    </>
  )
}

export default Upload
