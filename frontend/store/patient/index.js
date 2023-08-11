
import { getField, updateField } from 'vuex-map-fields'
import { gql } from 'graphql-request'

export const state = () => ({

})

export const getters = {
  getField
}

export const mutations = {
  updateField
}

export const actions = {

  async fetchPatientById ({}, id) {
    const query = gql`
      query($patientId: Int) {
        patient(patientId: $patientId){
        id
        name
        allergies
        }
      }`

     const variables = { patientId: id }

    return await this.$graphql.default.request(query, variables)
  },
}

export default {
  namespaced: true,
  getters,
  mutations,
  actions,
  state
}