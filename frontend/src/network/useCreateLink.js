// src/network/useCreateLink.js
export async function useCreateLink(url_token, event_id) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/link`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url_token, event_id })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'リンク作成に失敗しました');
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
