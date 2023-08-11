import { gql } from "nuxt-graphql-request";

const SET_LOADING = 'SET_LOADING'
const SET_APPOINTMENTS = 'SET_APPOINTMENTS'
const PUSH_APPOINTMENTS = 'PUSH_APPOINTMENTS'
const SET_EMPTY_APPOINTMENTS = 'SET_EMPTY_APPOINTMENTS'
const SET_APPOINTMENT_DURATIONS = 'SET_APPOINTMENT_DURATIONS'
const PUSH_APPOINTMENT_DURATION = 'PUSH_APPOINTMENT_DURATION'
const SET_TOOTHS = 'SET_TOOTHS'
const PUSH_TOOTH = 'PUSH_TOOTH'
const SET_DIAGNOSTICS = 'SET_DIAGNOSTICS'
const PUSH_DIAGNOSTIC = 'PUSH_DIAGNOSTIC'
const SET_TREAMMENTS = 'SET_TREAMMENTS'
const PUSH_TREAMMENT = 'PUSH_TREAMMENT'
const SET_PATIENT_DISEASES = 'SET_PATIENT_DISEASES'
const SET_TYPE_OF_APPOINTMENTS = 'SET_TYPE_OF_APPOINTMENTS'

export const state = () => ({
  loading: false,
  tooths: [],
  diagnostics: [],
  treatments: [],
  appointments: [],
  appointmentDurations: [],
  typeOfAppointments: [],
  patientDiseases: []
});

export const getters = {
  tooths(state) {
    return state.tooths
  },
  diagnostics(state) {
    return state.diagnostics
  },
  treatments(state) {
    return state.treatments
  },
  appointments(state) {
    return state.appointments?.map(item => {
      return {
        id: item.node.id,
        duration: item.node.duration,
        startDate: item.node.startDate,
        isActive: item.node.isActive,
        patient: item.node.patient.name,
        doctorId: item.node.doctor.id,
        doctor: item.node.doctor.name,
        appointmentFollowUp: item.node.appointmentFollowUp,
        appointmentDetails: item.node.appointmentDetails,
        appointmentprioritySet: item.node.appointmentprioritySet,
        companyId: item.node.company.id,
        companyName: item.node.company.name,
        survey: item.node.appointmentSurvey,
      }
    })

  },
  durations(state) {
    return state.appointmentDurations.map(item => {
      if (item.number >= 60) {
        item.text = Math.ceil(item.number / 60) + 'h'
      } else {
        item.text = Math.ceil(item.number) + 'm'
      }
      return item
    })
  },
  typeOfAppointments(state) {
    return state.typeOfAppointments
  },
  patientDiseases(state) {
    return state.patientDiseases
  },
}

export const mutations = {
  [SET_LOADING](state, payload) {
    state.loading = payload
  },
  [SET_APPOINTMENTS](state, payload) {
    state.appointments = payload
  },
  [PUSH_APPOINTMENTS](state, payload) {
    if (payload && payload.length > 0) {
      state.appointments.push(...payload)
    }
  },
  [SET_EMPTY_APPOINTMENTS](state) {
    state.appointments = []
  },
  [SET_TOOTHS](state, payload) {
    state.tooths = payload
  },
  [PUSH_TOOTH](state, payload) {
    state.tooths.push(payload)
  },
  [SET_DIAGNOSTICS](state, payload) {
    state.diagnostics = payload
  },
  [PUSH_DIAGNOSTIC](state, payload) {
    state.diagnostics.push(payload)
  },
  [SET_TREAMMENTS](state, payload) {
    state.treatments = payload
  },
  [PUSH_TREAMMENT](state, payload) {
    state.treatments.push(payload)
  },
  [SET_APPOINTMENT_DURATIONS](state, payload) {
    state.appointmentDurations = payload
  },
  [PUSH_APPOINTMENT_DURATION](state, payload) {
    state.appointmentDurations.push(payload)
  },
  [SET_PATIENT_DISEASES](state, payload) {
    state.patientDiseases = payload
  },
  [SET_TYPE_OF_APPOINTMENTS](state, payload) {
    state.typeOfAppointments = payload
  },
}

export const actions = {
  async fetchAppointments({ }, { patientId, doctorId, companyId, langId, isActive }) {
    const query = gql`
        query ($patientId: ID, $doctorId: Float, $companyId: Float, $langId: Float, $isActive: Boolean) {
          appointments(
            patient: $patientId
            doctor_Id: $doctorId
            company_Id: $companyId
            isActive: $isActive
          ) {
            edges {
              node {
                id
                patient {
                  id
                  name
                }
                doctor {
                  id
                  name
                }
                company {
                  id
                  name
                }
                isActive
                startDate
                duration
                createdAt
                appointmentDetails {
                  edges {
                    node {
                      id
                      tooth {
                        id
                        number
                      }
                      diagnosis {
                        id
                        diagnosticlangSet(lang_Id: $langId){
                          edges{
                            node{
                              id
                              name
                            }
                          }
                        }
                      }
                      treatment {
                        id
                        treatmentlangSet(lang_Id: $langId){
                          edges{
                            node{
                              id
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }
                appointmentprioritySet {
                  edges {
                    node {
                      id
                      priority {
                        id
                        name
                      }
                    }
                  }
                }
                appointmentlangSet(lang_Id: $langId){
                  edges{
                    node{
                      note
                    }
                  }
                }
                appointmentSurvey {
                  edges {
                    node {
                      id
                      survey {
                        id
                        name
                        file
                        createdAt
                      }
                      createdAt
                    }
                  }
                }
              }
            }
          }
        }`

    const variables = { patientId, doctorId, companyId, langId, isActive }
    return await this.$graphql.default.request(query, variables);
  },
  async fetchSingleAppointment({ }, { id, langId }) {
    const query = gql`
         query ($id: Float, $langId:Float) {
          appointments(id: $id) {
            edges {
              node {
                id
                patient {
                  id
                  name
                }
                doctor {
                  id
                  name
                }
                company{
                  id
                  name
                }
                note
                startDate
                duration
                appointmentFollowUp{
                  edges{
                      node{
                          id
                          followUpDate
                      }
                   }
                }
                appointmentDetails {
                  edges {
                    node {
                      id
                      tooth {
                        id
                        number
                      }
                      diagnosis {
                        id
                        diagnosticlangSet(lang_Id: $langId){
                          edges{
                            node{
                              id
                              name
                            }
                          }
                        }
                      }
                      treatment {
                        id
                        treatmentlangSet(lang_Id: $langId){
                          edges{
                            node{
                              id
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }
                appointmentprioritySet {
                  edges {
                    node {
                      id
                      priority {
                        id
                        name
                      }
                    }
                  }
                }
                appointmentspecializationSet {
                  edges {
                    node {
                      id
                      specialization {
                        id
                        name
                      }
                    }
                  }
                }
                appointmentlangSet(lang_Id: $langId){
                  edges{
                    node{
                      note
                    }
                  }
                }
                appointmentfileSet{
                  edges{
                    node{
                      id
                      name
                      file
                      createdAt
                      updatedAt
                    }
                  }
                }
                appointmentSurvey {
                  edges {
                    node {
                      id
                      survey {
                        id
                        name
                        file
                        createdAt
                      }
                      createdAt
                    }
                  }
                }
                appointmentshortcodeSet {
                    edges {
                        node {
                            id
                            appointmentCode {
                                id
                            }
                        }
                    }
                }
              }
            }
          }
        }`;

    const variables = { id, langId }
    return await this.$graphql.default.request(query, variables);
  },

  async fetchAppointmentDuration() {
    const mutation = gql`
        query{
            durations{
                id
                number
            }
        }
        `
    return await this.$graphql.default.request(mutation);
  },

  async createAppointment({ }, { companyId, patientId, doctorId, startDate, duration, note, createdBy, updatedBy }) {
    const mutation = gql`
           mutation (
              $companyId: ID
              $patientId: ID
              $doctorId: ID
              $startDate: DateTime
              $duration: Int
              $note: String
              $createdBy: ID
              $updatedBy: ID
            ) {
              createAppointment(
                input: {
                  company: $companyId
                  patient: $patientId
                  doctor: $doctorId
                  startDate: $startDate
                  duration: $duration
                  note: $note
                  createdBy: $createdBy
                  updatedBy: $updatedBy
                }
              ) {
                appointment {
                  id
                }
              }
            }`

    const variables = { companyId, patientId, doctorId, startDate, duration, note, createdBy, updatedBy }

    return await this.$graphql.default.request(mutation, variables);

  },

  async updateAppointment({ }, { id, companyId, patientId, doctorId, startDate, duration, note, updatedBy }) {
    const mutation = gql`
            mutation (
              $id: ID
              $companyId: ID
              $patientId: ID
              $doctorId: ID
              $startDate: DateTime
              $duration: Int
              $note: String
              $updatedBy: ID
            ) {
              updateAppointment(
                input: {
                  id: $id
                  company: $companyId
                  patient: $patientId
                  doctor: $doctorId
                  startDate: $startDate
                  duration: $duration
                  note: $note
                  updatedBy: $updatedBy
                }
              ) {
                appointment {
                  id
                }
              }
            }`

    const variables = { id, companyId, patientId, doctorId, startDate, duration, note, updatedBy }

    return await this.$graphql.default.request(mutation, variables);
  },

  async deleteAppointment({ }, { id }) {
    const mutation = gql`
             mutation ($id: ID) {
                deleteAppointment(id: $id) {
                    appointment {
                        id
                    }
                }
            }
        `
    const variables = { id }
    return await this.$graphql.default.request(mutation, variables);
  },
  async createAppointmentDetails({ }, { appointmentId, toothId, diagnosticId, treatmentId, createdBy, updatedBy }) {
    const mutation = gql`
       mutation($appointmentId:ID,$toothId:ID,$diagnosticId:ID,$treatmentId:ID, $createdBy:ID, $updatedBy:ID){
            createAppointmentDetails(input:{
                appointment: $appointmentId,
                tooth: $toothId,
                diagnosis:$diagnosticId,
                treatment:$treatmentId,
                createdBy: $createdBy,
                updatedBy:$updatedBy
            }){
                appointmentDetails{
                    id
                    tooth{
                        id
                        number
                    }
                    diagnosis{
                      id
                      diagnosticlangSet{
                        edges{
                          node{
                            id
                            name
                          }
                        }
                      }
                  }
                  treatment{
                    id
                    treatmentlangSet{
                      edges{
                        node{
                          id
                          name
                        }
                      }
                    }
                }
                }
            }
        }
        `

    const variables = { appointmentId, toothId, diagnosticId, treatmentId, createdBy, updatedBy }

    return await this.$graphql.default.request(mutation, variables);
  },

  async createAppointmentShortCode({ }, { appointmentId, codeId, createdBy, updatedBy }) {
    const mutation = gql`
       mutation($appointmentId:ID, $codeId:ID, $createdBy:ID, $updatedBy:ID){
         createAppointmentShortCode(input:{
                appointment: $appointmentId,
                appointmentCode: $codeId,
                createdBy: $createdBy,
                updatedBy:$updatedBy
            }){
              appointmentShortCode {
                appointment {
                  id
                }
                appointmentCode {
                  id
                  name
                }
              }
            }
        }
        `

    const variables = { appointmentId, codeId, createdBy, updatedBy }

    return await this.$graphql.default.request(mutation, variables);
  },

  async updateAppointmentDetails({ }, { id, appointmentId, toothId, diagnosticId, treatmentId, updatedBy }) {
    const mutation = gql`
       mutation ($id:ID, $appointmentId: ID, $toothId: ID, $diagnosticId: ID, $treatmentId: ID, $updatedBy: ID) {
        updateAppointmentDetails(input: {id:$id, appointment: $appointmentId, tooth: $toothId, diagnosis: $diagnosticId, treatment: $treatmentId, updatedBy: $updatedBy}) {
            appointmentDetails {
                id
                tooth{
                    id
                    number
                }
                diagnosis{
                    id
                    diagnosticlangSet{
                      edges{
                        node{
                          id
                          name
                        }
                      }
                    }
                }
                treatment{
                    id
                    treatmentlangSet{
                      edges{
                        node{
                          id
                          name
                        }
                      }
                    }
                }
            }
        }
        }
        `
    const variables = { id, appointmentId, toothId, diagnosticId, treatmentId, updatedBy }
    return await this.$graphql.default.request(mutation, variables);
  },
  async deleteAppointmentDetails({ }, { id }) {
    const mutation = gql`
            mutation ($id:ID){
                deleteAppointmentDetails(id: $id){
                    appointment{
                        id
                    }
                }
            }
        `
    const variables = { id }
    return await this.$graphql.default.request(mutation, variables);
  },

  async deleteAppointmentShortCode({ }, { id }) {
    const mutation = gql`
            mutation ($id:ID){
                deleteAppointmentShortCode(id: $id){
                    appointmentShortCode {
                        id
                    }
                }
            }
        `
    const variables = { id }
    return await this.$graphql.default.request(mutation, variables);
  },

  async fetchTooths({ }) {
    const query = gql`
          query {
            teeth {
                id
                number
            }
          }
        `;
    return await this.$graphql.default.request(query);
  },

  async fetchDiagnostics({ }, {langId}) {
    const query = gql`
          query($langId: Float) {
            diagnostics {
                id
                name
                diagnosticlangSet(lang_Id: $langId){
                  edges{
                    node{
                      id
                      name
                    }
                  }
                }
            }
          }
        `;
    const variables = { langId }
    return await this.$graphql.default.request(query, variables);
  },

  async fetchTreatments({ }, {langId}) {
    const query = gql`
          query($langId: Float){
            treatments {
                id
                treatmentlangSet(lang_Id: $langId){
                  edges{
                    node{
                      id
                      name
                    }
                  }
                }
            }
          }
        `;
    const variables = { langId }
    return await this.$graphql.default.request(query, variables);
  },

  async createTooth({ }, { number, createdBy }) {
    const mutation = gql`
            mutation($number:Int, $createdBy:Int){
                createTooth(input:{number:$number, createdBy: $createdBy}){
                    tooth {
                        id
                        number
                    }
                }
            }
        `
    const variables = { number, createdBy }
    return await this.$graphql.default.request(mutation, variables);
  },
  async createDiagnostic({ }, { name, createdBy }) {
    const mutation = gql`
          mutation($name: String, $createdBy: Int) {
            createDiagnostic(input: { name: $name, createdBy: $createdBy }) {
              diagnostic {
                id
                name
              }
            }
          }
        `;

    const variables = { name, createdBy };

    return await this.$graphql.default.request(mutation, variables);
  },

  async createTreatment({ }, { name, createdBy }) {
    const mutation = gql`
          mutation($name: String, $createdBy: Int) {
            createTreatment(input: { name: $name, createdBy: $createdBy }) {
              treatment {
                id
                name
              }
            }
          }
        `;

    const variables = { name, createdBy };

    return await this.$graphql.default.request(mutation, variables);
  },
  async createAppointmentDuration({ }, { number, createdBy }) {
    const mutation = gql`
          mutation($number:Int, $createdBy:ID){
            createDuration(input:{number: $number, createdBy: $createdBy}){
                durations{
                    id
                    number
                }
            }
        }
        `;

    const variables = { number, createdBy };

    return await this.$graphql.default.request(mutation, variables);
  },

  async fetchPatientDiseases({ }, { patientId }) {
    const mutation = gql`
          mutation($number:Int, $createdBy:ID){
            durationsCreate(input:{number: $number, createdBy: $createdBy}){
                durations{
                    id
                    number
                }
            }
        }
        `;

    const variables = { patientId };

    return await this.$graphql.default.request(mutation, variables);
  },

  async fetchPriorities({}, {langId}) {
    const mutation = gql`
          query($langId: Float){
            priorities {
              id
              name
              prioritylangSet(lang_Id: $langId) {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
          }`;

    const variables = { langId };
    return await this.$graphql.default.request(mutation, variables);
  },

  async createAppointmentPriority({ }, { appointmentId, priorityId, createdById, updatedById }) {
    const mutation = gql`
     mutation ($appointmentId: ID, $priorityId: ID, $createdById: ID, $updatedById: ID) {
      createAppointmentPriority(
        input: {
          appointment: $appointmentId
          priority: $priorityId
          createdBy: $createdById
          updatedBy: $updatedById
        }
      ) {
        appointmentPriority {
          id
        }
      }
    }`

    const variables = { appointmentId, priorityId, createdById, updatedById }

    return await this.$graphql.default.request(mutation, variables)
  },

  async updateAppointmentPriority({ }, { id, appointmentId, priorityId, createdById, updatedById }) {
    const mutation = gql`
     mutation (
      $id: ID
      $appointmentId: ID
      $priorityId: ID
      $createdById: ID
      $updatedById: ID
    ) {
      updateAppointmentPriority(
        input: {
          id: $id
          appointment: $appointmentId
          priority: $priorityId
          createdBy: $createdById
          updatedBy: $updatedById
        }
      ) {
        appointmentPriority {
          id
        }
      }
    }`

    const variables = { id, appointmentId, priorityId, createdById, updatedById }

    return await this.$graphql.default.request(mutation, variables)
  },

  async deleteAppointmentPriority({ }, { id }) {
    const mutation = gql`
     mutation ($id: ID) {
      deleteAppointmentPriority(id: $id) {
        appointmentPriority {
          id
        }
      }
    }`

    const variables = { id }

    return await this.$graphql.default.request(mutation, variables)
  },

  async createAppointmentSpecialization({ }, { appointmentId, specializationId, createdById, updatedById }) {
    const mutation = gql`
     mutation (
      $appointmentId: ID
      $specializationId: ID
      $createdById: ID
      $updatedById: ID
    ) {
      createAppointmentSpecialization(
        input: {
          appointment: $appointmentId
          specialization: $specializationId
          createdBy: $createdById
          updatedBy: $updatedById
        }
      ) {
        appointmentSpecialization {
          id
        }
      }
    }`

    const variables = { appointmentId, specializationId, createdById, updatedById }

    return await this.$graphql.default.request(mutation, variables)
  },

  async updateAppointmentSpecialization({ }, { id, appointmentId, specializationId, createdById, updatedById }) {
    const mutation = gql`
     mutation (
      $id: ID
      $appointmentId: ID
      $specializationId: ID
      $createdById: ID
      $updatedById: ID
    ) {
      updateAppointmentSpecialization(
        input: {
          id: $id
          appointment: $appointmentId
          specialization: $specializationId
          createdBy: $createdById
          updatedBy: $updatedById
        }
      ) {
        appointmentSpecialization {
          id
        }
      }
    }`

    const variables = { id, appointmentId, specializationId, createdById, updatedById }

    return await this.$graphql.default.request(mutation, variables)
  },

  async deleteAppointmentSpecialization({ }, { id }) {
    const mutation = gql`
    mutation ($id: ID) {
      deleteAppointmentSpecialization(id: $id) {
        appointmentSpecialization {
          id
        }
      }
    }`

    const variables = { id }

    return await this.$graphql.default.request(mutation, variables)
  },

  async createAppointmentFile({ }, { name, file, appointmentId, doctorId, createdById, updatedById }) {
    const mutation = gql`
          mutation (
              $name: String
              $file: Upload
              $appointmentId: ID
              $doctorId: ID
              $createdById: ID
              $updatedById: ID
            ) {
              createAppointmentFile(
                input: {
                  name: $name
                  file: $file
                  appointment: $appointmentId
                  doctor: $doctorId
                  createdBy: $createdById
                  updatedBy: $updatedById
                }
              ) {
                appointmentFile {
                  id
                  name
                  file
                }
              }
            }`

    const variables = { name, file, appointmentId, doctorId, createdById, updatedById }
    return await this.$graphql.default.request(mutation, variables)
  },

  async createAppointmentSurvey({ }, { surveyId, appointmentId, createdById, updatedById }) {
    const mutation = gql`
            mutation (
              $surveyId: ID
              $appointmentId: ID
              $createdById: ID
              $updatedById: ID
            ) {
              createAppointmentSurvey(
                input: {
                  appointment: $appointmentId
                  survey: $surveyId
                  createdBy: $createdById
                  updatedBy: $updatedById
                }
              ) {
                appointmentSurvey {
                  id
                }
              }
            }`

    const variables = {surveyId, appointmentId, createdById, updatedById }
    return await this.$graphql.default.request(mutation, variables)
  },

  async updateAppointmentSurvey({ }, { appointmentSurveyId, surveyId, appointmentId, createdById, updatedById }) {
    const mutation = gql`
          mutation (
            $appointmentSurveyId: ID
            $surveyId: ID
            $appointmentId: ID
            $createdById: ID
            $updatedById: ID
          ) {
            updateAppointmentSurvey(
              input: {
                id: $appointmentSurveyId
                appointment: $appointmentId
                survey: $surveyId
                createdBy: $createdById
                updatedBy: $updatedById
              }
            ) {
              appointmentSurvey {
                id
              }
            }
          }`
    const variables = {appointmentSurveyId, surveyId, appointmentId, createdById, updatedById }
    return await this.$graphql.default.request(mutation, variables)
  },

  async deleteAppointmentSurvey({ }, { appointmentSurveyId }) {
    const mutation = gql`
         mutation($appointmentSurveyId:ID){
          deleteAppointmentSurvey(id:$appointmentSurveyId){
            appointmentSurvey{
              id
            }
          }
        }`
    const variables = {appointmentSurveyId }
    return await this.$graphql.default.request(mutation, variables)
  },
}


