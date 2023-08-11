import { gql } from "nuxt-graphql-request";

const SET_USERS_COMPANY = "SET_USERS_COMPANY"
const REMOVE_USER_COMPANY = "REMOVE_USER_COMPANY"
const SET_CLINICS = "SET_CLINICS"
const SET_REQUESTED_DOCTORS = "SET_REQUESTED_DOCTORS"
const SET_DOCTORS = "SET_DOCTORS"
const PUSH_REQUESTED_DOCTORS = "PUSH_REQUESTED_DOCTORS"
const SET_AUTH_USER_CLINICS = "SET_AUTH_USER_CLINICS"
const SET_RELATED_CLINICS_BY_AUTH_USER = "SET_RELATED_CLINICS_BY_AUTH_USER"
const REMOVE_CLINIC = "REMOVE_CLINIC"
const SET_ACTIVE_CLINIC = "SET_ACTIVE_CLINIC"
const SET_EMPTY_CLINIC = "SET_EMPTY_CLINIC"


const isExistRequest = (requestedDoctors, userCompany) => {
  return requestedDoctors.some(item => {
    return Number(item.company.id) === Number(userCompany.company.id) &&
      Number(item.doctor.id) === Number(userCompany.user.id)
  })
}


export const state = () => ({
  usersCompany: [],
  clinics: [],
  authUserClinics: [],
  requestedDoctors: [],
  doctors: [],
});

export const getters = {
  requestedDoctors(state) {
    return state.requestedDoctors.map(item => {
      return {
        company: item.node.company,
        doctor: item.node.doctor || item.node.user,
      }
    })
  },
  doctors(state, getters) {
    let newDoctors = []
    state.doctors.forEach(item => {
      if (!isExistRequest(getters.requestedDoctors, item.node)) {
        newDoctors.push(item)
      }
    })

    newDoctors = newDoctors.map(item => {
      return item.node
    })

    return [...new Map(newDoctors.map(item =>
      [item['id'], item])).values()];
  },
  getAuthUserCompanies(state) {
    return state.authUserClinics.map(clinic => {
      return {
        id: clinic.node?.id,
        companyId: clinic.node.company?.id,
        company: clinic.node.company?.name,
        isOwner: clinic.node.isOwner,
        joinedDatetime: clinic.node.joinedDatetime,
        userId: clinic.node.user?.id,
        user: clinic.node.user?.name,
      }
    })
  },
  getUserActiveCompany(state) {
    return state.authUserClinics.find(clinic => {
      return clinic.node.isActive
    })
  },

  relatedAndOwnerCompaniesIdByAuthUser(state) {
    return state.authUserClinics.map(clinic => {
      return Number(clinic.node.company.id)
    })
  },
  getAllClinics(state, getters) {
    const newClinics = []
    state.clinics.forEach(clinic => {
      if (!getters.relatedAndOwnerCompaniesIdByAuthUser.includes(Number(clinic.node.id))) {
        newClinics.push(clinic.node)
      }
    })
    return newClinics
  },
  getOnlyAuthUserCompanies(state, getters, rootState) {
    const companies = []
    const authUser = rootState.auth.profile

    state.clinics.forEach(clinic => {
      const companyOwners = clinic.node.companyuserSet && clinic.node.companyuserSet.edges.length > 0 ? clinic.node.companyuserSet.edges : null
      if (companyOwners) {
        companyOwners.forEach(Owner => {
          if (Owner.node.user.id === authUser.id) {
            companies.push(clinic.node.id)
          }
        })
      }
    })
    return [...new Set(companies)];
  }
}

export const mutations = {
  [SET_REQUESTED_DOCTORS](state, payload) {
    state.requestedDoctors = payload
  },
  [PUSH_REQUESTED_DOCTORS](state, payload) {
    state.doctors = state.doctors.filter(doctor => {
      return Number(doctor.node.id) !== Number(payload.node.id)
    })
  },

  [SET_DOCTORS](state, payload) {
    if (payload && payload.length > 0) {
      state.doctors = state.doctors.concat(payload)
    }
  },

  [SET_EMPTY_CLINIC](state) {
    state.doctors = []
  },

  [SET_CLINICS](state, payload) {
    state.clinics = payload
  },

  [SET_USERS_COMPANY](state, payload) {
    state.usersCompany = payload
  },

  [REMOVE_USER_COMPANY](state, { userCompanyId }) {
    state.authUserClinics = state.authUserClinics.filter(item => {
      return Number(item.node.id) !== Number(userCompanyId)
    })
  },

  [REMOVE_CLINIC](state, clinicId) {
    state.clinics = state.clinics.filter(item => {
      return Number(item.node.id) !== Number(clinicId)
    })
  },

  [SET_AUTH_USER_CLINICS](state, payload) {
    state.authUserClinics = payload
  },

  [SET_ACTIVE_CLINIC](state, id) {
    state.authUserClinics = state.authUserClinics.map(clinic => {
      if (Number(id) === Number(clinic.node.id)) {
        clinic.node.isActive = true
      } else {
        clinic.node.isActive = false
      }
      return clinic
    })
  },
  [SET_RELATED_CLINICS_BY_AUTH_USER](state, payload) {
    if (payload.length > 0) {
      state.authUserClinics = state.authUserClinics.concat(payload)
    }
  },
}

export const actions = {
  async fetchDoctorLists({ }, { groupName, statusId, companyName, userName, userEmail, langId }) {
    const query = gql`
       query (
          $groupName: String
          $statusId: Float
          $companyName: String
          $userName: String
          $userEmail: String
          $langId: Float
        ) {
          userCompany(
            group_Name: $groupName
            status_Id: $statusId
            company_Name: $companyName
            user_Name: $userName
            user_Email: $userEmail
          ) {
            edges {
              node {
                id
                user {
                  id
                  firstName
                  lastName
                  name
                  email
                  phone
                  avatar
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
                doctor {
                  id
                }
                company {
                  id
                  name
                  companylangSet(lang_Id: $langId){
                    edges{
                        node{
                        name
                        }
                    }
                   }
                }
                group{
                  id,
                  name
                }
                status {
                  id
                  name
                }
              }
            }
          }
        }`

    const variables = { groupName, statusId, companyName, userName, userEmail, langId }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchSingleCompany({ }, { companyId, groupName }) {
    const query = gql`
       query ($companyId:Int, $groupName:String){
          company(companyId: $companyId) {
            id
            name
            code
            street
            street2
            state
            city
            zipcode
            country
            companyuserSet(group_Name:$groupName) {
              edges {
                node {
                  id
                  requestedBy{
                    id
                    name
                  }
                  status{
                    id
                    name
                  }
                  user {
                    id
                    username
                    isActive
                    email
                    name
                    dateOfBirth
                    avatar
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
            }
          }
        }`

    const variables = { companyId, groupName }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchRequestedDoctorListByAuthUser({ }, { userId }) {
    const query = gql`
            query ($userId: Float) {
              userCompany(user_Id: $userId) {
                edges {
                  node {
                    id
                    user {
                      id
                      firstName
                      lastName
                      name
                      email
                      phone
                      avatar
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
                    doctor {
                      id
                    }
                    status {
                      id
                      name
                    }
                    company{
                      id
                      name
                    }
                  }
                }
              }
            }`

    const variables = { userId }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchCompanies({ }, { name, langId }) {
    const query = gql`
        query ($name: String, $langId: Float) {
            companies(name: $name) {
            edges {
                node {
                id
                name
                street
                street2
                state
                city
                zipcode
                country
                isActive
                code
                companyuserSet(isOwner: true) {
                    edges {
                    node {
                        id
                        user {
                        id
                        name
                        }
                        isOwner
                    }
                    }
                }
                companylangSet(lang_Id: $langId) {
                    edges {
                    node {
                        name
                        street
                        street2
                        state
                        city
                        zipcode
                        country
                        code
                    }
                    }
                }
                }
            }
            }
        }`

    const variables = { name, langId }
    return await this.$graphql.default.request(query, variables);
  },

  async fetchAuthUserCompanies({ }, { userId, isOwner, groupName, statusId, approvalById, langId }) {
    const query = gql`
        query (
            $groupName: String
            $userId: Float
            $statusId: Float
            $isOwner: Boolean
            $approvalBy:Float
            $langId:Float
          ) {
            userCompany(
              group_Name: $groupName
              user_Id: $userId
              status_Id: $statusId
              isOwner: $isOwner
              approvalBy_Id:$approvalBy
            ) {
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
                  company {
                    id
                    name
                    companylangSet(lang_Id: $langId){
                        edges{
                            node{
                            name
                            }
                        }
                    }
                  }
                  group {
                    id
                    name
                  }
                  doctor {
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
                  requestedAt
                  joinedDatetime
                  isOwner
                  isActive
                }
              }
            }
          }
        `
    const variables = { userId, isOwner, groupName, statusId, approvalById, langId }
    return await this.$graphql.default.request(query, variables);
  },

  async fetchActiveCompanyForUser({ }, { userId, isActive, groupName, statusId }) {
    const query = gql`
        query (
            $groupName: String
            $userId: Float
            $statusId: Float
            $isActive: Boolean
          ) {
            userCompany(
              group_Name: $groupName
              user_Id: $userId
              status_Id: $statusId
              isActive: $isActive
            ) {
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
                  company {
                    id
                    name
                  }
                  group {
                    id
                    name
                  }
                  doctor {
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
                  requestedAt
                  joinedDatetime
                  isOwner
                  isActive
                }
              }
            }
          }
        `
    const variables = { userId, isActive, groupName, statusId }
    return await this.$graphql.default.request(query, variables);
  },

  async createClinic({ }, { name, street, street2, state, city, zipcode, country }) {
    const mutation = gql`
           mutation($name:String, $street:String, $street2:String, $state:String, $city:String, $zipcode:String, $country:String) {
            createCompany(input:{name:$name, street:$street, street2:$street2, state:$state, city:$city, zipcode:$zipcode, country:$country}){
                company{
                    id
                    name
                }
            }
           }
            `
    const variables = { name, street, street2, state, city, zipcode, country }
    return await this.$graphql.default.request(mutation, variables);
  },

  async createUserCompany({ }, { name, state, street, street2, city, zipcode, country, createdBy, updatedBy }) {
    const mutation = gql`
      mutation($name:String, $street:String,$street2:String,$state:String,$city:String, $zipcode:String,$country:String, $createdBy:ID,$updatedBy:ID){
        createCompany(input:{
          name:$name,
          state:$state,
          street:$street,
          street2:$street2,
          city: $city,
          zipcode: $zipcode,
          country: $country,
          createdBy:$createdBy,
          updatedBy:$updatedBy
        }){
          company{
            id
          }
        }
      }
`
    const variables = { name, state, street, street2, city, zipcode, country, createdBy, updatedBy }
    return await this.$graphql.default.request(mutation, variables)
  },

  async updateUserCompany({ }, { id, name, state, street, street2, city, zipcode, country, updatedBy }) {
    const mutation = gql`
      mutation (
        $id: ID
        $name: String
        $street: String
        $street2: String
        $state: String
        $city: String
        $zipcode: String
        $country: String
        $updatedBy: ID
      ) {
        updateCompany(
          input: {
            id: $id
            name: $name
            zipcode: $zipcode
            country: $country
            city: $city
            state: $state
            street: $street
            street2: $street2
            updatedBy: $updatedBy
          }
        ) {
          updateCompany {
            id
          }
        }
      }`

    const variables = { id, name, state, street, street2, city, zipcode, country, updatedBy }
    return await this.$graphql.default.request(mutation, variables)
  },

  async createCompanyUserForCompanyOwner({ }, {
    companyId,
    userId,
    doctorId,
    groupId,
    status,
    isOwner,
    isActive,
    joinedDatetime,
    approvalById,
    approvalAt,
    requestedBy,
  }) {
    const mutation = gql`
     mutation (
        $companyId: ID
        $userId: ID
        $doctorId: ID
        $groupId: ID
        $approvalById: ID
        $status: String
        $isOwner: Boolean
        $isActive: Boolean
        $joinedDatetime: DateTime
        $approvalAt: DateTime
        $requestedBy:ID
      ) {
        createCompanyUser(
          input: {
            company: $companyId
            user: $userId
            doctor: $doctorId
            group: $groupId
            status: $status
            isOwner: $isOwner
            isActive: $isActive
            approvalBy: $approvalById
            joinedDatetime: $joinedDatetime
            approvalAt: $approvalAt
            requestedBy:$requestedBy
          }
        ) {
          companyUser {
            id
            isOwner
            joinedDatetime
            requestedAt
            approvalAt
            isActive
          }
        }
      }
`
    const variables = { companyId, userId, doctorId, groupId, status, isOwner, isActive, joinedDatetime, approvalById, approvalAt, requestedBy }

    return await this.$graphql.default.request(mutation, variables)
  },

  async createDoctorTypeUserForCompany({ }, { companyId, userId, groupId, status, isOwner, isActive, requestedBy, joinedDatetime, requestType }) {
    const mutation = gql`
      mutation (
        $companyId: ID
        $userId: ID
        $groupId: ID
        $status: String
        $isOwner: Boolean
        $isActive: Boolean
        $requestedBy: ID
        $joinedDatetime: DateTime
        $requestType: String
      ) {
        createCompanyUser(
          input: {
            company: $companyId
            user: $userId
            group: $groupId
            status: $status
            isOwner: $isOwner
            isActive: $isActive
            requestedBy: $requestedBy
            joinedDatetime: $joinedDatetime
            requestType: $requestType
          }
        ) {
          companyUser {
            id
            isOwner
            joinedDatetime
            requestedAt
            approvalAt
            isActive
          }
        }
      }`

    const variables = { companyId, userId, groupId, status, isOwner, isActive, requestedBy, joinedDatetime, requestType }

    return await this.$graphql.default.request(mutation, variables)
  },

  async createPatientTypeUserForCompany({ }, { companyId, userId, doctorId, groupId, status, isOwner, isActive, requestedBy, requestType }) {
    const mutation = gql`
      mutation (
        $companyId: ID
        $userId: ID
        $doctorId: ID
        $groupId: ID
        $status: String
        $isOwner: Boolean
        $isActive: Boolean
        $requestedBy: ID
        $requestType: String
      ) {
        createCompanyUser(
          input: {
            company: $companyId
            user: $userId
            doctor: $doctorId
            group: $groupId
            status: $status
            isOwner: $isOwner
            isActive: $isActive
            requestedBy: $requestedBy
            requestType: $requestType
          }
        ) {
          companyUser {
            id
            isOwner
            joinedDatetime
            requestedAt
            approvalAt
            isActive
          }
        }
      }`

    const variables = { companyId, userId, doctorId, groupId, status, isOwner, isActive, requestedBy, requestType }

    return await this.$graphql.default.request(mutation, variables)
  },

  async deleteUserCompany({ }, { userCompanyId }) {
    const mutation = gql`
          mutation($userCompanyId:ID){
            deleteCompanyUser(input:$userCompanyId){
              companyuser {
                id
              }
            }
          }
`
    const variables = { userCompanyId }
    return await this.$graphql.default.request(mutation, variables)
  },
  async deleteCompanyUser({ }, { companyUserId }) {
    const mutation = gql`
          mutation($companyUserId:ID){
            deleteCompanyUser(input:$companyUserId){
              companyuser{
                id
              }
            }
          }`

    const variables = { companyUserId }

    return await this.$graphql.default.request(mutation, variables)
  },

  async setActiveClinic({ }, { companyUserId, isActive, status }) {
    const mutation = gql`
         mutation ($companyUserId: ID, $isActive: Boolean, $status: String) {
          updateCompanyUser(
            input: { id: $companyUserId, isActive: $isActive, status: $status }
          ) {
            companyuserUpdate {
              id
              isActive
            }
          }
        }`

    const variables = { companyUserId, isActive, status }

    return await this.$graphql.default.request(mutation, variables)
  },

  async fetchAllPatientsByCompanyDoctor({ }, { companyId, doctorId, groupName, statusId }) {
    const mutation = gql`
         query (
            $companyId: Float
            $doctorId: Float
            $groupName: String
            $statusId: Float
          ) {
            userCompany(
              company_Id: $companyId
              doctor_Id: $doctorId
              group_Name: $groupName
              status_Id: $statusId
            ) {
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
                  company {
                    id
                    name
                  }
                  group {
                    id
                    name
                  }
                  doctor {
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
                  requestedAt
                  joinedDatetime
                  isOwner
                  isActive
                }
              }
            }
          }`

    const variables = { companyId, doctorId, groupName, statusId }

    return await this.$graphql.default.request(mutation, variables)
  },


}
