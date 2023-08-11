import { gql } from 'nuxt-graphql-request'

const SET_DOCTORS = "SET_DOCTORS"

export const state = () => {
    doctors: []
}


export const getters = {
    accessableDoctors(state) {
        return state.doctors
    }
}

export const mutations = {
    [SET_DOCTORS](state, payload) {
        state.doctors = payload
    },
}

export const actions = {
    async fetchAccessableDoctorLists() {
        const query = gql`
          query {
            allDoctor{
                id
                name
            }
         }
        `;
        return await this.$graphql.default.request(query);
    },

    async bannedTheDoctor({ }, { doctorId }) {
        const query = gql`
          query {
            allDoctor{
                id
                name
            }
         }
        `;
        const variables = { doctorId }
        return await this.$graphql.default.request(query, variables);
    },

    async accessTheDoctor({ }, { doctorId }) {
        const query = gql`
          query {
            allDoctor{
                id
                name
            }
         }
        `;
        const variables = { doctorId }
        return await this.$graphql.default.request(query, variables);
    },

    async accessDoctorsProfile({ }, { doctorId }) {
        const query = gql`
          query {
            allDoctor{
                id
                name
            }
         }
        `;
        return await this.$graphql.default.request(query);
    },
}




