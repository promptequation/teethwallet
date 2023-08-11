// TODO move queries / mutations to separated file
// TODO create models to handle complex executions

import { gql } from 'graphql-request';
import { getField, updateField } from 'vuex-map-fields';
import { SET_APPOINTMENT_CODE, SET_DOCTORS, SET_GROUPS, SET_PATIENTS, SET_SPECIALITY } from "./types";

export const state = () => ({
  doctors: [],
  patients: [],
  specialities: [],
  appointmentCodes: [],
  groups: [],
})

export const getters = {
  getField,
  doctors(state) {
    return state.doctors
  },
  getAllDoctorWithOutAuthUser(state, getters, rootState) {
    const authUser = rootState.auth.profile
    return state.doctors.filter(doctor => {
      return Number(doctor.id) !== Number(authUser.id)
    })
  },
  patients(state) {
    return state.patients
  },
  specialities(state) {
    return state.specialities
  },
  appointmentCodes(state) {
    return state.appointmentCodes
  },
  groups(state) {
    return state.groups
  },
}

export const mutations = {
    updateField,
    [SET_DOCTORS](state, payload) {
        state.doctors = payload;
    },
    [SET_PATIENTS](state, payload) {
        state.patients = payload;
    },
    [SET_SPECIALITY](state, payload) {
        state.specialities = payload;
    },
    [SET_APPOINTMENT_CODE](state, payload) {
        const code = payload.edges.map((item) => {
            

                return {
                    id: item.node?.id,
                    name: item.node?.name,
                    codeType: item.node?.codeType,
                    description: item.node?.description,
                };
                       
          });

        state.appointmentCodes = code;
    },
    [SET_GROUPS](state, payload) {
        state.groups = payload;
    },
};

export const actions = {
  async addManagedPatient({ }, userData) {

    const mutation = gql`
      mutation ($userId: ID, $patientId: ID) {
        addManagedPatient(addData: { userId: $userId, patientId: $patientId }) {
          user {
            id
          }
        }
      }`

    return await this.$graphql.default.request(mutation, userData)
  },

  async fetchDoctors({ }, email) {
    const query = gql`
      query($email:String){
        users(input:"Doctor", email:$email) {
          edges {
            node {
              id
              username
              isActive
              email
              name
              dateOfBirth
              avatar
              groups{
                edges{
                  node{
                    id
                    name
                  }
                }
              }
              userspecializationSet {
                edges {
                  node {
                    id
                    specialization {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }`

    const variables = { email }

    return await this.$graphql.default.request(query, variables)
  },

  async fetchPatients({ }) {
    const query = gql`
      query{
        users(input:"Patient") {
          edges {
            node {
              id
              username
              isActive
              email
              name
              dateOfBirth
              avatar
               groups{
                edges{
                  node{
                    id
                    name
                  }
                }
              }
              userspecializationSet {
                edges {
                  node {
                    id
                    specialization {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }`

    return await this.$graphql.default.request(query)
  },

  async fetchGroups({ }) {
    const query = gql`
      query {
        groups{
          id
          name
        }
      }
    `
    return await this.$graphql.default.request(query)
  },

  async fetchSpecialities({ }, { langId }) {
    const query = gql`
      query($langId: Float) {
        specializations {
          id
          name
          specializationlangSet(lang_Id: $langId) {
            edges {
              node {
                id
                name
              }
            }
          }
        }
      }
    `
    const variables = { langId }
    return await this.$graphql.default.request(query, variables)
  },

  async fetchAppointmentCodes({ }, { langId }) {
    const query = gql`
      query($langId: String) {
        appointmentCode(lang: $langId){
          edges{
            node{
              id
              name
              codeType
              description
            }
          }
        }
      }
    `
    const variables = { langId }
    return await this.$graphql.default.request(query, variables)
  },

  async deleteUserSpecialization({ }, { userId }) {
    const query = gql`
     mutation($userId:ID){
      deleteUserSpecialization(user:$userId){
        deleteSpecialization {
          id
        }
      }
    }
    `
    const variables = { userId }
    return await this.$graphql.default.request(query, variables)
  },

  async createUserSpecialization({ }, { userId, specialitiesId }) {
    const query = gql`
      mutation($userId:ID, $specialitiesId:ID){
        createUserSpecialization(input:{
          user:$userId,
          specialization:$specialitiesId

        }){
          userspecialization {
            id
          }
        }
      }
    `
    const variables = { userId, specialitiesId }

    return await this.$graphql.default.request(query, variables)
  },

  async fetchUserById({ }, id) {
    const query = gql`
      query($userId: Int) {
        user(userId: $userId){
          id
          username
          firstName
          lastName
        }
      }`

    const variables = { userId: id }

    return await this.$graphql.default.request(query, variables)
  },

  async createAuthorizationPendency({ }, createData) {
    const mutation = gql`
      mutation($requestUserId: ID, $patientId: ID, $typeId: ID){
        createPendingAuthorization(createData: {requestUserId: $requestUserId, patientId: $patientId, authorizationTypeId: $typeId}) {
          pendingAuthorization{
            id
          }
        }
      }`

    return await this.$graphql.default.request(mutation, createData)
  },
}

export default {
  namespaced: true,
  getters,
  mutations,
  actions,
  state
}
