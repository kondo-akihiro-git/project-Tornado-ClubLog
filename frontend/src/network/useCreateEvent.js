export async function useCreateEvent(title, club_id) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, club_id })
    })
    if (!res.ok) throw new Error((await res.json()).error)
    const data = await res.json()
    return { success: true, data }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
