// TODO move queries / mutations to separated file
// TODO create models to handle complex executions

import { getField, updateField } from 'vuex-map-fields'
import { gql } from 'graphql-request'
import { SET_USER_PROFILE, LOGOUT_USER, SET_JWT_TOKEN, SET_NEW_LANG } from './types'

export const state = () => ({
  profile: {
    id: "",
    firstName: "",
    lastName: "",
    username: '',
    email: '',
    avatar: '',
    street: '',
    street2: '',
    city: '',
    country: '',
    lang: '',
    isDentist: false,
    speciality: [],
    groups: {
      edges: []
    },
    userspecializationSet: {
      edges: []
    },
    dateOfBirth: '',
    patientsManaged: [],
    accessSurvey: false,
  },
  selectedProfile: {},
  token: null,
  currentLang: 'en'
})

export const getters = {
  getField,
  hasToken(state) { return !!state.token },
  getUserProfile(state) { return state.profile },
  getSelectedProfile(state) { return state.selectedProfile },
}

export const mutations = {
  updateField,
  SET_USER_PROFILE(state, payload) {
    let doctor = false
    payload.groups?.edges.forEach(item => {
      if (item.node.name === 'Doctor') {
        return doctor = true
      }
    })
    payload.isDentist = doctor

    if (payload.userspecializationSet?.edges?.length > 0) {
      const ids = payload.userspecializationSet.edges.map(item => {
        return item.node.specialization.id
      })
      payload.speciality = [...new Set(ids)];
    } else {
      payload.speciality = []
    }
    payload.patientsManaged = []
    if (payload.userlangSet && payload.userlangSet.edges?.length > 0) {
        payload.firstName = payload.userlangSet.edges[0]?.node?.firstName
        payload.lastName = payload.userlangSet.edges[0]?.node?.lastName
        payload.name = payload.userlangSet.edges[0]?.node?.name
        payload.phone = payload.userlangSet.edges[0]?.node?.phone
        payload.state = payload.userlangSet.edges[0]?.node?.state
        payload.street = payload.userlangSet.edges[0]?.node?.street
        payload.street2 = payload.userlangSet.edges[0]?.node?.street2
        payload.zip = payload.userlangSet.edges[0]?.node?.zip
        payload.city = payload.userlangSet.edges[0]?.node?.city
    }
    state.profile = payload
    state.currentLang = payload.lang?.code || 'en'
  },
  SET_SELECTED_PROFILE(state, payload) {
    //console.log('payload=====',payload)  // logging out
    //console.log('state=====',state)      //
    state.selectedProfile = payload
  },
  SET_JWT_TOKEN(state, token) {
    state.token = token
    // console.log('token=====',token)  // entering profile
    this.$cookies.set('JWT', token)
    this.$graphql.default.setHeader('Authorization', `JWT ${token}`)
  },
  LOGOUT_USER(state) {
    state.profile = {}
    state.token = null
    this.$cookies.removeAll()
    this.$cookies.set('i18n_redirected', 'pt')
    this.$graphql.default.setHeader('Authorization', null)
  },
  SET_NEW_LANG(state, payload){
    state.currentLang = payload
  }
}

export const actions = {

  async signUp({ }, userData) {
    const mutation = gql`
        mutation ($firstName: String!, $lastName:String, $username:String, $email: String!, $password: String!, $birthdate: Date!, $address: String!, $addressTwo: String, $country: String!, $nationality: Int!, $language: ID, $isCaregiver: Boolean!) {
          createUser(input: {
            firstName: $firstName,
            lastName:$lastName,
            username:$username
            email: $email,
            password: $password,
            dateOfBirth: $birthdate,
            street: $address,
            street2: $addressTwo,
            country: $country,
            nationality: $nationality,
            lang: $language,
            isCaregiver: $isCaregiver
          }) {
            user {
              id
              email
              username
              lang{
                id
                name
                code
              }
            }
          }
        }
`

    const variables = { ...userData }

    return await this.$graphql.default.request(mutation, variables)
  },

  async signIn({ }, userData) {
    const mutation = gql`
      mutation ($username: String!,$password: String!) {
        tokenAuth(username: $username, password: $password) {
            payload
            token
            user{
              isFirstLogin
          }
        }
      }`

    const variables = { ...userData }
    return await this.$graphql.default.request(mutation, variables)
  },

  async updateADProfile({ state }) {
    console.log('updateADProfile ==== is launched')
    /*const mutation = gql`
      mutation ($id: ID, Sheart: String) {
        updatePatient(patientData: {id: $id, adHeart: $heart}) {
          patient {
            id
            adHeart
          }
        }
      }
`*/
    const mutation = gql`
      mutation ($heart: String, $kidney:String, $diabet:String, $hyper:String, $blood:String, $liver:String, $stomach:String, $smoker:String, $radio:String, $drug:String) {
        updatePatient(id:1, patientData: {adHeart: $heart, adKidney: $kidney, adDiabet: $diabet, adHyper: $hyper, adBlood: $blood, adLiver: $liver, adStomach: $stomach, adSmoker: $smoker, adRadio: $radio, adDrugAl: $drug} ) {
          patient {
            id
            adHeart
            adKidney
            adDiabet
            adHyper
            adBlood
            adLiver
            adStomach
            adSmoker
            adRadio
            adDrugAl
          }
        }
      }
`
    let variables = Object.assign(state.profile)
    variables.id = variables.id.replace('UserType:', '')

    return await this.$graphql.default.request(mutation, variables)
  },
  /*

  mutation {
  updatePatient(
    id: 2,
    patientData: {
     name: "Mania",
      birthDate: "1999-04-01"
    }
  ){
    patient {
      id
      name
      birthDate
      allergies
      adHeart
      adSmoker
    }
  }
}

  */




  async updateUserProfile({ state }) {
    const mutation = gql`
       mutation (
        $id: ID
        $firstName: String
        $lastName: String
        $username: String
        $email: String
        $phone: String
        $gender: String
        $street: String
        $street2: String
        $city: String
        $zip: String
        $country: String
        $avatar: String
        $nationality: Int
        $dateOfBirth: Date
        $lang: ID
        $isCaregiver: Boolean
        $accessSurvey:Boolean
      ) {
        updateUser(
          input: {
            id: $id
            firstName: $firstName
            lastName: $lastName
            username: $username
            email: $email
            phone: $phone
            gender: $gender
            street: $street
            street2: $street2
            city: $city
            zip: $zip
            country: $country
            avatar: $avatar
            nationality: $nationality
            dateOfBirth: $dateOfBirth
            lang: $lang
            isCaregiver: $isCaregiver
            accessSurvey: $accessSurvey
          }
        ) {
          user {
            id
          }
        }
      }
`
    let variables = JSON.parse(JSON.stringify(Object.assign(state.profile)))
    typeof variables.lang === 'object' ? variables.lang = variables.lang.id : variables.lang = variables.lang
    variables.id = variables.id.replace('UserType:', '')
    return await this.$graphql.default.request(mutation, variables)
  },


  async fetchUserProfile({ state }) {
    const patientFragment = `
          id
          name
          __typename
          currentDoctor{
            id
            name
            doctorUser{ edges{ node{
              avatar
              id
            }}}
            __typename
          }
          previousDoctors{
            id
            name
            doctorUser{ edges{ node{
              avatar
              id
            }}}
            __typename
          }`

    const query = gql`
     query ($token: String!, $langId:Float) {
        viewer(token: $token) {
          username
          id
          firstName
          lastName
          email
          street
          street2
          city
          country
          avatar
          accessSurvey
          userlangSet(lang_Id: $langId) {
            edges {
              node {
                firstName
                lastName
                name
                gender
                phone
                street
                street2
                state
                city
                zip
              }
            }
          }
          lang{
            id
            name
            code
          }
          dateOfBirth
          groups {
            edges {
              node {
                id
                name
              }
            }
          }
          userspecializationSet {
            edges {
              node {
                specialization {
                  id
                  name
                }
              }
            }
          }
        }
        approvalStatuses {
          id
          name
        }
      }
  `

    const variables = {
        token: state.token,
        langId: state.profile?.lang?.id,
    }

    return await this.$graphql.default.request(query, variables)
  },


  async fetchSpecialitiesByAuthUser({ }, { userId }) {
    const query = gql`
       query($userId:Float){
        userSpecializations(user_Id:$userId) {
              edges {
            node {
              id
            }
          }
        }
      }
    `
    const variables = { userId }
    return await this.$graphql.default.request(query, variables)
  },


  async verifyToken({ }, token) {
    const query = gql`
      mutation($token: String){
        verifyToken(token: $token) {
          payload
        }
      }`

    const variables = { token }

    const response = await this.$graphql.default.request(query, variables)
    if (response.verifyToken?.payload) {
      return true
    }
    return false
  },

  async invalidateToken() {
    const mutation = gql`
      mutation{
        deleteTokenCookie{
          deleted
        }
      }`

    const response = await this.$graphql.default.request(mutation)

    return response.deleteTokenCookie?.deleted
  },

  async updateUserGroup({ }, { userId, group }) {
    const mutation = gql`
      mutation($userId:ID,$group:String){
        updateUserGroup(input:{
          id:$userId,
          group:$group
        }){
          user{
            id
            username
            name
            firstName
            groups {
              edges {
                node {
                  id
                  name
                }
              }
            }
          }
        }
      }
    `
    const variables = { userId, group }
    return await this.$graphql.default.request(mutation, variables)
  },
  async emailVerify({ }, { token, uuid }) {
    const mutation = gql`
      mutation ($uuid: String, $token: String) {
        emailVerification(input: { uuid: $uuid, emailToken: $token }) {
          user {
            id
            username
          }
        }
      }
    `
    const variables = { token, uuid }
    return await this.$graphql.default.request(mutation, variables)
  },

  async logout({ commit, dispatch }) {
    await dispatch('invalidateToken')
    await commit(LOGOUT_USER)
  },

  async setUserProfile({ commit, dispatch }, token) {
    commit(SET_JWT_TOKEN, token)
    const { viewer, approvalStatuses } = await dispatch('fetchUserProfile')
    commit(SET_USER_PROFILE, viewer)
    commit('common/SET_APPROVAL_STATUS', approvalStatuses, { root: true })
  },

  async reFatchUserprofile({ commit, dispatch }) {
    const { viewer } = await dispatch('fetchUserProfile')
    commit(SET_USER_PROFILE, viewer)
  }
}

export default {
  namespaced: true,
  getters,
  mutations,
  actions,
  state
}
