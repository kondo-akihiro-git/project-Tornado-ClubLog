// src/network/useGetParticipants.js
export async function useGetParticipants() {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/participants`)
    const data = await res.json()
    return data
  } catch (err) {
    console.error("API fetch error:", err)
    return { clubs: [] }
  }
}
