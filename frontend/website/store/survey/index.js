import { gql } from "nuxt-graphql-request";
import Vue from 'vue';

const SET_SURVEY = "SET_SURVEY"
const PUSH_SURVEY = "PUSH_SURVEY"
const UPDATE_QUESTION = "UPDATE_QUESTION"
const SET_QUESTIONS = "SET_QUESTIONS"
const PUSH_TARGET_QUESTION = "PUSH_TARGET_QUESTION"
const REMOVE_QUESTIONS = "REMOVE_QUESTIONS"
const UPDATE_QUESTION_ANSWER = "UPDATE_QUESTION_ANSWER"
const UPDATE_MULTIPLE_QUESTION_ANSWER = "UPDATE_MULTIPLE_QUESTION_ANSWER"
const SET_APPOINTMENT_SURVEY = "SET_APPOINTMENT_SURVEY"



// const item = {
//     id: question.node.id,
//     parentSurvey: question.node.parentSurvey?.id,
//     serialNo: question.node.serialNo,
//     surveyType: question.node.surveyType,
//     // surveyanswerSet: question.node.surveyanswerSet?.edges.map(option => {
//     //     return {
//     //             xmlSurveyAnswerId: option.node.xmlSurveyAnswerId,
//     //             answer: option.node.answer,
//     //             targetXmlSurveyIds: option.node.surveyanwsertargetSet?.edges.map(targetQuestion => {
//     //                 return {
//     //                     targetXmlSurveyIds: targetQuestion.node.xmlSurveyAnswerTargetSurveyId
//     //                 }
//     //             })
//     //         }
//     // }),
//     title: question.node.title,
//     xmlSurveyId: question.node.xmlSurveyId,
// }



export const state = () => ({
    surveys: [
        // { id: 1, name: 'survey one', createdAt: new Date().toDateString() },
        // { id: 2, name: 'survey two', createdAt: new Date().toDateString() },
        // { id: 3, name: 'survey three', createdAt: new Date().toDateString() },
        // { id: 4, name: 'survey four', createdAt: new Date().toDateString() },
    ],
    decisionTrees: {},
    questions: [
        // { id: 1, title: 'Question One', answer: '' },
        // { id: 2, title: 'Question Two', answer: '' },
        // { id: 3, title: 'Question Three', answer: '' },
        // { id: 4, title: 'Question Four', answer: '' },
        // { id: 5, title: 'Question Five', answer: '' },
    ],
    nextQuestions: [],
    appointmentSurvey: {}
});

export const getters = {
    surveys(state) {
        return state.surveys
    },
    allQuestions(state) {
        return state.questions
    },
    questions(state) {
        return state.nextQuestions
    },
    appointmentSurvey(state) {
        return state.appointmentSurvey
    },
};

export const mutations = {
    [SET_SURVEY](state, payload) {
        state.surveys = payload
    },
    [SET_APPOINTMENT_SURVEY](state, payload){
        state.appointmentSurvey = payload
    },
    [PUSH_SURVEY](state, payload) {
        state.surveys.push(payload)
    },
    [UPDATE_QUESTION](state, { question, index }) {
        Vue.set(state.questions, index, question)
    },
    [SET_QUESTIONS](state, questions) {
        // console.log(questions);
        const parentQuestions = questions.filter(question => {
            return  question.parentQuestion === undefined || question.parentQuestion === null ||  question.parentQuestion === ''
        })
        state.nextQuestions = parentQuestions
        state.questions = questions
    },
    [PUSH_TARGET_QUESTION](state, {currentQuestion, newQs,nextIndexNumber}){
        // const targetIds = selectedAnswer.targetXmlSurveyIds.map(id => {
        //     return id.targetXmlSurveyIds
        // })

     state.nextQuestions.splice(nextIndexNumber, 0, ...newQs)

       const uniqueQuestion = [...new Map(state.nextQuestions.map(item =>
        [item['id'], item])).values()];

        state.nextQuestions = uniqueQuestion
    // state.nextQuestions = state.nextQuestions.concat(newQs)

        // if (targetIds.length > 0) {
        //     const newQ =  state.questions.filter(question => {
        //         return targetIds.includes(Number(question.xmlSurveyId))
        //     })    
        //     console.log(targetIds);        
        //     console.log(newQ);        
        //     state.nextQuestions = state.nextQuestions.concat(newQ)
        // }
    },
    [REMOVE_QUESTIONS](state, {tragetXmlQuestionIds, index}){
        // state.nextQuestions.splice(index, 1)
        if (tragetXmlQuestionIds.length > 0) {
            const solidQuestions = state.nextQuestions.filter(question => {
                return !tragetXmlQuestionIds.includes(question.xmlQuestionId)
            })
            // const uniqueQuestion = [...new Map(solidQuestions.map(item =>
            //     [item['id'], item])).values()];

            state.nextQuestions = solidQuestions
        }
    },

    [UPDATE_QUESTION_ANSWER](state, question){
        const index = state.nextQuestions.findIndex(ques => {
            return Number(question.id) === Number(ques.id)
        })
        Vue.set(state.nextQuestions, index, question)
    },
    [UPDATE_MULTIPLE_QUESTION_ANSWER](state, {question, id}){
        const questionIndex = state.nextQuestions.findIndex(ques => {
            return Number(question.id) === Number(ques.id)
        })
        
        if (questionIndex > -1) {
            let newQuestion = JSON.parse(JSON.stringify(question))
            if (newQuestion.userAnswer.answer.indexOf(id) != -1) {
              const newList = newQuestion.userAnswer.answer.filter(data => data != id);
              newQuestion.userAnswer.answer = newList
            } else {
              newQuestion.userAnswer.answer.push(id)
            }
            Vue.set(state.nextQuestions, questionIndex, question)
        }
    }
};

export const actions = {
    async fetchSurvey({ }, { doctorId }) {
        const query = gql`
        query{
            surveys{
              id
              name
              file
              createdAt
            }
          }`

        // const variables = { doctorId }

        // return await this.$graphql.default.request(query, variables);
        return await this.$graphql.default.request(query);
    },

    async fetchAppointmentSurveys({ }, { appointmentId }) {
        const query = gql`
        query($appointmentId:Int){
            appointmentSurveys(appointmentId:$appointmentId){
              id
              isFinished
              appointment{
                id
              }
              survey{
                id
              }
            }
          }`

        const variables = { appointmentId }

        return await this.$graphql.default.request(query, variables);
    },

 
    async fetchSurveyWithQuestions({ }, { surveyId, appointmentSurveyId }) {
        const query = gql`
        query ($surveyId: Int, $appointmentSurveyId:Float) {
            surveys(pk: $surveyId) {
              id
              surveysquestionSet {
                edges {
                  node {
                    id
                    questionType
                    serialNo
                    isConditionalQuestion
                    createdAt
                    title
                    defaultDisplay
                    xmlQuestionId
                    parentQuestion {
                      id
                    }
                    surveyquestionresponseSet {
                      edges {
                        node {
                          id
                          xmlQuestionId
                          questionResponse
                          surveyquestionrelationSet {
                            edges {
                              node {
                                xmlQuestionResponseTargetQuestionId
                              }
                            }
                          }
                        }
                      }
                    }
                    appointmentsurveyquestionresponseSet (appointmentSurvey_Id:$appointmentSurveyId){
                      edges{
                        node{
                          responseValue
                                          id
                          questionResponse{
                            id
                            questionResponse
                          }
                          appointmentSurvey{
                            appointment{
                              doctor{
                                id
                                name
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }                                
        `
        const variables = { surveyId, appointmentSurveyId }

        return await this.$graphql.default.request(query, variables);
    },

    async createAppointmentSurveyAnswer({ }, {appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }) {
        const query = gql`
                mutation (
                    $appointmentDecisionTreeId: ID
                    $surveyId: ID
                    $surveyAnswerId: ID
                    $createdById: ID
                ) {
                    createAppointmentSurveyAnswer(
                    input: {
                        appointmentDecisionTree: $appointmentDecisionTreeId
                        survey: $surveyId
                        surveyAnswer: $surveyAnswerId
                        createdBy: $createdById
                    }
                    ) {
                    appointmentSurveyAnswer {
                        id
                    }
                    }
                }`

        const variables = { appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }
        return await this.$graphql.default.request(query, variables);
    },

    async updateAppointmentSurveyAnswer({ }, { appointmentSurveyAnswerId, appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }) {
        const query = gql`
                mutation (
                    $appointmentSurveyAnswerId: ID
                    $appointmentDecisionTreeId: ID
                    $surveyId: ID
                    $surveyAnswerId: ID
                    $createdById: ID
                ) {
                    updateAppointmentSurveyAnswer(
                    input: {
                        id: $appointmentSurveyAnswerId
                        appointmentDecisionTree: $appointmentDecisionTreeId
                        survey: $surveyId
                        surveyAnswer: $surveyAnswerId
                        createdBy: $createdById
                    }
                    ) {
                    appointmentSurveyAnswer {
                        survey {
                        id
                        }
                        surveyAnswer {
                        id
                        }
                        appointmentDecisionTree {
                        id
                        }
                    }
                    }
                }`

        const variables = { appointmentSurveyAnswerId, appointmentDecisionTreeId, surveyId, surveyAnswerId, createdById }

        return await this.$graphql.default.request(query, variables);
    },

    async createAppointmentSurveyQuestionResponse({ }, { appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }) {
        const query = gql`
                mutation (
                        $appointmentSurveyId: ID
                        $surveyQuestionId: ID
                        $questionResponseId: ID
                        $responseValue: String
                        $createdById: ID
                        $updatedByID: ID
                    ) 
                    {
                    createAppointmentSurveyQuestionResponse(
                        input: {
                        appointmentSurvey: $appointmentSurveyId
                        surveyQuestion: $surveyQuestionId
                        questionResponse: $questionResponseId
                        responseValue: $responseValue
                        createdBy: $createdById
                        updatedBy: $updatedByID
                        }
                    ) {
                        appointmentSurveyQuestionResponse {
                            id
                        }
                    }
                }`

        const variables = { appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }
                console.log(variables);
        return await this.$graphql.default.request(query, variables);
    },

    async updateAppointmentSurveyQuestionResponse({ }, {appointmentSurveyQuestionResponseId, appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }) {
        const query = gql`
                mutation (
                    $appointmentSurveyQuestionResponseId: ID
                    $appointmentSurveyId: ID
                    $surveyQuestionId: ID
                    $questionResponseId: ID
                    $responseValue: String
                    $createdById: ID
                    $updatedByID: ID
                    ) {
                    updateAppointmentSurveyQuestionResponse(
                        input: {
                        id: $appointmentSurveyQuestionResponseId
                        appointmentSurvey: $appointmentSurveyId
                        surveyQuestion: $surveyQuestionId
                        questionResponse: $questionResponseId
                        responseValue: $responseValue
                        createdBy: $createdById
                        updatedBy: $updatedByID
                        }
                    ) {
                        appointmentSurveyQuestionResponse {
                        id
                        }
                    }
                }`

        const variables = { appointmentSurveyQuestionResponseId, appointmentSurveyId, surveyQuestionId, questionResponseId,responseValue, createdById, updatedByID }

        return await this.$graphql.default.request(query, variables);
    },

    async deleteAppointmentSurveyQuestionResponse({ }, { appointmentSurveyQuestionResponseId }) {
        const query = gql`
                mutation ($appointmentSurveyQuestionResponseId: ID) {
                    deleteAppointmentSurveyQuestionResponse(id:$appointmentSurveyQuestionResponseId) {
                        appointmentSurveyQuestionResponse {
                        id
                        }
                    }
                }`

        const variables = { appointmentSurveyQuestionResponseId }

        return await this.$graphql.default.request(query, variables);
    },

    async surveryQuestionFinished({ }, { appointmentSurveyId, surveyId, appointmentId, isFinished=true, createdById, updatedById }) {
        const mutation = gql`
              mutation (
                $appointmentSurveyId: ID
                $surveyId: ID
                $appointmentId: ID
                $isFinished: Boolean
                $createdById: ID
                $updatedById: ID
              ) {
                updateAppointmentSurvey(
                  input: {
                    id: $appointmentSurveyId
                    appointment: $appointmentId
                    survey: $surveyId
                    isFinished:$isFinished
                    createdBy: $createdById
                    updatedBy: $updatedById
                  }
                ) {
                  appointmentSurvey {
                    id
                  }
                }
              }`
        const variables = {appointmentSurveyId, surveyId, appointmentId, isFinished, createdById, updatedById }
        return await this.$graphql.default.request(mutation, variables)
      },

    async downloadPatientSurveyAnswer({ }, { patientId, appointmentId }) {
        const query = gql`
         query ($userId:Float){
          
        }
        `
        const variables = { patientId, appointmentId }

        return await this.$graphql.default.request(query, variables);
    },
};
