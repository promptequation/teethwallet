
import { useStore } from "@nuxtjs/composition-api";

const useMyPatient = () => {

    const { dispatch, commit } = useStore()

    const fetchMyPatientLists = async ({ doctorId, userId }) => {
        try {
            const { userCompany } = await dispatch('patient/fetchMyPatientLists', { doctorId, userId })
            commit('patient/SET_PATIENTS', userCompany.edges)
        } catch (error) {
            console.log(error);
        }
    }
    const fetchUserRequest = async ({ userId, groupName }) => {
        try {
            const { userCompany } = await dispatch('patient/fetchUserRequest', { groupName, userId })
            commit('patient/SET_PATIENT_REQUEST', userCompany.edges)
        } catch (error) {
            console.log(error);
        }
    }

    return {
        fetchMyPatientLists,
        fetchUserRequest,
    }

}

export default useMyPatient



