import { gql } from 'nuxt-graphql-request';

const SET_NOTIFICATIONS = "SET_NOTIFICATIONS"
const PUSH_NOTIFICATIONS = 'PUSH_NOTIFICATIONS'

export const state = () => ({
    notifications: [],
})


export const getters = {
    notifications(state) {
        return state.notifications
    },
}

export const mutations = {
    [SET_NOTIFICATIONS](state, payload) {
        state.notifications = payload
    },
    [PUSH_NOTIFICATIONS](state, payload) {
        state.notifications.unshift(...payload)
    },
}

export const actions = {
    async fetchNotifications({ }, { userId }) {
        const query = gql`
            query($userId: Int) {
                notifications(userId: $userId) {
                    id
                    isRead
                    createdBy {
                        name
                    }
                    createdFor {
                        name
                    }
                    company {
                        name
                    }
                    notificationType
                    createdAt
                    appointment{
                        id
                    }
                    appointmentFollowUp{
                        id 
                        followUpDate
                    }
                 }
            }
        `;
        const variables = { userId }
        return await this.$graphql.default.request(query, variables);
    },

    async deleteNotification({ }, { id }) {
        const mutation = gql`
            mutation ($id: ID) {
                deleteNotification(input: $id) {
                    notification {
                       id
                    }
                }
            }
        `;
        const variables = { id };
        return await this.$graphql.default.request(mutation, variables);
    },

    async updateNotification({ }, { id, isRead }) {
        const mutation = gql`
            mutation($id: ID, $isRead: Boolean) {
                updateNotification(input: { id: $id, isRead: $isRead }) {
                    notification {
                        isRead
                    }
                }
            }
        `;
        const variables = { id, isRead };
        return await this.$graphql.default.request(mutation, variables);
    },
}




