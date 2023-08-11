import { gql } from "nuxt-graphql-request";


export const state = () => ({
  clinics: [
    {
      id: 1,
      phone: "(123) 456 789",
      image:
        "https://my.clevelandclinic.org/-/scassets/images/org/promo-panels/health-essentials-podcast-promo.jpg?h=560&la=en&w=620&hash=58C2A33B152A18D43B52802EF13A04E539197C85",
      clinicName: "Hanna Gover",
      ownerName: "Owner Name",
      address: " 2289 5th Ave, Suite 600 San Francisco New York, NY, 10037 ",
    },
    {
      id: 2,
      phone: "(234) 456 789",
      image:
        "https://www.myhealth.ph/wp-content/uploads/2019/08/alabang-1.jpg",
      clinicName: "Daniel Kristeen",
      ownerName: "Owner Name",
      address: " 55 E 11th St #1OTH, Suite 600 New York, NY, 10003 ",
    },
  ]
});

export const getters = {
  getAllClinics(state) {
    return state.clinics
  }
}

export const mutations = {

}

export const actions = {
  async sendAccessRequest({ }, { clinicId }) {
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
    const variables = { clinicId }

    return await this.$graphql.default.request(query, variables);
  },

  async createCompanyPatientTypeUser({ }, { userId, companyId, isOwner, isDefault }) {
    const mutation = gql`    
      mutation($companyId:ID, $userId:ID, $doctorId:ID, $groupId:ID,$approvalById:ID,$status:String, $isOwner:Boolean,$isActive:Boolean) {
        createCompanyUser(input: {
          company:$companyId,
          user:$userId, 
          doctor:$doctorId,
          group:$groupId,
          status: $status,
          isOwner:$isOwner,
          isActive:$isActive,
          approvalBy:$approvalById
        }) {
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
    const variables = { userId, companyId, isOwner, isDefault }
    return await this.$graphql.default.request(mutation, variables)
  },

}
