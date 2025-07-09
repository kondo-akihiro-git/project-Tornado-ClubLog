// src/network/useGetEvent.js
export async function useGetEvent(token) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/events?token=${token}`)
    if (!res.ok) throw new Error((await res.json()).error)
    const data = await res.json()
    return { success: true, data }
  } catch (error) {
    return { success: false, error: error.message }
  }
}