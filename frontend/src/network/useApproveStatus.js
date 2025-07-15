// network/useApproveStatus.js
export async function useApproveStatus({ user_id, event_id, status }) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/approval`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id, event_id, status })
    })

    const result = await response.json()
    if (!response.ok) throw new Error(result.error || '更新に失敗しました')
    return result
  } catch (error) {
    console.error('承認ステータス変更失敗:', error.message)
    throw error
  }
}
