/**
 * RiskLevelBadge Component
 * 
 * Displays risk level badge for agent analysis
 * Used in the agent analysis panel
 */

const RiskLevelBadge = ({ riskLevel }) => {
  const getRiskConfig = (level) => {
    switch (level?.toLowerCase()) {
      case 'low':
        return {
          label: 'Low Risk',
          className: 'bg-success-50 text-success-700 border-success-300'
        }
      case 'medium':
        return {
          label: 'Medium Risk',
          className: 'bg-warning-50 text-warning-700 border-warning-300'
        }
      case 'high':
        return {
          label: 'High Risk',
          className: 'bg-warning-100 text-warning-800 border-warning-400'
        }
      case 'critical':
        return {
          label: 'Critical Risk',
          className: 'bg-danger-50 text-danger-700 border-danger-300'
        }
      default:
        return {
          label: 'Unknown',
          className: 'bg-gray-50 text-gray-700 border-gray-300'
        }
    }
  }

  const config = getRiskConfig(riskLevel)

  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-md text-sm font-semibold border ${config.className}`}>
      {config.label}
    </span>
  )
}

export default RiskLevelBadge

