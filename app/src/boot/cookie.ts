import { boot } from 'quasar/wrappers'
import Cookie from 'cookie-universal'

const cookie = Cookie()

export default boot(({ app }) => {
  app.config.globalProperties.$cookies = cookie
})

export { cookie }
