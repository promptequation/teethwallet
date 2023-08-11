import { gql } from "nuxt-graphql-request";
import { userlookupType } from '~/types/companyUser'

const SET_APPROVAL_STATUS = "SET_APPROVAL_STATUS"

export const state = () => ({
    approvalStatuses: []
});

export const getters = {
    approvalStatuses(state) {
        return state.approvalStatuses
    },
    getApprovedStatus(state) {
        return state.approvalStatuses.find((item) => {
            return item.name === 'Approve'
        })
    },
    getPendingStatus(state) {
        return state.approvalStatuses.find((item) => {
            return item.name === 'Pending'
        })
    },
    getRejectStatus(state) {
        return state.approvalStatuses.find((item) => {
            return item.name === 'Reject'
        })
    }
};

export const mutations = {
    [SET_APPROVAL_STATUS](state, payload) {
        state.approvalStatuses = payload
    }
};

export const actions = {

};
