
import { useStore } from "@nuxtjs/composition-api";

const useJoinClinic = () => {

    const { dispatch, commit } = useStore()

    const fetchCompanies = async ({ name, langId }) => {
        try {
            const { companies } = await dispatch('clinic/fetchCompanies', { name, langId })
            const newCompanies = companies.edges.map(item => {
                let company= item.node
                if (item.node.companylangSet && item.node.companylangSet.edges?.length > 0) {
                    company =  {
                        id: item.node.id,
                        name: item.node.companylangSet.edges[0]?.node?.name,
                        city: item.node.companylangSet.edges[0]?.node?.city,
                        code: item.node.companylangSet.edges[0]?.node?.code,
                        state: item.node.companylangSet.edges[0]?.node?.state,
                        street: item.node.companylangSet.edges[0]?.node?.street,
                        street2: item.node.companylangSet.edges[0]?.node?.street2,
                        zipcode: item.node.companylangSet.edges[0]?.node?.zipcode,
                        zipcode: item.node.companylangSet.edges[0]?.node?.zipcode,
                        country: item.node.companylangSet.edges[0]?.node?.country,
                        isActive: item.node.isActive,
                        companyuserSet: item.node.companyuserSet,
                    }
                }
                return item = {node: company}
              })
            commit('clinic/SET_CLINICS', newCompanies)
        } catch (error) {
            console.log(error);
        }
    }

    const fetchAuthUserCompanies = async ({ userId, isOwner, groupName, statusId, approvalById, langId }) => {
        try {
            const { userCompany } = await dispatch('clinic/fetchAuthUserCompanies', { userId, isOwner, groupName, statusId, approvalById, langId })
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
            commit('clinic/SET_AUTH_USER_CLINICS', newUserCompany)
            return newUserCompany
        } catch (error) {
            console.log(error);
        }
    }

    const fetchRelatedCompaniesByAuthUser = async ({ userId, isOwner, groupName, statusId, approvalById, langId }) => {
        try {
            const { userCompany } = await dispatch('clinic/fetchAuthUserCompanies', { userId, isOwner, groupName, statusId, approvalById, langId })
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
            commit('clinic/SET_RELATED_CLINICS_BY_AUTH_USER', newUserCompany)
        } catch (error) {
            console.log(error);
        }
    }

    const fetchActiveCompanyForUser = async ({ userId, isActive, groupName, statusId }) => {
        try {
            return await dispatch('clinic/fetchActiveCompanyForUser', { userId, isActive, groupName, statusId })
        } catch (error) {
            console.log(error);
        }
    }

    const fetchAllPatientsByCompanyDoctor = async ({ companyId, doctorId, groupName, statusId }) => {
        try {
            return await dispatch('clinic/fetchAllPatientsByCompanyDoctor', { companyId, doctorId, groupName, statusId })
        } catch (error) {
            console.log(error);
        }
    }

    return {
        fetchCompanies,
        fetchAuthUserCompanies,
        fetchRelatedCompaniesByAuthUser,
        fetchAllPatientsByCompanyDoctor,
        fetchActiveCompanyForUser,
    }
}


export default useJoinClinic



