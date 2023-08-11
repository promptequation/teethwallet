

import { useContext, useStore } from "@nuxtjs/composition-api";
import { provideToast, useToast } from 'vue-toastification/composition';

const useManageClinic = () => {
    provideToast({
        timeout: 4000, position: 'bottom-center'
    })
    const { $dayjs } = useContext();
    const { dispatch, commit } = useStore()
    const toast = useToast()


    const fetchDoctorLists = async ({ groupName, statusId, companyName, userName, userEmail, langId }) => {
        try {
            const { userCompany } = await dispatch('clinic/fetchDoctorLists', { groupName, statusId, companyName, userName, userEmail, langId })
            const newUserCompany = userCompany.edges.map(item => {
                let company= item.node.company
                if (item.node.company &&  item.node.company.companylangSet && item.node.company.companylangSet.edges?.length > 0) {
                    company = {
                        id: item.node.company.id,
                        name: item.node.company.companylangSet.edges[0]?.node?.name
                    }
                }
                item.node.company = company
                return item
            })
            commit('clinic/SET_DOCTORS', newUserCompany)
        } catch (error) {
            console.log(error);
        }
    }

    const fetchSingleCompany = async ({ companyId, groupName }) => {
        try {
            return await dispatch('clinic/fetchSingleCompany', { companyId, groupName })
        } catch (error) {
            console.log(error);
        }
    }

    const fetchRequestedDoctorListByAuthUser = async ({ userId }) => {
        try {
            const { userCompany } = await dispatch('clinic/fetchRequestedDoctorListByAuthUser', { userId })
            commit('clinic/SET_REQUESTED_DOCTORS', userCompany.edges)
        } catch (error) {
            console.log(error);
        }
    }

    const createUserCompany = async ({ name, state, street, street2, city, zipcode, country, createdBy, updatedBy }) => {
        try {
            return await dispatch('clinic/createUserCompany', { name, state, street, street2, city, zipcode, country, createdBy, updatedBy })
        } catch (error) {
            console.log(error);
        }
    }
    const updateUserCompany = async ({ id, name, state, street, street2, city, zipcode, country, updatedBy }) => {
        try {
            return await dispatch('clinic/updateUserCompany', { id, name, state, street, street2, city, zipcode, country, updatedBy })
        } catch (error) {
            console.log(error);
        }
    }

    const createCompanyUserForCompanyOwner = async ({ companyId, userId, doctorId, groupId, status, isOwner, isActive, joinedDatetime, approvalById, approvalAt, requestedBy }) => {
        try {
            return await dispatch('clinic/createCompanyUserForCompanyOwner', { companyId, userId, doctorId, groupId, status, isOwner, isActive, joinedDatetime, approvalById, approvalAt, requestedBy })
        } catch (error) {
            console.log(error);
        }
    }

    const createDoctorTypeUserForCompany = async ({ companyId, userId, groupId, status, isOwner, isActive, requestedBy, joinedDatetime, requestType }) => {
        try {
            return await dispatch('clinic/createDoctorTypeUserForCompany', { companyId, userId, groupId, status, isOwner, isActive, requestedBy, joinedDatetime, requestType })
        } catch (error) {
            console.log(error);
        }
    }

    const createPatientTypeUserForCompany = async ({ companyId, userId, doctorId, groupId, status, isOwner, isActive, requestedBy, requestType }) => {
        try {
            return await dispatch('clinic/createPatientTypeUserForCompany', { companyId, userId, doctorId, groupId, status, isOwner, isActive, requestedBy, requestType })
        } catch (error) {
            console.log(error);
        }
    }


    const deleteUserCompany = async (userCompanyId) => {
        try {
            await dispatch('clinic/deleteUserCompany', { userCompanyId })
            commit('clinic/REMOVE_USER_COMPANY', { userCompanyId })
        } catch (error) {
            console.log(error);
        }
    }
    const deleteCompanyUser = async (companyUserId) => {
        try {
            await dispatch('clinic/deleteCompanyUser', { companyUserId })
        } catch (error) {
            console.log(error);
        }
    }

    const setActiveClinic = async ({ companyUserId, isActive, status }) => {
        try {
            return await dispatch('clinic/setActiveClinic', { companyUserId, isActive, status })
        } catch (error) {
            console.log(error);
        }
    }

    const fetchCities = () => {
        return [
            { text: "Dhaka", value: "bn" },
            { text: "Kolkata", value: "ar" },
            { text: "Islamabad", value: "pk" },
            { text: "Modina", value: "in" },
        ]
    }

    return {
        fetchDoctorLists,
        fetchSingleCompany,
        fetchRequestedDoctorListByAuthUser,
        createUserCompany,
        updateUserCompany,
        deleteUserCompany,
        deleteCompanyUser,
        fetchCities,
        createCompanyUserForCompanyOwner,
        createDoctorTypeUserForCompany,
        createPatientTypeUserForCompany,
        setActiveClinic,
    }

}

export default useManageClinic
