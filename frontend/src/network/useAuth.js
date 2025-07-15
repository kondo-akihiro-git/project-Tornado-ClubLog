export async function useAuth(userId) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/auth`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId }),
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.error || '認証確認に失敗しました')
    }

    return await res.json()
  } catch (err) {
    throw new Error(err.message)
  }
}
