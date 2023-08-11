import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { ClientError } from 'graphql-request'

import { useAuthStore } from 'src/stores/auth'

export function useAuth() {
  const router = useRouter()
  const toast = useToast()
  const authStore = useAuthStore()

  const step = ref('login')
  const loading = ref(false)

  const formInitialState = {
    username: '',
    email: '',
    password: '',
    birthdate: '',
    address: '',
    country: null,
    nationality: null,
    languageCode: null,
    isCaregiver: false
  }
  const form = reactive({ ...formInitialState })

  const resetForm = () => Object.assign(form, formInitialState)


  const signIn = async (username: string, password: string) => {
    loading.value = true
    try {
      const { tokenAuth } = await authStore.signIn(username, password)

      authStore.setToken(tokenAuth?.token)
      const { viewer } = await authStore.loadUser(tokenAuth?.token)
      const { userCompany } = await authStore.userActiveCompany(viewer?.id, true)
      const company = userCompany?.edges[0]?.node?.company
      authStore.setActiveCompany({company})
      const user = Object.assign({}, viewer, { company })
      authStore.setUser(user)
      // console.log(user.value, "userActiveCompany")

      toast.success('Successfully Logged In!')
      await router.push('/admin')
      resetForm()
    } catch (error: unknown) {
      handleError(error)
    } finally {
      loading.value = false
    }
  }

  const signOut = async () => {
    try {
      await authStore.invalidateToken()

      authStore.removeToken()
      router.push('/')
      toast.success('Successfully Logged Out!')
    } catch (error: unknown) {
      console.log(error);

      handleError(error)
    }
  }

  const handleError = (error: unknown) => {
    if (process.env.DEV) {
      console.error(JSON.stringify(error, undefined, 2))
    }
    if (error instanceof ClientError) {
      error.response.errors?.forEach(e => toast.error(e.message))
    } else {
      toast.error('Something went wrong, please try again later')
    }
  }

  return {
    step,
    form,
    resetForm,
    signIn,
    signOut,
    loading: computed(() => loading.value),
  }
}
