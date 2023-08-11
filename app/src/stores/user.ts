import { defineStore } from 'pinia'
import { gql } from 'graphql-request'

import { graphQLClient } from 'src/boot/graphql'
import { User, CompanyUser } from 'src/types/user'

interface State {
  user: User | null
}

export const useUserStore = defineStore('user', {
  state: (): State => ({
    user: null,
  }),
  actions: {
    // set user
    setUser(user: User) {
      this.user = user
    },
    // load user
    async getUserById(userId: number) {
      const query = gql`
        query ($userId: Int) {
          user(userId: $userId) {
            id
            name
            email
            avatar
            dateOfBirth
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
      `
      const variables = { userId }

      return await graphQLClient.request(query, variables)
    },

    // request patient for authorization
    async createAuthorizationPendency(variables: CompanyUser) {
      // console.log(JSON.stringify(variables));
      const mutation = gql`
        mutation ($companyId: ID, $userId: ID, $doctorId: ID, $groupId: ID, $status: String, $isOwner: Boolean, $isActive: Boolean, $requestedById: ID, $approvalById: ID, $joinedDatetime: DateTime, $approvalAt: DateTime) {
          createCompanyUser(input: {company: $companyId, user: $userId, doctor: $doctorId, group: $groupId, status: $status, isOwner: $isOwner, isActive: $isActive, requestedBy: $requestedById, approvalBy: $approvalById, approvalAt: $approvalAt, joinedDatetime: $joinedDatetime}) {
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

      return await graphQLClient.request(mutation, variables)
    },

  },
});
