import { defineStore } from 'pinia'
import { gql } from 'graphql-request'

import { graphQLClient } from 'src/boot/graphql'
import { User } from 'src/types/user'
import { cookie } from 'src/boot/cookie'

interface State {
  token: string | null
  user: User | null
  activeCompany: number | null
}

export const useAuthStore = defineStore('auth', {
  state: (): State => ({
    token: null,
    user: null,
    activeCompany: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isDoctor: (state) => state.user?.groups?.edges?.some(group => group.node?.name === 'Doctor') || false,
    getActiveCompany: (state) => state.activeCompany
  },
  actions: {
    // set auth token
    setToken(token: string) {
      this.token = token
      cookie.set('JWT', token)
      graphQLClient.setHeader('Authorization', `JWT ${token}`)
    },
    // set activeCompany
    setActiveCompany(activeCompany: any) {
      this.activeCompany = activeCompany
    },
    // set user
    setUser(user: User) {
      this.user = user
    },
    // delete token
    removeToken() {
      this.token = null
      cookie.removeAll()
      graphQLClient.setHeader('Authorization', 'null')
    },
    // sign in
    async signIn(username: string, password: string) {
      const mutation = gql`
        mutation ($username: String!, $password: String!) {
          tokenAuth(username: $username, password: $password) {
            payload
            token
          }
        }
      `
      const variables = { username, password }

      return await graphQLClient.request(mutation, variables)
    },
    // load auth user
    async loadUser(token: string) {
      const query = gql`
        query ($token: String!) {
          viewer(token: $token) {
            id
            name
            email
            username
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
      const variables = { token }

      return await graphQLClient.request(query, variables)
    },
    // load auth user active company
    async userActiveCompany(userId: number, isActive: boolean) {
      const query = gql`
        query ($userId: Float, $isActive: Boolean) {
          userCompany(user_Id: $userId, isActive: $isActive, first: 1) {
            edges {
              node {
                company {
                  id
                  name
                }
              }
            }
          }
        }
      `
      const variables = { userId, isActive }

      return await graphQLClient.request(query, variables)
    },
    // invalid token in API
    async invalidateToken(): Promise<boolean> {
      const mutation = gql`
        mutation{
          deleteTokenCookie{
            deleted
          }
        }`

      const response = await graphQLClient.request(mutation)

      return response.deleteTokenCookie?.deleted
    },
  },
});
