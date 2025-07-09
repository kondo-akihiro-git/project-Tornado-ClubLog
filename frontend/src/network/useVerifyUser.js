// src/network/useVerifyUser.js
export async function useVerifyUser(mail_address) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mail_address })
    })
    if (!res.ok) throw new Error((await res.json()).error)
    const data = await res.json()
    return { success: true, data }
  } catch (error) {
    return { success: false, error: error.message }
  }
}