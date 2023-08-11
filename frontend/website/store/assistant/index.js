import { getField, updateField } from "vuex-map-fields";
import { gql } from "nuxt-graphql-request";

export const state = () => ({});

export const getters = {
  getField
};

export const mutations = {
  updateField
};

export const actions = {
  async sendEmailInvitation({}, email) {
    const mutation = gql`
      mutation($email: String) {
        sendEmailInvitation(email: $email) {
          response
        }
      }
    `;

    const variables = { email };

    return await this.$graphql.default.request(mutation, variables);
  },

  async fetchAssistantsByCompanyId({}, { companyId, first, offset, name }) {
    const query = gql`
      query($companyId: Float, $first: Int, $offset: Int, $name: String) {
        allAssistants(
          company_Id: $companyId
          first: $first
          offset: $offset
          name_Icontains: $name
        ) {
          totalCount
          pageInfo {
            hasNextPage
            hasPreviousPage
          }
          edges {
            node {
              id
              name
              user {
                id
                dateJoined
              }
            }
          }
        }
      }
    `;

    const variables = { companyId, first, offset, name };

    return await this.$graphql.default.request(query, variables);
  }
};
