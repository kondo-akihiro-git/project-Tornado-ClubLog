// src/network/useRegisterParticipation.js
export async function useRegisterParticipation({ mail_address, event_id }) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mail_address, event_id })  // password を削除
    })

    if (!res.ok) throw new Error((await res.json()).error)
    return { success: true }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
