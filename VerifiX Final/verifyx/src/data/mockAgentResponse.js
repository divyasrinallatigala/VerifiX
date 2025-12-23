/**
 * Mock Agent Response Data
 * 
 * This file contains sample data that simulates what the AI agent will return.
 * In production, this data will come from an API endpoint.
 * 
 * Structure:
 * - receipts: Array of receipt objects with analysis results
 * - Each receipt contains agent-generated risk analysis data
 */

export const mockAgentResponse = {
  receipts: [
    {
      id: 'INV-2023-1825',
      vendor: 'ABC Supplies',
      amount: 16000,
      date: '2023-10-15',
      status: 'risky',
      agentAnalysis: {
        riskLevel: 'high',
        reasons: [
          'Duplicate invoice detected',
          'Paid $16,000 to ABC Supplies',
          'Unusual payment pattern for this vendor'
        ],
        confidenceScore: 0.92,
        notes: 'This invoice appears to be a duplicate of INV-2023-1788. The payment amount matches exactly, and the vendor name is identical. Recommend manual review.',
        evidenceImageUrl: null // Will be populated by agent if evidence image exists
      }
    },
    {
      id: 'INV-2023-1788',
      vendor: 'Pake Contractors',
      amount: 12500,
      date: '2023-10-12',
      status: 'risky',
      agentAnalysis: {
        riskLevel: 'medium',
        reasons: [
          'Vendor name variation detected',
          'Amount exceeds typical threshold'
        ],
        confidenceScore: 0.78,
        notes: 'Vendor name "Pake" may be a variation of "Pake Contractors". Amount is higher than usual for this vendor category.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1784',
      vendor: 'DuPcare Services',
      amount: 8500,
      date: '2023-10-10',
      status: 'risky',
      agentAnalysis: {
        riskLevel: 'medium',
        reasons: [
          'Duplicate invoice',
          'Vendor name inconsistency'
        ],
        confidenceScore: 0.81,
        notes: 'Duplicate invoice detected for Cfly Contractors. Vendor name shows inconsistency in records.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1794',
      vendor: 'Tech Solutions Inc',
      amount: 22000,
      date: '2023-10-08',
      status: 'risky',
      agentAnalysis: {
        riskLevel: 'high',
        reasons: [
          'Amount significantly above average',
          'Multiple flags in document analysis'
        ],
        confidenceScore: 0.88,
        notes: 'Invoice amount is 3x the average for this vendor. Document analysis flagged multiple suspicious patterns.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1765',
      vendor: 'Apax Builders',
      amount: 18500,
      date: '2023-10-05',
      status: 'risky',
      agentAnalysis: {
        riskLevel: 'medium',
        reasons: [
          'Duplicate invoice pattern',
          'Vendor verification pending'
        ],
        confidenceScore: 0.75,
        notes: 'Duplicate invoice pattern detected for Apax Builders. Vendor verification is still pending.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1739',
      vendor: 'Standard Office Supplies',
      amount: 3200,
      date: '2023-10-01',
      status: 'safe',
      agentAnalysis: {
        riskLevel: 'low',
        reasons: [
          'All checks passed',
          'Vendor verified'
        ],
        confidenceScore: 0.95,
        notes: 'Invoice passes all automated checks. Vendor is verified and amount is within expected range.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1720',
      vendor: 'Reliable Logistics',
      amount: 4500,
      date: '2023-09-28',
      status: 'safe',
      agentAnalysis: {
        riskLevel: 'low',
        reasons: [
          'Standard transaction',
          'No anomalies detected'
        ],
        confidenceScore: 0.93,
        notes: 'Standard transaction with verified vendor. No anomalies or suspicious patterns detected.',
        evidenceImageUrl: null
      }
    },
    {
      id: 'INV-2023-1705',
      vendor: 'Suspicious Corp',
      amount: 25000,
      date: '2023-09-25',
      status: 'fake',
      agentAnalysis: {
        riskLevel: 'critical',
        reasons: [
          'Document authenticity verification failed',
          'Vendor not found in registry',
          'Amount pattern matches known fraud cases'
        ],
        confidenceScore: 0.97,
        notes: 'CRITICAL: Document authenticity verification failed. Vendor "Suspicious Corp" is not found in any business registry. Amount and pattern match known fraud cases. Immediate review required.',
        evidenceImageUrl: null
      }
    }
  ]
}

/**
 * Helper function to get receipt by ID
 * TODO: Replace with API call in production
 */
export const getReceiptById = (id) => {
  return mockAgentResponse.receipts.find(receipt => receipt.id === id)
}

/**
 * Helper function to get all receipts
 * TODO: Replace with API call in production
 */
export const getAllReceipts = () => {
  return mockAgentResponse.receipts
}

