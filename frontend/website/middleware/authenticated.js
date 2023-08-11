const START_URL = '/start'
export default function async ({ store, redirect }) {
    const token = store.state.auth?.token || false;

    if (!token) {
        return redirect(START_URL)
    }
    return store.dispatch('auth/verifyToken', token)
        .then(tokenIsValid => {
            if (!tokenIsValid) {
                redirect(START_URL)
            }
        })
        .catch(error => {
            redirect(START_URL)
        })
}