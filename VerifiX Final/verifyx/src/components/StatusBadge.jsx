/**
 * StatusBadge Component
 * 
 * Displays a status badge with appropriate color coding
 * Used for receipt status indicators (Safe, Risky, Fake)
 */

const StatusBadge = ({ status }) => {
  const getStatusConfig = (status) => {
    switch (status?.toLowerCase()) {
      case 'safe':
        return {
          label: 'Safe',
          className: 'bg-success-50 text-success-600 border-success-200'
        }
      case 'risky':
        return {
          label: 'Risky',
          className: 'bg-warning-50 text-warning-600 border-warning-200'
        }
      case 'fake':
        return {
          label: 'Fake',
          className: 'bg-danger-50 text-danger-600 border-danger-200'
        }
      default:
        return {
          label: 'Unknown',
          className: 'bg-gray-50 text-gray-600 border-gray-200'
        }
    }
  }

  const config = getStatusConfig(status)

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border ${config.className}`}>
      {config.label}
    </span>
  )
}

export default StatusBadge

