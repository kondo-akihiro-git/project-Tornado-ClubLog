// src/network/useLogin.js
export async function useLogin({ mail_address, password }) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mail_address, password })
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.error || 'ログインに失敗しました')
    }

    return await res.json()
  } catch (err) {
    throw new Error(err.message)
  }
}
