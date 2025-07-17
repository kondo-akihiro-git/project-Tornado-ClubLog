// src/network/useGetParticipants.js
export async function useGetParticipants(owner_id) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/participants`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ owner_id })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.error || '取得に失敗しました')
    }

    return await res.json()
  } catch (err) {
    console.error("API fetch error:", err)
    return { clubs: [] }
  }
}
