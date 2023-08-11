import { useStore } from '@nuxtjs/composition-api'

const useAccessManagement = () => {

    const { dispatch, commit } = useStore()


    const fetchAccessableDoctorLists = async () => {
        try {
            const { doctors } = await dispatch('manage-access/fetchAccessableDoctorLists')
            commit('manage-access/SET_DOCTORS', doctors)
        } catch (error) {
            console.log(error);
        }
    }

    const bannedTheDoctor = async (doctorId) => {
        try {
            const { doctors } = await dispatch('manage-access/bannedTheDoctor', { doctorId })
            commit('manage-access/SET_DOCTORS', doctors)
        } catch (error) {
            console.log(error)
        }
    }
    const accessTheDoctor = async (doctorId) => {
        try {
            const { doctors } = await dispatch('manage-access/accessTheDoctor', { doctorId })
            commit('manage-access/SET_DOCTORS', doctors)
        } catch (error) {
            console.log(error)
        }
    }
    const accessDoctorsProfile = async (doctorId) => {
        try {
            const { doctors } = await dispatch('manage-access/accessDoctorsProfile', { doctorId })
            commit('manage-access/SET_DOCTORS', doctors)
        } catch (error) {
            console.log(error)
        }
    }
    return {
        fetchAccessableDoctorLists,
        bannedTheDoctor,
        accessTheDoctor,
        accessDoctorsProfile,
    }

}

export default useAccessManagement