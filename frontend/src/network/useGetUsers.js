// src/network/useGetUsers.js
export async function useGetUsers(limit = 6, offset = 0) { // ★引数追加
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/users?limit=${limit}&offset=${offset}`
    )
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API fetch error:', error)
    return { user_participation: [] }
  }
}
