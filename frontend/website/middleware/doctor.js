const START_URL = '/start'
export default function async({ store, redirect }) {
    const token = store.state.auth?.token || false;
    if (!token) {
        return redirect(START_URL)
    }

    const selectedProfile = store.state.auth.profile
    let doctor = false
    selectedProfile?.groups?.edges.forEach(item => {
        if (item.node.name === 'Doctor') {
            return doctor = true
        }
    })

    if (!doctor) {
        return redirect('/admin')
    }
}