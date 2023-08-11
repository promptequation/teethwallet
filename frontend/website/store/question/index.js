import { gql } from 'nuxt-graphql-request'
import Vue from 'vue'


const SET_QUESTIONS = 'SET_QUESTIONS'
const SET_QUESTION_ANSWER = 'SET_QUESTION_ANSWER'
const SET_SUB_QUESTION_ANSWER = 'SET_SUB_QUESTION_ANSWER'
const SET_USER_QUESTION_ANSWERS = 'SET_USER_QUESTION_ANSWERS'
const SET_CLEAR_QUESTION_ANSWER = 'SET_CLEAR_QUESTION_ANSWER'
const SET_QUESTION_HOVE_TRUE = 'SET_QUESTION_HOVE_TRUE'
const SET_QUESTION_HOVE_FALSE = 'SET_QUESTION_HOVE_FALSE'
const SET_UPDATE_QUESTION_INFOMATION = 'SET_UPDATE_QUESTION_INFOMATION'
const SET_UPDATE_CHECK_BOX_TYPE_QUESTION_ANSWERS = 'SET_UPDATE_CHECK_BOX_TYPE_QUESTION_ANSWERS'
const SET_UPDATE_QUESTION_DISPLAY = 'SET_UPDATE_QUESTION_DISPLAY'


const findQuestion = (rootQuestions, neqQuestion) => {
  return rootQuestions.find(item => {
    return item.node.referenceId === Number(neqQuestion.node.id)
  })
}
const getQuestionResponse = (allQuestions, newQuestionResponse, eachQuestion) => {
  let questionResponse = []
  newQuestionResponse.forEach(qR => {
    let newQuestion = null
    if (qR.node.referenceId) {
      newQuestion = findQuestion(allQuestions, eachQuestion)
    }

    let qr = null
    if (newQuestion?.node.questionresponseSet.edges.length > 0) {
      qr = getQuestionResponse(allQuestions, newQuestion?.node.questionresponseSet.edges, newQuestion)
    }

    questionResponse.push({
      id: qR.node.id,
      title: qR.node.title,
      referenceId: qR.node.referenceId,
      question: {
        id: newQuestion?.node.id,
        title: newQuestion?.node.title,
        elementType: newQuestion?.node.elementType,
        referenceId: newQuestion?.node.referenceId,
        questionResponse: qr
      }
    })
  })

  return questionResponse

}


const findYesAndDontKnowQuestion = (question) => {
  const newResponse = question.questionResponse.find(response => {
    return Number(response.id) === Number(question.userAnswer.answer)
  })
  if (newResponse) {
    if (newResponse.title === "I Don't know" || newResponse.title === "Yes") {
      return true
    } else {
      return false
    }
  }
  return false
}

export const state = () => ({
  questions: [],
  answers: []
})

export const getters = {
  getQuestions(state) {
    // return state.questions.map(item => {
    //   let questionResponse = getQuestionResponse(state.questions, item.node.questionresponseSet.edges, item)
    //   item.questionResponse = questionResponse

    //   return {
    //     id: item.node.id,
    //     title: item.node.title,
    //     elementType: item.node.elementType,
    //     referenceId: item.node.referenceId,
    //     questionResponse
    //   }
    // })
    return []
  },
  getAllOfQuestions(state) {
    return state.questions.map(item => {
      return item
    })
  },
  getOnlyYesAndDontKnowQuestions(state) {
    // return state.questions.filter(question => {
    //   return findYesAndDontKnowQuestion(question)
    // })
    const questions = []

    state.questions.forEach(question => {
      if (question.elementType.name === 'RADIO_BUTTON') {
        // console.log(question.questionResponse);
        const selectedResponse = question.questionResponse.find(response => {
          return Number(response.id) === Number(question.userAnswer.answer)
        })

        if (selectedResponse && (selectedResponse.title === "I Don't know" || selectedResponse.title === "Yes")) {
          questions.push(question)
          if (Number(question.referenceId) === 1002 && Number(selectedResponse.referenceId) === 1) {
            const relatedQuestion = state.questions.find(newQ => {
              return Number(newQ.referenceId) === 1003

            })
            questions.push(relatedQuestion)
          } else if (Number(question.referenceId) === 1006 && Number(selectedResponse.referenceId) === 1) {
            const relatedQuestion = state.questions.find(newQ => {
              return Number(newQ.referenceId) === 1007
            })
            questions.push(relatedQuestion)

            const selectedResponse = relatedQuestion.questionResponse.find(response => {
              return Number(response.id) === Number(relatedQuestion.userAnswer.answer)
            })

            if (selectedResponse && Number(selectedResponse.referenceId) === 1) {
              const relatedQuestion = state.questions.find(newQ => {
                return Number(newQ.referenceId) === 1008

              })
              questions.push(relatedQuestion)

            } else if (selectedResponse && Number(selectedResponse.referenceId) === 5) {
              const relatedQuestion = state.questions.find(newQ => {
                return Number(newQ.referenceId) === 1009
              })
              questions.push(relatedQuestion)
            }
          } else if (Number(question.referenceId) === 1010 && Number(selectedResponse.referenceId) === 1) {
            const relatedQuestion = state.questions.find(newQ => {
              return Number(newQ.referenceId) === 1011

            })
            questions.push(relatedQuestion)


            const selectedResponse = relatedQuestion.questionResponse.find(response => {
              return Number(response.referenceId) === Number(3)
            })

            if (selectedResponse && relatedQuestion.userAnswer.answer.includes(selectedResponse.id)) {
              const relatedQuestion = state.questions.find(newQ => {
                return Number(newQ.referenceId) === 1012

              })
              questions.push(relatedQuestion)
            }

          } else if (Number(question.referenceId) === 1018 && Number(selectedResponse.referenceId) === 1) {
            const relatedQuestion = state.questions.find(newQ => {
              return Number(newQ.referenceId) === 1019

            })
            questions.push(relatedQuestion)

            const selectedResponse = relatedQuestion.questionResponse.find(response => {
              return Number(response.referenceId) === Number(10)
            })

            if (selectedResponse && relatedQuestion.userAnswer.answer.includes(selectedResponse.id)) {
              const relatedQuestion = state.questions.find(newQ => {
                return Number(newQ.referenceId) === 1020

              })
              questions.push(relatedQuestion)
            }
          }
        }
      }
    })


    let newQuestions = questions.map(question => {
      let answer;
      if (question.elementType.name === 'RADIO_BUTTON') {
        const selectedResponse = question.questionResponse.find(response => {
          return Number(response.id) === Number(question.userAnswer.answer)
        })
        if (selectedResponse) {
          answer = selectedResponse.title
        }

      } else if (question.elementType.name === 'CHECK_BOX') {
        let ans = []
        question.userAnswer.answer.forEach(answer => {
          const selectedResponse = question.questionResponse.find(response => {
            return Number(response.id) === Number(answer)
          })
          if (selectedResponse) {
            ans.push(selectedResponse.title)
          }
        })

        answer = ans

      } else if (question.elementType.name === 'TEXT_BOX') {
        answer = question.userAnswer.answer
      }

      return {
        id: question.id,
        title: question.title,
        type: question.elementType.name,
        answer,
      }
    })

    return newQuestions

  },
  getAllAnswers(state) {
    return state.answers.map(answer => {
      return answer.node
    })
  }
}

export const mutations = {
  [SET_QUESTIONS](state, payload) {
    state.questions = payload
  },

  [SET_USER_QUESTION_ANSWERS](state, payload) {
    state.answers = payload
  },



  [SET_QUESTION_ANSWER](state, payload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.node.id === payload.node.question.id) {
        return question
      }
    })
    let question = state.questions[questionIndex]
    question.node.userAnswer = payload
    Vue.set(state.questions, questionIndex, question)
  },

  [SET_SUB_QUESTION_ANSWER](state, payload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.node.id === payload.node.question.subQuestion.id) {
        return question
      }
    })
    let question = state.questions[questionIndex]
    console.log(question);

    // question.node.userAnswer = payload
    // Vue.set(state.questions, questionIndex, question)
  },

  [SET_CLEAR_QUESTION_ANSWER](state, questionPaload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.id === questionPaload.id) {
        return question
      }
    })
    state.questions[questionIndex] = questionPaload
    state.questions[questionIndex].userAnswer = {
      diseasesId: null,
      diseaseanswerId: null,
      answer: null,
    }

    if (state.questions[questionIndex].elementType.name === 'CHECK_BOX') {
      state.questions[questionIndex].userAnswer.diseaseanswerId = []
      state.questions[questionIndex].userAnswer.answer = []
    }

    Vue.set(state.questions, questionIndex, state.questions[questionIndex])
  },

  [SET_QUESTION_HOVE_TRUE](state, questionPaload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.id === questionPaload.id) {
        return question
      }
    })
    if (questionIndex > -1) {
      let question = state.questions[questionIndex] = questionPaload
      question.hover = true
      Vue.set(state.questions, questionIndex, question)
    }
  },

  [SET_QUESTION_HOVE_FALSE](state, questionPaload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.id === questionPaload.id) {
        return question
      }
    })
    if (questionIndex > -1) {
      let question = state.questions[questionIndex] = questionPaload
      question.hover = false
      Vue.set(state.questions, questionIndex, question)
    }
  },
  [SET_UPDATE_QUESTION_INFOMATION](state, questionPaload) {
    const questionIndex = state.questions.findIndex(question => {
      if (question.id === questionPaload.id) {
        return question
      }
    })
    if (questionIndex > -1) {
      let question = state.questions[questionIndex] = questionPaload
      Vue.set(state.questions, questionIndex, question)
    }
  },
  [SET_UPDATE_CHECK_BOX_TYPE_QUESTION_ANSWERS](state, { checkBoxValue, question }) {
    const questionIndex = state.questions.findIndex(item => {
      if (item.id === question.id) {
        return item
      }
    })
    if (questionIndex > -1) {
      let newQuestion = state.questions[questionIndex]
      if (newQuestion.userAnswer.answer.indexOf(checkBoxValue) != -1) {
        const newList = newQuestion.userAnswer.answer.filter(data => data != checkBoxValue);
        newQuestion.userAnswer.answer = newList
      } else {
        newQuestion.userAnswer.answer.push(checkBoxValue)
      }

      Vue.set(state.questions, questionIndex, newQuestion)
    }
  },
  [SET_UPDATE_QUESTION_DISPLAY](state, { displayQuestion, display }) {
    const questionIndex = state.questions.findIndex(item => {
      if (item.id === displayQuestion.id) {
        return item
      }
    })
    if (questionIndex > -1) {
      let newQuestion = displayQuestion
      newQuestion.display = display
      Vue.set(state.questions, questionIndex, newQuestion)
    }
  },
}

export const actions = {
  async fetchQuestions({ }, { userId, langId }) {
    const query = gql`
         query ($userId:Float, $langId:Float){
          questions{
            edges {
              node {
                id
                title
                referenceId
                isConditionalQuestion
                elementType {
                  id
                  name
                }
                questionlangSet(lang_Id: $langId){
                  edges{
                    node{
                        title
                    }
                  }
                }
                serialNo
                questionresponseSet {
                  edges {
                    node {
                      id
                      title
                      referenceId
                      serialNo
                      questionresponselangSet(lang_Id: $langId){
                        edges{
                          node{
                            title
                          }
                        }
                      }
                    }
                  }
                }
                diseaseSet(user_Id:$userId){
                  edges{
                    node{
                      id
                      user{
                        id
                      }
                      question{
                        id
                      }
                      diseaseanswerSet{
                        edges{
                          node{
                            id
                            value
                            questionResponse{
                              id
                              title
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

    const variables = { userId, langId }

    return await this.$graphql.default.request(query, variables);
  },
  async createQuestionAnswer({ }, { questionId, userId, textInput, createdById, updatedById }) {
    const query = gql`
              mutation (
                $questionId: Int
                $userId: ID
                $textInput: String
                $createdById: ID
                $updatedById: ID
              ) {
                createQuestionAnswer(
                  input: {
                    textInput: $textInput
                    questionId: $questionId
                    user: $userId
                    createdBy: $createdById
                    updatedBy: $updatedById
                  }
                ) {
                  questionAnswer {
                    id
                  }
                }
              }`

    const variables = { questionId, userId, textInput, createdById, updatedById }

    return await this.$graphql.default.request(query, variables);
  },

  async updateQuestionAnswer({ }, { id, questionId, userId, textInput, updatedById }) {
    const query = gql`
             mutation (
                $id: ID
                $questionId: Int
                $userId: ID
                $textInput: String
                $updatedById: ID
              ) {
                updateQuestionAnswer(
                  input: {
                    id: $id
                    textInput: $textInput
                    questionId: $questionId
                    user: $userId
                    updatedBy: $updatedById
                  }
                ) {
                  questionAnswer {
                    id
                  }
                }
              }
              `

    const variables = { id, questionId, userId, textInput, updatedById }

    return await this.$graphql.default.request(query, variables);
  },

  async fetchQuestionAnswerByUser({ }, { userId, textInput }) {
    const query = gql`
          query ($userId:Float, $textInput:String) {
            questionAnswers(user_Id: $userId, textInput: $textInput) {
              edges {
                node {
                  id
                  questionId
                  textInput
                  user {
                    id
                    username
                  }
                }
              }
            }
          }`

    const variables = { userId, textInput }

    return await this.$graphql.default.request(query, variables);
  },

  async createQuestionDiseases({ }, { questionId, userId, createdById, updatedById }) {
    const query = gql`
          mutation ($userId: ID, $questionId: ID, $createdById: ID, $updatedById: ID) {
            createDisease(
              input: {
                question: $questionId
                user: $userId
                createdBy: $createdById
                updatedBy: $updatedById
              }
            ) {
              disease {
                id
              }
            }
          }
          `

    const variables = { questionId, userId, createdById, updatedById }

    return await this.$graphql.default.request(query, variables);
  },

  async createQuestionDiseasesAnswer({ }, { diseasesId, questionResponseId, inputValue, createdById, updatedById }) {
    const mutation = gql`
         mutation (
            $diseasesId: ID
            $questionResponseId: ID
            $inputValue: String
            $createdById: ID
            $updatedById: ID
          ) {
            createDiseaseAnswer(
              input: {
                disease: $diseasesId
                questionResponse: $questionResponseId
                value: $inputValue
                createdBy: $createdById
                updatedBy: $updatedById
              }
            ) {
              diseaseAnswer {
                id
                disease {
                  id
                }
              }
            }
          }`

    const variables = { diseasesId, questionResponseId, inputValue, createdById, updatedById }

    return await this.$graphql.default.request(mutation, variables);
  },

  async updateQuestionDiseasesAnswer({ }, { diseaseAnswerId, diseasesId, questionResponseId, inputValue, updatedById }) {
    const mutation = gql`
         mutation (
          $diseaseAnswerId: ID
          $diseasesId: ID
          $inputValue: String
          $questionResponseId: ID
          $updatedById: ID
        ) {
          updateDiseaseAnswer(
            input: {
              id: $diseaseAnswerId
              value: $inputValue
              disease: $diseasesId
              questionResponse: $questionResponseId
              updatedBy: $updatedById
            }
          ) {
            diseaseAnswer {
              id
              value
            }
          }
        }`

    const variables = { diseaseAnswerId, diseasesId, questionResponseId, inputValue, updatedById }

    return await this.$graphql.default.request(mutation, variables);
  },

  async deleteQuestionDiseases({ }, { diseasesId }) {
    const mutation = gql`
         mutation ($diseasesId: ID) {
          deleteDisease(id: $diseasesId) {
            disease {
              id
            }
          }
        }`

    const variables = { diseasesId }

    return await this.$graphql.default.request(mutation, variables);
  },
  async deleteUserAllQuestionDiseases({ }, { userId }) {
    const mutation = gql`
          mutation ($userId: ID) {
            deleteUserDisease(id: $userId) {
              disease {
                id
              }
            }
          }
          `
    const variables = { userId }

    return await this.$graphql.default.request(mutation, variables);
  },
  async deleteQuestionDiseasesAnswer({ }, { diseaseAnswerId }) {
    const mutation = gql`
          mutation($diseaseAnswerId:ID){
            deleteDiseaseAnswer(id:$diseaseAnswerId)
            {
              diseaseAnswer {
                id
              }
            }
          }
          `
    const variables = { diseaseAnswerId }

    return await this.$graphql.default.request(mutation, variables);
  },
}
