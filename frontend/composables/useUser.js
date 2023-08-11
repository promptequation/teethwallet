import { useStore, watchEffect, computed, useContext } from '@nuxtjs/composition-api'
import useNuxtTranslator from "~/../composables/useNuxti18n";
import { provideToast, useToast } from 'vue-toastification/composition'
import { SET_SELECTED_PROFILE } from '@common-store/auth/types'
const useUser = () => {
  const { $t } = useNuxtTranslator()
  provideToast({
    timeout: 4000, position: 'bottom-center'
  })

  const toast = useToast()
  const { dispatch, commit, getters, state } = useStore()
  const { $dayjs } = useContext();

  const userProfile = getters['auth/getUserProfile']
  const selectedProfile = computed(() => state.auth.profile)

  const isDoctor = computed(() => {
    let doctor = false
    selectedProfile.value.groups?.edges.forEach(item => {
      if (item.node.name === 'Doctor') {
        return doctor = true
      }
    })
    return doctor
  })

  const isSwitchToDoctor = computed(() => {
    let isSwitch = false
    if (selectedProfile.value.dateOfBirth) {
      const dateOfBirth = new Date(selectedProfile.value.dateOfBirth)
      const currentDate = new Date()

      const date1 = $dayjs(currentDate)
      const date2 = $dayjs(dateOfBirth)
      const year = date1.diff(date2, 'y')

      isSwitch = year > 22 ? true : false
    } else {
      isSwitch = false
    }
    return isSwitch
  })

  const updateUserProfile = async () => {
    try {
      await dispatch('auth/updateUserProfile')
      toast.success(`${$t('toastMessage.Updated Successfully!')}`)
    } catch (error) {
      toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
    }
  }

  const updateADProfile = async () => {
    try {
      await dispatch('auth/updateADProfile')
      toast.success(`${$t('toastMessage.Updated Successfully!')}`)
    } catch (error) {
      toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
    }
  }

  const profileOptions = computed(() => {
    const options = []
    if (userProfile.doctor) {
      options.push(userProfile.doctor)
    }
    if (userProfile.patient) {
      options.push(userProfile.patient)
      userProfile.patientsManaged.forEach(patient => options.push({ managed: true, ...patient }))
    }
    return options
  })

  const fetchDoctors = async (search) => {
    try {
      const { users } = await dispatch('user/fetchDoctors', search)
      commit('user/SET_DOCTORS', getUsers(users && users.edges))
    } catch (error) {
      console.log(error);
    }
  }

  const fetchPatients = async () => {
    try {
      const { users } = await dispatch('user/fetchPatients')
      commit('user/SET_PATIENTS', getUsers(users && users.edges))
    } catch (error) {
      console.log(error);
    }
  }

  const fetchGroups = async () => {
    try {
      const { groups } = await dispatch('user/fetchGroups')
      commit('user/SET_GROUPS', groups)
      return groups
    } catch (error) {

    }
  }

  const deleteUserSpecialization = async ({ userId }) => {
    try {
      await dispatch('user/deleteUserSpecialization', { userId })
    } catch (error) {
      console.log(error);
    }
  }

  const createUserSpecialization = async ({ userId, specialitiesId }) => {
    try {
      await dispatch('user/createUserSpecialization', { userId, specialitiesId })
    } catch (error) {
      console.log(error);
    }
  }

  const fetchSpecialitiesByAuthUser = async ({ userId }) => {
    try {
      const { userSpecializations } = await dispatch('auth/fetchSpecialitiesByAuthUser', { userId })
    } catch (error) {
      console.log(error);
    }
  }

  const fetchSpecialities = async ({ langId }) => {
    try {
      const { specializations } = await dispatch('user/fetchSpecialities', { langId })
      const newSpecializations = specializations.map(item => {
        if (item.specializationlangSet && item.specializationlangSet.edges?.length > 0) {
          return {
            id: item.id,
            name: item.specializationlangSet.edges[0]?.node?.name
          }
        } else {
          return {
            id: item.id,
            name: item.name
          }
        }
      })

      commit('user/SET_SPECIALITY', newSpecializations)
    } catch (error) {
      console.log(error);
    }
  }

  const fetchAppointmentCodes = async ({ langId }) => {
    try {
      const { appointmentCode } = await dispatch('user/fetchAppointmentCodes', { langId })
      commit('user/SET_APPOINTMENT_CODE', appointmentCode)
    } catch (error) {
      console.log(error);
    }
  }

  const getUsers = (users, key) => {
    return users.map(item => {
      if (item.node) {
        return item.node
      } else {
        return []
      }
    })
  }

  const updateUserGroup = async ({ userId, group }) => {
    try {
      await dispatch('auth/updateUserGroup', { userId, group })
    } catch (error) {
      console.log(error);
    }
  }

  watchEffect(
    () => {
      if (selectedProfile.value && !selectedProfile.value.id) {
        commit(`auth/${SET_SELECTED_PROFILE}`, profileOptions.value[0])
      }
    })

  return {
    updateUserProfile,
    updateADProfile,
    userProfile,
    selectedProfile,
    profileOptions,
    isDoctor,
    isSwitchToDoctor,
    fetchGroups,
    fetchDoctors,
    fetchPatients,
    fetchSpecialities,
    fetchAppointmentCodes,
    fetchSpecialitiesByAuthUser,
    deleteUserSpecialization,
    createUserSpecialization,
    updateUserGroup,
  }
}

export default useUser