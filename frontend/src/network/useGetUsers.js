// src/network/useGetUsers.js
export async function useGetUsers() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/users`)
    const data = await response.json() 
    return data
  } catch (error) {
    console.error('API fetch error:', error)
    return { users: [] }
  }
}
