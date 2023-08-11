import { gql } from "nuxt-graphql-request";

const SET_PATIENT_INVITATIONS = "SET_PATIENT_INVITATIONS"
const REMOVE_PATIENT = "REMOVE_PATIENT"
const SET_DOCTOR_INVITATIONS = "SET_DOCTOR_INVITATIONS"
const SET_DOCTOR_INVITATIONS_EMPTY = "SET_DOCTOR_INVITATIONS_EMPTY"
const REMOVE_DOCTOR_INVITATION = "REMOVE_DOCTOR_INVITATION"
const SET_CLINIC_INVITATIONS = "SET_CLINIC_INVITATIONS"
const REMOVE_CLINIC_INVITATION = "REMOVE_CLINIC_INVITATION"

export const state = () => ({
  patientsInvitations: [],
  doctorInvitations: [],
  clinicInvitations: [],
});

export const getters = {
  getAllPatientsInvitations(state) {
    return state.patientsInvitations.map(item => {
      return {
        id: item.node?.id,
        company_id: item.node.company?.id,
        company: item.node.company?.name,
        requestedBy: item.node.requestedBy?.name,
        requestedById: item.node.requestedBy?.id,
        name: item.node.user?.name,
        email: item.node.user?.email,
        phone: item.node.user?.phone,
        requestedAt: item.node.requestedAt,
      }
    })
  },
  getAllDoctorInvitations(state, getters, rootState) {
    const authUser = rootState.auth.profile
    let invitations = state.doctorInvitations.filter(item => {
      if (item.node.status.name == 'Pending' && item.node.requestedBy?.id !== authUser.id) {
        return item
      }
    })

    invitations = invitations.map(item => {
      return {
        id: item.node.id,
        company_id: item.node.company?.id,
        company: item.node.company?.name,
        requestedBy: item.node.requestedBy?.name,
        requestedById: item.node.requestedBy?.id,
        name: item.node.user?.name,
        email: item.node.user?.email,
        phone: item.node.user?.phone,
        requestedAt: item.node.requestedAt,
      }
    })

    return [...new Map(invitations.map(item =>
      [item['id'], item])).values()];

  },
  getClinicInvitations(state, getters, rootState) {
    const authUser = rootState.auth.profile

    let newInvitations = state.clinicInvitations.map(item => {
      return {
        id: item.node?.id,
        company_id: item.node.company?.id,
        company: item.node.company?.name,
        requestedBy: item.node.requestedBy?.name,
        requestedById: item.node.requestedBy?.id,
      }
    })

    newInvitations = newInvitations.filter(item => {
      if (item.requestedById !== authUser.id) {
        return item
      }
    })

    return [...new Map(newInvitations.map(item => [item['id'], item])).values()]
  }
}

export const mutations = {
  [SET_PATIENT_INVITATIONS](state, payload) {
    state.patientsInvitations = payload
  },
  [REMOVE_PATIENT](state, { id }) {
    state.patientsInvitations = state.patientsInvitations.filter(item => {
      return Number(item.node.id) !== id
    })
  },

  [SET_DOCTOR_INVITATIONS](state, payload) {
    if (payload && payload.length > 0) {
      state.doctorInvitations = state.doctorInvitations.concat(payload)
    }
  },

  [SET_DOCTOR_INVITATIONS_EMPTY](state) {
    state.doctorInvitations = []
  },

  [REMOVE_DOCTOR_INVITATION](state, { id }) {
    state.doctorInvitations = state.doctorInvitations.filter(item => {
      return Number(item.node.id) !== id
    })
  },
  [SET_CLINIC_INVITATIONS](state, payload) {
    if (payload && payload.length > 0) {
      state.clinicInvitations = state.clinicInvitations.concat(payload)
    }
  },
  [REMOVE_CLINIC_INVITATION](state, { id }) {
    state.clinicInvitations = state.clinicInvitations.filter(item => {
      return Number(item.node.id) !== id
    })
  },
}

export const actions = {
  async fetchUserLookup({ }) {
    const query = gql`
        query{
          approvalStatuses{
            id
            name
          }
        }
        `
    return await this.$graphql.default.request(query);
  },

  async fetchPatientInvitations({ }, { companyId, groupName, doctorId, statusId, userId }) {
    const query = gql`
        query (
          $companyId: Float
          $groupName: String
          $doctorId: Float
          $statusId: Float
          $userId: Float
        ) {
          userCompany(
            company_Id: $companyId
            group_Name: $groupName
            doctor_Id: $doctorId
            status_Id: $statusId
            user_Id: $userId
          ) {
            edges {
              node {
                id
                user {
                  id
                  name
                  username
                  isActive
                  email
                  phone
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
                  userspecializationSet{
                    edges{
                      node{
                        id
                        specialization{
                          id
                          name
                        }
                      }
                    }
                  }
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
                requestedBy {
                  id
                  email
                  name
                }
              }
            }
          }
        }`

    const variables = { companyId, groupName, doctorId, statusId, userId }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchDoctorInvitations({ }, { companyId, groupName, statusId }) {
    const query = gql`
        query (
          $companyId: Float
          $groupName: String
          $statusId: Float
        ) {
          userCompany(
            company_Id: $companyId
            group_Name: $groupName
            status_Id: $statusId
          ) {
            edges {
              node {
                id
                user {
                  id
                  name
                  username
                  isActive
                  email
                  phone
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
                  userspecializationSet{
                    edges{
                      node{
                        id
                        specialization{
                          id
                          name
                        }
                      }
                    }
                  }
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
                requestedBy {
                  id
                  email
                  name
                }
              }
            }
          }
        }`

    const variables = { companyId, groupName, statusId }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchClinicInvitations({ }, { userId, groupName, statusId, isOwner }) {
    const query = gql`
        query (
          $userId: Float
          $groupName: String
          $statusId: Float
          $isOwner: Boolean
        ) {
          userCompany(
            user_Id: $userId
            group_Name: $groupName
            status_Id: $statusId
            isOwner: $isOwner
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
                requestedBy{
                  id
                  email
                  name
                }
              }
            }
          }
        }
        `
    const variables = { userId, groupName, statusId, isOwner }

    return await this.$graphql.default.request(query, variables);
  },

  async acceptPatientInvitation({ }, { id, doctorId, approvalById, status, joinedDatetime, approvalAt, requestType }) {
    const query = gql`
        mutation($id:ID, $doctorId:ID, $approvalById:ID, $status:String, $joinedDatetime:DateTime, $approvalAt:DateTime,$requestType: String) {
          updateCompanyUser(input: {
            id:$id,
            doctor:$doctorId,
            status: $status,
            joinedDatetime:$joinedDatetime,
            approvalBy:$approvalById,
            approvalAt:$approvalAt
            requestType: $requestType
          }) {
            companyuserUpdate{
              id
              joinedDatetime
              approvalAt
               doctor{
                id
                email
              }
              status{
                id
                name
              }
            }
          }
        }
        `
    const variables = { id, doctorId, approvalById, status, joinedDatetime, approvalAt, requestType }

    return await this.$graphql.default.request(query, variables);
  },

  async rejectPatientInvitation({ }, { id, doctorId, approvalById, status, approvalAt, requestType }) {
    const query = gql`
        mutation(
            $id: ID
            $doctorId: ID
            $approvalById: ID
            $status: String
            $approvalAt: DateTime
            $requestType: String
        ) {
            updateCompanyUser(
                input: {
                    id: $id
                    doctor: $doctorId
                    status: $status
                    approvalBy: $approvalById
                    approvalAt: $approvalAt
                    requestType: $requestType
                }
            ) {
                companyuserUpdate {
                    id
                    joinedDatetime
                    approvalAt
                    doctor {
                        id
                        email
                    }
                    group {
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
                }
            }
        }
    `;
    const variables = { id, doctorId, approvalById, status, approvalAt, requestType }

    return await this.$graphql.default.request(query, variables);
  },

  async acceptDoctorInvitation({ }, { doctorInvitationId }) {
    const query = gql`
        query ($userId:ID,$isOwner:Boolean){
          userCompany(userId: $userId, isOwner:$isOwner) {
            edges {
              node {
                id
                company {
                  id
                  name
                }
                user {
                  id
                  name
                }
                isOwner
                isDefault
                joinedDate
              }
            }
          }
        }
        `
    const variables = { patientId }

    return await this.$graphql.default.request(query, variables);
  },

  async rejectDoctorInvitation({ }, { doctorInvitationId }) {
    const query = gql`
        query ($userId:ID,$isOwner:Boolean){
          userCompany(userId: $userId, isOwner:$isOwner) {
            edges {
              node {
                id
                company {
                  id
                  name
                }
                user {
                  id
                  name
                }
                isOwner
                isDefault
                joinedDate
              }
            }
          }
        }
        `
    const variables = { patientId }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchDoctorsByPatient({ }, { userId, groupName, statusId }) {
    const query = gql`
       query (
          $groupName: String
          $statusId: Float
          $userId: Float
        ) {
          userCompany(
            group_Name: $groupName
            status_Id: $statusId
            user_Id: $userId
          ) {
            edges {
              node {
                user {
                  id
                  name
                }
                doctor {
                  id
                  name
                  username
                  isActive
                  email
                  phone
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
        `
    const variables = { userId, groupName, statusId }

    return await this.$graphql.default.request(query, variables);
  },
  async fetchPatienstByDoctor({ }, { companyId, groupName, doctorId, statusName, statusId }) {
    const query = gql`
        query (
          $companyId: Float
          $groupName: String
          $doctorId: Float
          $statusName: String
          $statusId: Float
        ) {
          userCompany(
            company_Id: $companyId
            group_Name: $groupName
            doctor_Id: $doctorId
            status_Name: $statusName
            status_Id: $statusId
          ) {
            edges {
              node {
                id
                user {
                  id
                  name
                  username
                  isActive
                  email
                  phone
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
                  userspecializationSet{
                    edges{
                      node{
                        id
                        specialization{
                          id
                          name
                        }
                      }
                    }
                  }
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
                requestedBy {
                  id
                  email
                  name
                }
              }
            }
          }
        }`;

    const variables = { companyId, groupName, doctorId, statusName, statusId };

    return await this.$graphql.default.request(query, variables);
  },
}
