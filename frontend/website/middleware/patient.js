
const START_URL = '/start'
export default function async({ store, redirect }) {
    const token = store.state.auth?.token || false;
    if (!token) {
        return redirect(START_URL)
    }
    const selectedProfile = store.state.auth.profile

    let patient = false
    selectedProfile?.groups?.edges.forEach(item => {
        if (item.node.name === 'Patient') {
            return patient = true
        }
    })
    if (!patient) {
        return redirect('/admin')
    }
}