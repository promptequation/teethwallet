import { boot } from 'quasar/wrappers'
import { GraphQLClient } from 'graphql-request'
const endpoint = 'https://api.teethwallet.com/graphql'
const graphQLClient = new GraphQLClient(endpoint)

export default boot(({ app }) => {
  app.config.globalProperties.$graphql = graphQLClient
})

export { graphQLClient }
