export async function useRegisterParticipation({ username, mail_address, event_id }) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, mail_address, event_id })
    })

    const data = await response.json()

    if (response.ok) {
      return { success: true, data }
    } else {
      return { success: false, error: data.error || '登録に失敗しました' }
    }
  } catch (error) {
    return { success: false, error: error.message || '通信エラーが発生しました' }
  }
}
