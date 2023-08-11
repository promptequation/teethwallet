import { gql } from 'nuxt-graphql-request'
import {
    useStore,
} from "@nuxtjs/composition-api";


const SET_PATIENTS = "SET_PATIENTS"
const UPDATED_STATUS = "UPDATED_STATUS"
const SET_DOCTOR_FOR_PATIENT = "SET_DOCTOR_FOR_PATIENT"
const SET_PATIENT_REQUEST = "SET_PATIENT_REQUEST"
const UPDATED_PATIENT_REQUEST_STATUS = "UPDATED_PATIENT_REQUEST_STATUS"

export const state = () => ({
    patients: [],
    patientDoctors: [],
    patientRequests: [],
})


export const getters = {
    getMyPatients(state) {
        const patientInvitations = state.patients.map(item => {
            return {
                id: item.node?.id,
                company_id: item.node.company?.id,
                company: item.node.company?.name,
                requestedBy: item.node.requestedBy?.name,
                requestedById: item.node.requestedBy?.id,
                doctorId: item.node.doctor?.id,
                doctorName: item.node.doctor?.name,
                userId: item.node.user?.id,
                name: item.node.user?.name,
                email: item.node.user?.email,
                phone: item.node.user?.phone,
                dateOfBirth: item.node.user?.dateOfBirth,
                requestedAt: item.node.requestedAt,
                joinedDatetime: item.node.joinedDatetime,
                status: item.node.status,
                approvalBy: item.node.approvalBy,
            }
        })

        return patientInvitations.filter(item => {
            return item.status.name !== 'Pending'
        })
    },
    getUserRequest(state) {
        const patientRequests = state.patientRequests.map(item => {
            return {
                id: item.node?.id,
                company_id: item.node.company?.id,
                company: item.node.company?.name,
                requestedBy: item.node.requestedBy?.name,
                requestedById: item.node.requestedBy?.id,
                doctorId: item.node.doctor?.id,
                doctorName: item.node.doctor?.name,
                userId: item.node.user?.id,
                name: item.node.user?.name,
                email: item.node.user?.email,
                phone: item.node.user?.phone,
                dateOfBirth: item.node.user?.dateOfBirth,
                requestedAt: item.node.requestedAt,
                joinedDatetime: item.node.joinedDatetime,
                status: item.node.status,
                approvalBy: item.node.approvalBy,
            }
        })

        return patientRequests.filter(item => {
            return item.status.name !== 'Pending'
        })
    },
    getMyApprovedPatients(state) {
        const patientInvitations = state.patients.map(item => {
            return {
                id: item.node?.id,
                company_id: item.node.company?.id,
                company: item.node.company?.name,
                requestedBy: item.node.requestedBy?.name,
                requestedById: item.node.requestedBy?.id,
                doctorId: item.node.doctor?.id,
                doctorName: item.node.doctor?.name,
                userId: item.node.user?.id,
                name: item.node.user?.name,
                email: item.node.user?.email,
                phone: item.node.user?.phone,
                dateOfBirth: item.node.user?.dateOfBirth,
                requestedAt: item.node.requestedAt,
                joinedDatetime: item.node.joinedDatetime,
                status: item.node.status,
                approvalBy: item.node.approvalBy,
            }
        })

        return patientInvitations.filter(item => {
            return item.status.name === 'Approve'
        })
    },
    getMyApprovedPatientsForMessage(state) {
        const patientInvitations = state.patients.map(item => {
            return {
                status: item.node.status,
                ...item.node.user,
                lastConversation: item.node.lastConversation
            }
        })

        const approvedPatients = patientInvitations.filter(item => {
            return item.status.name === 'Approve'
        })

        //get unique patients
        return [...new Map(approvedPatients.map(item =>
            [item['id'], item])).values()];
    },
    getPatientDoctors(state) {
        const newPatients = state.patientDoctors.map(item => {
            return {
                ...item.node.doctor,
                lastConversation: item.node.lastConversation
            }
        })

        //get unique doctors
        return [...new Map(newPatients.map(item =>
            [item['id'], item])).values()];
    }
}

export const mutations = {
    [SET_PATIENTS](state, payload) {
        state.patients = payload
    },

    [SET_DOCTOR_FOR_PATIENT](state, payload) {
        state.patientDoctors = payload
    },

    [SET_PATIENT_REQUEST](state, payload) {
        state.patientRequests = payload
    },

    [UPDATED_STATUS](state, { status, id }) {
        const patientIndex = state.patients.findIndex((item) => {
            return Number(item.node.id) === id
        })

        state.patients[patientIndex].node.status.name = status
        const authUser = this.state.auth.profile
        state.patients[patientIndex].node.approvalBy.id = authUser.id
        state.patients[patientIndex].node.approvalBy.name = authUser.name
    },
    [UPDATED_PATIENT_REQUEST_STATUS](state, { status, id }) {
        const patientIndex = state.patientRequests.findIndex((item) => {
            return Number(item.node.id) === id
        })

        state.patientRequests[patientIndex].node.status.name = status
        const authUser = this.state.auth.profile
        state.patientRequests[patientIndex].node.approvalBy.id = authUser.id
        state.patientRequests[patientIndex].node.approvalBy.name = authUser.name
    },
}

export const actions = {
    async fetchMyPatientLists({ }, { doctorId }) {
        const query = gql`
            query ($doctorId: Float) {
                userCompany(doctor_Id: $doctorId) {
                    edges {
                    node {
                        id
                        user {
                            id
                            name
                            email
                            phone
                            dateOfBirth
                        }
                        doctor{
                            id
                            name
                        }
                        company {
                            id
                            name
                        }
                        status {
                            id
                            name
                        }
                        approvalBy{
                            id
                            name
                       }
                       joinedDatetime
                    }
                    }
                }
            }
        `;
        const variables = { doctorId, userId }
        return await this.$graphql.default.request(query, variables);
    },
    async fetchUserRequest({ }, { groupName, userId }) {
        const query = gql`
            query ($groupName: String, $userId: Float) {
                userCompany(group_Name: $groupName, user_Id: $userId) {
                    edges {
                    node {
                        id
                        user {
                        id
                        name
                        email
                        phone
                        dateOfBirth
                        }
                        doctor {
                        id
                        name
                        }
                        company {
                        id
                        name
                        }
                        status {
                        id
                        name
                        }
                        approvalBy {
                        id
                        name
                        }
                        joinedDatetime
                    }
                    }
                }
                }
        `;
        const variables = { groupName, userId }
        return await this.$graphql.default.request(query, variables);
    },
}




