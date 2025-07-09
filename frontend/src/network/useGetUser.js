// src/network/useGetUser.js
export async function useGetUser(user_id) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/user/${user_id}/info`)
    const data = await response.json()  
    return data
  } catch (error) {
    console.error('API fetch error:', error)
    return { users: [] }
  }
}
