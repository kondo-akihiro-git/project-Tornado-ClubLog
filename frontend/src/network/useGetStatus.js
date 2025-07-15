// src/network/useGetStatus.js
export const useGetStatus = async ({ user_id, event_id }) => {
  const params = new URLSearchParams({ user_id, event_id })
  const res = await fetch(`${import.meta.env.VITE_API_URL}/approval?${params}`, {
    method: 'GET',
  })

  if (!res.ok) {
    throw new Error('ステータス取得に失敗しました')
  }

  return await res.json()
}
