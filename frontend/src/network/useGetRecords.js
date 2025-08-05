// frontend/src/network/useGetRecords.js
export async function useGetRecords(userId) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/user/${userId}/records`)
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API fetch error (records):', error)
    return { records: [] }
  }
}
