export function useLogout() {
  localStorage.removeItem('user') // ユーザー情報削除
  window.location.href = '/login' // ログイン画面にリダイレクト
}
