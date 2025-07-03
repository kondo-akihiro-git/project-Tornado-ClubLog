// src/network/useLogin.js
export async function useLogin() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/`)
    const data = await response.text()
    return data
  } catch (error) {
    console.error('API fetch error:', error)
    return 'Error fetching from API'
  }
}
