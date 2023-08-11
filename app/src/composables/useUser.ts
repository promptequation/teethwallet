import { useToast } from 'vue-toastification'
import { ClientError } from 'graphql-request'

import { useUserStore } from 'src/stores/user'
import { CompanyUser } from 'src/types/user'

export function useUser() {
  const toast = useToast()
  const userStore = useUserStore()

  const getUserById = async (userId: number) => {
    try {
      const { user } = await userStore.getUserById(userId)
      console.log(user);

      userStore.setUser(user)
    } catch (error: unknown) {
      handleError(error)
    }
  }

  const createAuthorizationPendency = async (companyUser: CompanyUser) => {
    try {
      const { createCompanyUser } = await userStore.createAuthorizationPendency(companyUser)
      console.log(createCompanyUser);

    } catch (error: unknown) {
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
    getUserById,
    createAuthorizationPendency,
  }
}
