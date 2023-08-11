import { ref, useStore } from '@nuxtjs/composition-api'

const useAppointment = () => {
  const { dispatch, commit } = useStore()

  const errors = ref("")

  const fetchAppointments = async ({ patientId, doctorId, companyId, langId, isActive }) => {
    try {
      const { appointments } = await dispatch('appointment/fetchAppointments', { patientId, doctorId, companyId, langId, isActive })
      commit('appointment/SET_APPOINTMENTS', appointments.edges)
    } catch (error) {
      console.log(error);
    }
  }
  const fetchSingleAppointment = async ({id, langId}) => {
    try {
      return await dispatch('appointment/fetchSingleAppointment', { id, langId })
    } catch (error) {
      console.log(error);
    }
  }
  const fetchAppointmentDuration = async () => {
    try {
      const { durations } = await dispatch('appointment/fetchAppointmentDuration')
      commit('appointment/SET_APPOINTMENT_DURATIONS', durations)
    } catch (error) {
      console.log(error);
    }
  }

  const createAppointment = async (companyId, patientId, doctorId, startDate, duration, note, createdBy, updatedBy) => {
    try {
      return await dispatch('appointment/createAppointment', {
        companyId, patientId, doctorId, startDate, duration, note, createdBy, updatedBy
      })
    } catch (error) {
      errors.value = error.response
    }
  }

  const updateAppointment = async (id, companyId, patientId, doctorId, startDate, duration, note, updatedBy) => {
    try {
      const res = await dispatch('appointment/updateAppointment', {
        id, companyId, patientId, doctorId, startDate, duration, note, updatedBy
      })
      return res
    } catch (error) {
      errors.value = error.response
    }
  }

  const deleteAppointment = async (id) => {
    try {
      return await dispatch('appointment/deleteAppointment', { id })
    } catch (error) {
      errors.value = error.response
    }
  }

  const createAppointmentDetails = async ( appointmentId, toothId, diagnosticId, treatmentId, createdBy, updatedBy) => {
    try {
      return await dispatch('appointment/createAppointmentDetails', { appointmentId, toothId, diagnosticId, treatmentId, createdBy, updatedBy })

    } catch (error) {
      errors.value = error.response
    }
  }

  const createAppointmentShortCode = async ( appointmentId, codeId, createdBy, updatedBy) => {
    try {
      return await dispatch('appointment/createAppointmentShortCode', { appointmentId, codeId, createdBy, updatedBy })

    } catch (error) {
      errors.value = error.response
    }
  }


  const updateAppointmentDetails = async (id, appointmentId, toothId, diagnosticId, treatmentId, updatedBy) => {
    try {
      return await dispatch('appointment/updateAppointmentDetails', { id, appointmentId, toothId, diagnosticId, treatmentId, updatedBy })
    } catch (error) {
      errors.value = error.response
    }
  }

  const deleteAppointmentDetails = async (id) => {
    try {
      return await dispatch('appointment/deleteAppointmentDetails', { id })
    } catch (error) {
      errors.value = error.response
    }
  }

  const deleteAppointmentShortCode = async (id) => {
    try {
      return await dispatch('appointment/deleteAppointmentShortCode', { id })
    } catch (error) {
      errors.value = error.response
    }
  }

  const fetchTooths = async () => {
    try {
      const { teeth } = await dispatch('appointment/fetchTooths')
      commit('appointment/SET_TOOTHS', teeth)
    } catch (error) {
      console.log(error);
    }
  }
  const fetchDiagnostics = async ({ langId }) => {
    try {
      const { diagnostics } = await dispatch('appointment/fetchDiagnostics', { langId })
      const newDiagnostic = diagnostics.map(item => {
        if (item.diagnosticlangSet && item.diagnosticlangSet.edges?.length > 0) {
          return {
            id: item.id,
            name: item.diagnosticlangSet.edges[0]?.node?.name
          }
        } else {
          return {
            id: item.id,
            name: item.name
          }
        }
      })
      commit('appointment/SET_DIAGNOSTICS', newDiagnostic)
    } catch (error) {
      console.log(error);
    }
  }

  const fetchTreatments = async ({ langId }) => {
    try {
      const { treatments } = await dispatch('appointment/fetchTreatments', { langId })
      const newTreatments = treatments.map(item => {
        if (item.treatmentlangSet && item.treatmentlangSet.edges?.length > 0) {
          return {
            id: item.id,
            name: item.treatmentlangSet.edges[0]?.node?.name
          }
        } else {
          return {
            id: item.id,
            name: item.name
          }
        }
      })
      commit('appointment/SET_TREAMMENTS', newTreatments)
    } catch (error) {
      console.log(error);
    }
  }

  const createTooth = async (number, createdBy) => {
    try {
      const { createTooth } = await dispatch('appointment/createTooth', { number, createdBy })
      const { tooth } = createTooth
      commit('appointment/PUSH_TOOTH', tooth)
      return tooth
    } catch (error) {
      errors.value = error.response
    }
  }
  const createDiagnostic = async (name, createdBy) => {
    try {
      const { createDiagnostic } = await dispatch('appointment/createDiagnostic', { name, createdBy })
      const { diagnostic } = createDiagnostic
      commit('appointment/PUSH_DIAGNOSTIC', diagnostic)
      return diagnostic
    } catch (error) {
      errors.value = error.response
    }
  }

  const createTreatment = async (name, createdBy) => {
    try {
      const { createTreatment } = await dispatch('appointment/createTreatment', { name, createdBy })
      const { treatment } = createTreatment
      commit('appointment/PUSH_TREAMMENT', treatment)
      return treatment
    } catch (error) {
      errors.value = error.response
    }
  }

  const createAppointmentDuration = async (number, createdBy) => {
    try {
      const { createDuration } = await dispatch('appointment/createAppointmentDuration', { number, createdBy })
      const { durations } = createDuration
      commit('appointment/PUSH_APPOINTMENT_DURATION', durations)
      return durations
    } catch (error) {
      errors.value = error.response
    }
  }

  const fetchPatientDiseases = async (patientId) => {
    try {
      const { diseases } = await dispatch('appointment/fetchPatientDiseases', { patientId })
      commit('appointment/SET_PATIENT_DISEASES', diseases)
    } catch (error) {
      console.log(error);
    }
  }

  const fetchPriorities = async ({langId}) => {
    try {
      const { priorities } = await dispatch('appointment/fetchPriorities', {langId})
        const newPriorities = priorities.map(item => {
            if (item.prioritylangSet && item.prioritylangSet.edges?.length > 0) {
                return {
                    id: item.id,
                    name: item.prioritylangSet.edges[0]?.node?.name
                }
            }else{
                return {
                    id: item.id,
                    name: item.name
                }
            }
        })
      commit('appointment/SET_TYPE_OF_APPOINTMENTS', newPriorities)
    } catch (error) {
      console.log(error);
    }
  }

  const createAppointmentPriority = async ({ appointmentId, priorityId, createdById, updatedById }) => {
    try {
      await dispatch('appointment/createAppointmentPriority', { appointmentId, priorityId, createdById, updatedById })
    } catch (error) {
      errors.value = error.response
    }
  }

  const updateAppointmentPriority = async ({ id, appointmentId, priorityId, createdById, updatedById }) => {
    try {
      await dispatch('appointment/updateAppointmentPriority', { id, appointmentId, priorityId, createdById, updatedById })
    } catch (error) {
      errors.value = error.response
    }
  }

  const deleteAppointmentPriority = async ({ id }) => {
    try {
      const { deleteAppointmentPriority } = await dispatch('appointment/deleteAppointmentPriority', { id })
      console.log(deleteAppointmentPriority);
    } catch (error) {
      console.log(error);
    }
  }

  const createAppointmentSpecialization = async ({ appointmentId, specializationId, createdById, updatedById }) => {
    try {
      await dispatch('appointment/createAppointmentSpecialization', { appointmentId, specializationId, createdById, updatedById })
    } catch (error) {
      errors.value = error.response
    }
  }

  const updateAppointmentSpecialization = async ({ id, appointmentId, specializationId, createdById, updatedById }) => {
    try {
      await dispatch('appointment/updateAppointmentSpecialization', { id, appointmentId, specializationId, createdById, updatedById })
    } catch (error) {
      errors.value = error.response
    }
  }

  const deleteAppointmentSpecialization = async ({ id }) => {
    try {
      const { deleteAppointmentSpecialization } = await dispatch('appointment/deleteAppointmentSpecialization', { id })
      console.log(deleteAppointmentSpecialization);
    } catch (error) {
      console.log(error);
    }
  }

  const createAppointmentFile = async ({ name, file, appointmentId, doctorId, createdById, updatedById }) => {
    try {
      const res = await dispatch('appointment/createAppointmentFile', { name, file, appointmentId, doctorId, createdById, updatedById })
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  const createAppointmentSurvey = async ({ surveyId, appointmentId, createdById, updatedById  }) => {
    try {
      return await dispatch('appointment/createAppointmentSurvey', { surveyId, appointmentId, createdById, updatedById })
    } catch (error) {
      console.log(error);
    }
  }

  const updateAppointmentSurvey = async ({ appointmentSurveyId, surveyId, appointmentId, createdById, updatedById }) => {
    try {
      return await dispatch('appointment/updateAppointmentSurvey', { appointmentSurveyId, surveyId, appointmentId, createdById, updatedById })
    } catch (error) {
      console.log(error);
    }
  }

  const deleteAppointmentSurvey = async ({ appointmentSurveyId }) => {
    try {
      return await dispatch('appointment/deleteAppointmentSurvey', { appointmentSurveyId })
    } catch (error) {
      console.log(error);
    }
  }



  return {
    createAppointment,
    updateAppointment,
    deleteAppointment,
    createAppointmentDetails,
    updateAppointmentDetails,
    deleteAppointmentDetails,
    fetchTooths,
    fetchDiagnostics,
    fetchTreatments,
    createTooth,
    createDiagnostic,
    createTreatment,
    fetchAppointments,
    fetchSingleAppointment,
    fetchAppointmentDuration,
    createAppointmentDuration,
    fetchPatientDiseases,
    fetchPriorities,
    createAppointmentPriority,
    updateAppointmentPriority,
    deleteAppointmentPriority,
    createAppointmentSpecialization,
    updateAppointmentSpecialization,
    deleteAppointmentSpecialization,
    errors,
    createAppointmentFile,
    createAppointmentSurvey,
    updateAppointmentSurvey,
    deleteAppointmentSurvey,
    createAppointmentShortCode,
    deleteAppointmentShortCode,
  }
}


export default useAppointment
