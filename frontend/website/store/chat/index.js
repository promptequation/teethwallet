import { getField, updateField } from "vuex-map-fields";
import { gql } from "nuxt-graphql-request";
import dayjs from 'dayjs';
import groupBy from 'lodash.groupby';

const snakeToCamel = str =>
    str.toLowerCase().replace(/([-_][a-z])/g, group =>
        group.slice(-1).toUpperCase());

const findConnectedUser = (connection, authUserId) => {
    let lastConversation = null
    if (connection.coversationConnectionId.edges.length > 0) {
        lastConversation = connection.coversationConnectionId.edges[0].node
    }
    if (connection.receiver && Number(connection.receiver.id) === Number(authUserId)) {
        return {
            ...connection.sender,
            lastConversation
        }
    } else {
        return {
            ...connection.receiver,
            lastConversation
        }
    }
}

import {
    SET_LOADING,
    SET_CONVERSATIONS,
    SET_USER,
    SET_AUTH_USER,
    PUSH_CONVERSATION,
    UPDATE_CONVERSATION,
    MARK_AS_SEEN_CONVERSATION,
    PUSH_SOCKET_CONVERSATION,
    SET_CONNECTED_USERS,
    SET_PATIENT_OR_DOCTOR__USERS,
    SET_LAST_CONVERSATION,
} from "./types";

export const state = () => ({
    loading: false,
    conversations: null,
    user: null,
    authUser: null,
    connectedUsers: []
});

export const getters = {
    getField,
    loading (state) { return state.loading },
    conversations (state) {
        let array = [];
        if (state.conversations) {
            const edges = JSON.parse(JSON.stringify(state.conversations.edges))
            array = edges.map((item) => {
                const conversation = {
                    ...item.node
                }
                if (item.node.datetime) {
                    conversation.date = dayjs(item.node.datetime).format('YYYY-MM-DD')
                }
                return conversation
            })
        }
        return groupBy(array, 'date');
    },
    getConnectedUsers (state) {
        return [...new Map(state.connectedUsers.map(item => [item['id'], item])).values()]
    },
};

export const mutations = {
    updateField,
    [SET_LOADING] (state, payload) {
        state.loading = payload
    },
    [SET_CONVERSATIONS] (state, payload) {
        state.conversations = payload
    },
    [PUSH_CONVERSATION] (state, payload) {
        const edges = state.conversations;
        if (edges) {
            const item = {
                node: payload,
                sender: state.authUser,
            }
            edges.edges.push(item)
        }
    },
    [UPDATE_CONVERSATION] (state, payload) {
        const conversations = state.conversations;
        if (conversations) {
            const index = conversations.edges.findIndex(_ => _.node.id === payload.id)
            if (index > -1) {
                state.conversations.edges.splice(index, 1, { node: payload })
            }
        }
    },
    [MARK_AS_SEEN_CONVERSATION] (state) {
        const edges = state.conversations;
        if (edges) {
            state.conversations.edges = edges.edges.map(item => {
                item.node.isSeen = true;
                return item;
            })
        }
    },
    [PUSH_SOCKET_CONVERSATION] (state, payload) {
        const edges = state.conversations;
        if (edges) {
            const array = JSON.parse(payload)
            const obj = array[0]
            const fields = { ...obj.fields }
            let output = {}
            for (var key in fields) {
                output[snakeToCamel(key)] = fields[key];
            }

            let sender = state.user
            if (state.authUser && state.authUser.id == output.sender) {
                sender = state.authUser
            }

            const node = {
                id: obj.pk,
                ...output,
                sender
            }

            let receiverId = null
            if (Number(node.createdBy) === Number(state.authUser.id)) {
                receiverId = node.receiver
            } else {
                receiverId = node.createdBy
            }

            const index = edges.edges.findIndex(_ => _.node.id === obj.pk)
            if (index > -1) {
                state.conversations.edges.splice(index, 1, { node })
                const lastConversation = state.conversations.edges.slice(-1)[0]
                this.commit('chat/SET_LAST_CONVERSATION', { lastConversation, receiver: receiverId })
            } else {
                if (Number(receiverId) === Number(state.user.id)) {
                    state.conversations.edges.push({ node })
                }
                this.commit('chat/SET_LAST_CONVERSATION', { lastConversation: node, receiver: receiverId })
            }
        }
    },
    [SET_USER] (state, payload) {
        state.user = payload
    },
    [SET_AUTH_USER] (state, payload) {
        state.authUser = payload
    },
    [SET_CONNECTED_USERS] (state, { authUserId, connections }) {
        const connectedUsers = connections.map(connection => {
            return findConnectedUser(connection, authUserId)
        })
        state.connectedUsers = connectedUsers
    },
    [SET_PATIENT_OR_DOCTOR__USERS] (state, payload) {
        if (payload && payload.length > 0) {
            state.connectedUsers = payload.concat(state.connectedUsers)
        }
    },
    [SET_LAST_CONVERSATION] (state, { lastConversation, receiver }) {
        let lastMessage = lastConversation.node ? lastConversation.node : lastConversation
        state.connectedUsers = state.connectedUsers.map(user => {
            if (Number(user.id) === Number(receiver)) {
                user.lastConversation = JSON.parse(JSON.stringify(lastMessage))
            }
            return user
        })
    },
};

export const actions = {
    async checkConnection ({ }, { sender, receiver }) {
        const query = gql`
        query($sender: ID, $receiver: ID) {
            checkConnection(sender: $sender, receiver: $receiver) {
                id
            }
        }
    `;

    const variables = { sender, receiver };

    return await this.$graphql.default.request(query, variables);
    },

    async createConnection ({ }, { sender, receiver }) {
        const mutation = gql`
        mutation($sender: ID, $receiver: ID) {
            createConnection(input: {
            sender: $sender,
            receiver: $receiver
            }) {
                connection {
                    id
                }
            }
        }
    `;

    const variables = { sender, receiver };

    return await this.$graphql.default.request(mutation, variables);
    },

    async fetchConversations ({ }, { connectionId }) {
        const query = gql`
        query ($connectionId: Float) {
            conversations(connection_Id: $connectionId) {
                edges {
                    node {
                        id
                        connection{
                            id
                        }
                        message
                        datetime
                        sender {
                            id
                            name
                            username
                            avatar
                        }
                        isSeen
                        isEdited
                        isAutoMessage
                    }
                }
            }
        }
    `;

    const variables = { connectionId };
    return await this.$graphql.default.request(query, variables);
    },

    async updateMessage ({ }, { id, body }) {
        const mutation = gql`
        mutation($id: ID, $body: String) {
            updateMessage(messageData: { id: $id, body: $body }) {
                message {
                    id
                    body
                }
            }
        }
    `;

    const variables = { id, body };

    return await this.$graphql.default.request(mutation, variables);
    },

    async fetchConnectedUser ({ }, { userId }) {
        const query = gql`
        query($userId:ID){
            connections(id:$userId) {
                id
                sender {
                    id
                    firstName
                    lastName
                    name
                    email
                    username
                    avatar
                }
                receiver {
                    id
                    firstName
                    lastName
                    name
                    email
                    username
                    avatar
                }
                coversationConnectionId(last: 1) {
                    edges {
                        node {
                            message
                        }
                    }
                }
            }
        }
    `;

    const variables = { userId }
    return await this.$graphql.default.request(query, variables);
    },

};
