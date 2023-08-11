export const state = () => ({
    Sidebar_drawer: null,
    SidebarColor: 'white',
    SidebarBg: '',
    showOverlay: false,
    loading: false,
})


export const mutations = {
    SET_SIDEBAR_DRAWER(state, payload) {
        state.Sidebar_drawer = payload
    },
    SET_SIDEBAR_COLOR(state, payload) {
        state.SidebarColor = payload
    },
    SET_OVERLAY(state, payload) {
        state.showOverlay = payload
    },
    SET_LOADING(state, payload) {
        state.loading = payload
    }
}


export const actions = {
    async nuxtServerInit({ dispatch }) {
        const token = this.$cookies.get('JWT')
        if (token) {
            await dispatch('auth/setUserProfile', token)
        }
    }
}