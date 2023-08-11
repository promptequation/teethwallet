
import { useStore } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import { provideToast, useToast } from 'vue-toastification/composition'

const useMyInvitations = () => {
    const { $t } = useNuxtTranslator()
    provideToast({
        timeout: 4000, position: 'bottom-center'
    })
    const toast = useToast()


    const { dispatch, commit } = useStore()

    const fetchUserLookup = async () => {
        try {
            return await dispatch('invitation/fetchUserLookup')
        } catch (error) {
            console.log(error);
        }
    }

    const fetchPatientInvitations = async ({ companyId, groupName, doctorId, statusId, userId, from }) => {
        try {
            const { userCompany } = await dispatch('invitation/fetchPatientInvitations', { companyId, groupName, doctorId, statusId, userId })
            if (from === 'patientInvitations') {
                commit('invitation/SET_PATIENT_INVITATIONS', userCompany.edges)
            } else if (from === 'doctorInvitations') {
                commit('invitation/SET_DOCTOR_INVITATIONS', userCompany.edges)
            } else if (from === 'myPatients') {
                commit('patient/SET_PATIENTS', userCompany.edges)
            } else if (from === 'message') {
                commit('patient/SET_PATIENTS', userCompany.edges)
            }

        } catch (error) {
            console.log(error);
        }
    }

    const fetchDoctorInvitations = async ({ companyId, groupName, statusId }) => {
        try {
            const { userCompany } = await dispatch('invitation/fetchDoctorInvitations', { companyId, groupName, statusId })
            commit('invitation/SET_DOCTOR_INVITATIONS', userCompany.edges)
        } catch (error) {
            console.log(error);
        }
    }

    const fetchDoctorsByPatient = async ({ userId, groupName, statusId }) => {
        try {
            return await dispatch('invitation/fetchDoctorsByPatient', { userId, groupName, statusId })
        } catch (error) {
            console.log(error);
        }
    }

    const fetchPatienstByDoctor = async ({ companyId, groupName, doctorId, statusName, statusId }) => {
        try {
            return await dispatch('invitation/fetchPatienstByDoctor', { companyId, groupName, doctorId, statusName, statusId })
        } catch (error) {
            console.log(error);
        }
    }

    const fetchClinicInvitations = async ({ userId, groupName, statusId, isOwner }) => {
        try {
            const { userCompany } = await dispatch('invitation/fetchClinicInvitations', { userId, groupName, statusId, isOwner })
            commit('invitation/SET_CLINIC_INVITATIONS', userCompany.edges)
        } catch (error) {
            console.log(error);
        }
    }

    const acceptPatientInvitation = async ({ id, doctorId, approvalById, status, joinedDatetime, approvalAt, from, requestType }) => {
        try {
            await dispatch('invitation/acceptPatientInvitation', { id, doctorId, approvalById, status, joinedDatetime, approvalAt, requestType })

            if (from === 'myInvitation') {
                commit('invitation/REMOVE_PATIENT', { id })
            } else if (from === 'myPatient') {
                commit('patient/UPDATED_STATUS', { status, id })
            } else if (from === 'accessManagement') {
                commit('patient/UPDATED_PATIENT_REQUEST_STATUS', { status, id })
            } else if (from === 'doctorInvitations') {
                commit('invitation/REMOVE_DOCTOR_INVITATION', { id })
            } else if (from === 'clinicInvitations') {
                commit('invitation/REMOVE_CLINIC_INVITATION', { id })
            }

            toast.success(`${$t('toastMessage.Invitations Successfully Accepted!')}`)
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }

    const rejectPatientInvitation = async ({ id, doctorId, approvalById, status, approvalAt, from, requestType }) => {
        try {
            await dispatch('invitation/rejectPatientInvitation', { id, doctorId, approvalById, status, approvalAt, requestType })

            if (from === 'myInvitation') {
                commit('invitation/REMOVE_PATIENT', { id })
            } else if (from === 'myPatient') {
                commit('patient/UPDATED_STATUS', { status, id })
            } else if (from === 'accessManagement') {
                commit('patient/UPDATED_PATIENT_REQUEST_STATUS', { status, id })
            } else if (from === 'doctorInvitations') {
                commit('invitation/REMOVE_DOCTOR_INVITATION', { id })
            } else if (from === 'clinicInvitations') {
                commit('invitation/REMOVE_CLINIC_INVITATION', { id })
            }

            toast.success(`${$t('toastMessage.Invitations Successfully Rejected!')}`)

        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }

    const acceptDoctorInvitation = async (doctorInvitationId) => {
        try {
            await dispatch('invitation/acceptDoctorInvitation', { doctorInvitationId })
            commit('invitation/REMOVE_DOCTOR_INVITATION', { doctorInvitationId })
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }

    const rejectDoctorInvitation = async (doctorInvitationId) => {
        try {
            await dispatch('invitation/rejectDoctorInvitation', { doctorInvitationId })
            commit('invitation/REMOVE_DOCTOR_INVITATION', { doctorInvitationId })
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }


    return {
        fetchUserLookup,
        fetchDoctorInvitations,
        fetchPatientInvitations,
        fetchClinicInvitations,
        acceptPatientInvitation,
        rejectPatientInvitation,
        acceptDoctorInvitation,
        rejectDoctorInvitation,
        fetchDoctorsByPatient,
        fetchPatienstByDoctor,
    }


}

export default useMyInvitations










