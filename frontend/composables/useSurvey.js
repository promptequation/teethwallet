
import { ref, useStore } from "@nuxtjs/composition-api";


const useSurvey = () => {

    const { dispatch, commit } = useStore()
    const errors = ref("")


    const fetchSurvey = async ({ doctorId }) => {
        try {
            const { surveys } = await dispatch('survey/fetchSurvey', { doctorId })
            commit('survey/SET_SURVEY', surveys)
        } catch (error) {
            console.log(error);
        }
    }

    const fetchAppointmentSurveys = async ({ appointmentId }) => {
        try {
            const { appointmentSurveys } = await dispatch('survey/fetchAppointmentSurveys', { appointmentId })
            commit('survey/SET_APPOINTMENT_SURVEY', appointmentSurveys[0])
        } catch (error) {
            console.log(error);
        }
    }

    const fetchSurveyWithQuestions = async ({ surveyId, appointmentSurveyId }) => {
        try {
            const {surveys} = await dispatch('survey/fetchSurveyWithQuestions', { surveyId, appointmentSurveyId })
            const questions =  surveys[0].surveysquestionSet?.edges.map(question => {

                const userAnswerUpdated = {
                    appointmentSurveyQuestionResponseId: question.node.questionType  === 'MULTIPLE_SELECTION' ?  [] : '',
                    answer: question.node.questionType  === 'MULTIPLE_SELECTION' ?  [] : ''
                }

                    if (question.node.appointmentsurveyquestionresponseSet.edges && question.node.appointmentsurveyquestionresponseSet.edges.length > 0) {
                        if (question.node.questionType === 'RADIO_BUTTON') {
                            const userResponse = question.node.appointmentsurveyquestionresponseSet.edges[0]
                            userAnswerUpdated.appointmentSurveyQuestionResponseId = Number(userResponse.node.id)
                            userAnswerUpdated.answer = Number(userResponse.node.questionResponse.id)
                        }
                        if (question.node.questionType === 'TEXT_FIELD') {
                            const userResponse = question.node.appointmentsurveyquestionresponseSet.edges[0]
                            userAnswerUpdated.appointmentSurveyQuestionResponseId = Number(userResponse.node.id)
                            userAnswerUpdated.answer = userResponse.node.responseValue
                        }
                        if (question.node.questionType === 'MULTIPLE_SELECTION') {
                            const userResponse = question.node.appointmentsurveyquestionresponseSet.edges
                           const ids = []
                           const answers = []
                            userResponse.forEach(response => {
                                ids.push(Number(response.node.id))
                                answers.push(Number(response.node.questionResponse.id))
                            })
                            userAnswerUpdated.appointmentSurveyQuestionResponseId = ids
                            userAnswerUpdated.answer = answers
                        }
                    }


                return {
                      id: Number(question.node.id),
                      title: question.node.title,
                      xmlQuestionId: question.node.xmlQuestionId ? Number(question.node.xmlQuestionId) : null,
                      isConditionalQuestion: question.node.isConditionalQuestion,
                      questionType: question.node.questionType,
                      parentQuestion: question.node.parentQuestion?.id,
                      serialNo: Number(question.node.serialNo),
                      questionResponses: question.node.surveyquestionresponseSet?.edges.map(option => {
                          return {
                              id: Number(option.node.id),
                              answer: option.node.questionResponse,
                              xmlQuestionId: Number(option.node.xmlQuestionId),
                              tragetXmlQuestionIds: option.node.surveyquestionrelationSet?.edges.map(targetQuestion => {
                                  return Number(targetQuestion.node.xmlQuestionResponseTargetQuestionId)
                              })
                          }
                      }),
                      userAnswer: userAnswerUpdated
                }
           })
            commit('survey/SET_QUESTIONS', questions)
        } catch (error) {
            console.log(error);
        }
    }

    const createAppointmentSurveyAnswer = async ({ appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }) => {
        try {
            const { createSurveyAnswer } = await dispatch('survey/submitSurveyQuestionAnswer', { appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById })
            // commit('survey/SET_SURVEY', questions)
        } catch (error) {
            errors.value = error.response
        }
    }

    const updateAppointmentSurveyAnswer = async ({ appointmentSurveyAnswerId, appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }) => {
        try {
            const { createSurveyAnswer } = await dispatch('survey/submitSurveyQuestionAnswer', { appointmentSurveyAnswerId, appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById })
            // commit('survey/SET_SURVEY', questions)
        } catch (error) {
            errors.value = error.response
        }
    }

    const downloadPatientSurveyAnswer = async ({ appointmentId, patientId }) => {
        try {
            const { questions } = await dispatch('survey/downloadPatientSurveyAnswer', { patientId, appointmentId })
            // commit('survey/SET_SURVEY', questions)
        } catch (error) {
            console.log(error);
        }
    }

    const createAppointmentSurveyQuestionResponse = async ({ appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }) => {
        try {
            return await dispatch('survey/createAppointmentSurveyQuestionResponse', { appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID })
        } catch (error) {
            console.log(error);
        }
    }
    const updateAppointmentSurveyQuestionResponse = async ({appointmentSurveyQuestionResponseId, appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }) => {
        try {
            return await dispatch('survey/updateAppointmentSurveyQuestionResponse', {appointmentSurveyQuestionResponseId, appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID })
        } catch (error) {
            console.log(error);
        }
    }

    const surveryQuestionFinished = async ({ appointmentSurveyId, surveyId, appointmentId, isFinished, createdById, updatedById }) => {
        try {
            return await dispatch('survey/surveryQuestionFinished', {appointmentSurveyId, surveyId, appointmentId, isFinished, createdById, updatedById })
        } catch (error) {
            console.log(error);
        }
    }

    const deleteAppointmentSurveyQuestionResponse = async ({appointmentSurveyQuestionResponseId }) => {
        try {
            return await dispatch('survey/deleteAppointmentSurveyQuestionResponse', {appointmentSurveyQuestionResponseId })
        } catch (error) {
            console.log(error);
        }
    }

    return {
        errors,
        fetchSurvey,
        fetchAppointmentSurveys,
        fetchSurveyWithQuestions,
        createAppointmentSurveyAnswer,
        downloadPatientSurveyAnswer,
        updateAppointmentSurveyAnswer,
        createAppointmentSurveyQuestionResponse,
        updateAppointmentSurveyQuestionResponse,
        deleteAppointmentSurveyQuestionResponse,
        surveryQuestionFinished,
    }
}


export default useSurvey