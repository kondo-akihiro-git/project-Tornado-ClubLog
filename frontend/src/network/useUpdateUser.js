// src/network/useUpdateUser.js
export async function useUpdateUser(user_id, updateData) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/user/${user_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData),
    })

    const data = await res.json()

    if (!res.ok) throw new Error(data.error || '更新に失敗しました')
    return { success: true, data }
  } catch (error) {
    console.error('ユーザー更新エラー:', error)
    return { success: false, error: error.message }
  }
}
