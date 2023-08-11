
import { useStore } from "@nuxtjs/composition-api";


const useQuestions = () => {

    const { dispatch, commit } = useStore()

    const fetchQuestions = async ({ userId, langId }) => {
        try {
            const { questions } = await dispatch('question/fetchQuestions', { userId, langId })
            const newQuestions = questions.edges.map(item => {
                let questionResponse = []
                item.node.questionresponseSet.edges.forEach(qR => {
                    let title = qR.node.title
                    if (qR.node.questionresponselangSet && qR.node.questionresponselangSet.edges?.length > 0) {
                        title = qR.node.questionresponselangSet.edges[0]?.node?.title
                    }
                    questionResponse.push({
                        id: qR.node.id,
                        title,
                        referenceId: qR.node.referenceId,
                    })
                })

                const userAnswerUpdated = {
                    diseasesId: "",
                    diseaseanswerId: "",
                    answer: "",
                }

                if (item.node.elementType && item.node.elementType.name === 'CHECK_BOX') {
                    userAnswerUpdated.diseaseanswerId = []
                    userAnswerUpdated.answer = []
                }


                if (item.node.diseaseSet && item.node.diseaseSet.edges.length > 0) {
                    const disease = item.node.diseaseSet.edges[0].node
                    userAnswerUpdated.diseasesId = disease.id
                    if (disease.diseaseanswerSet && disease.diseaseanswerSet.edges.length > 0) {

                        if (item.node.elementType && item.node.elementType.name === 'CHECK_BOX') {
                            disease.diseaseanswerSet.edges.forEach(item => {
                                userAnswerUpdated.diseaseanswerId.push(item.node.id)
                                userAnswerUpdated.answer.push(item.node.questionResponse.id)
                            })
                        } else {
                            const diseaseAnswer = disease.diseaseanswerSet.edges[0].node
                            userAnswerUpdated.diseaseanswerId = diseaseAnswer.id
                            userAnswerUpdated.answer = diseaseAnswer.value ? diseaseAnswer.value : diseaseAnswer.questionResponse.id
                        }
                    }
                }

                let title = item.node.title
                if (item.node.questionlangSet && item.node.questionlangSet.edges?.length > 0) {
                    title = item.node.questionlangSet.edges[0]?.node?.title
                }

                return {
                    id: item.node.id,
                    title,
                    elementType: item.node.elementType,
                    referenceId: item.node.referenceId,
                    isConditionalQuestion: item.node.isConditionalQuestion,
                    serialNo: item.node.serialNo,
                    questionResponse,
                    userAnswer: userAnswerUpdated,
                    hover: false,
                    display: false,
                }
            })
            commit('question/SET_QUESTIONS', JSON.parse(JSON.stringify(newQuestions)))
        } catch (error) {
            console.log(error);
        }
    }

    const fetchQuestionAnswerByUser = async ({ userId, textInput }) => {
        try {
            const { questionAnswers } = await dispatch('question/fetchQuestionAnswerByUser', { userId, textInput })
            commit('question/SET_USER_QUESTION_ANSWERS', questionAnswers.edges)
        } catch (error) {
            console.log(error);
        }
    }

    const createQuestionAnswer = async ({ questionId, userId, textInput, createdById, updatedById }) => {
        try {
            return await dispatch('question/createQuestionAnswer', { questionId, userId, textInput, createdById, updatedById })
        } catch (error) {
            console.log(error);
        }
    }

    const updateQuestionAnswer = async ({ id, questionId, userId, textInput, updatedById }) => {
        try {
            return await dispatch('question/updateQuestionAnswer', { id, questionId, userId, textInput, updatedById })
        } catch (error) {
            console.log(error);
        }
    }

    const createQuestionDiseases = async ({ questionId, userId, createdById, updatedById }) => {
        try {
            return await dispatch('question/createQuestionDiseases', { questionId, userId, createdById, updatedById })
        } catch (error) {
            console.log(error);
        }
    }
    const createQuestionDiseasesAnswer = async ({ diseasesId, questionResponseId, inputValue, createdById, updatedById }) => {
        try {
            return await dispatch('question/createQuestionDiseasesAnswer', { diseasesId, questionResponseId, inputValue, createdById, updatedById })
        } catch (error) {
            console.log(error);
        }
    }
    const updateQuestionDiseasesAnswer = async ({ diseaseAnswerId, diseasesId, questionResponseId, inputValue, updatedById }) => {
        try {
            return await dispatch('question/updateQuestionDiseasesAnswer', { diseaseAnswerId, diseasesId, questionResponseId, inputValue, updatedById })
        } catch (error) {
            console.log(error);
        }
    }
    const deleteQuestionDiseases = async ({ diseasesId }) => {
        try {
            return await dispatch('question/deleteQuestionDiseases', { diseasesId })
        } catch (error) {
            console.log(error);
        }
    }
    const deleteUserAllQuestionDiseases = async ({ userId }) => {
        try {
            return await dispatch('question/deleteUserAllQuestionDiseases', { userId })
        } catch (error) {
            console.log(error);
        }
    }
    const deleteQuestionDiseasesAnswer = async ({ diseaseAnswerId }) => {
        try {
            return await dispatch('question/deleteQuestionDiseasesAnswer', { diseaseAnswerId })
        } catch (error) {
            console.log(error);
        }
    }

    return {
        fetchQuestions,
        fetchQuestionAnswerByUser,
        createQuestionAnswer,
        updateQuestionAnswer,
        createQuestionDiseases,
        createQuestionDiseasesAnswer,
        updateQuestionDiseasesAnswer,
        deleteQuestionDiseases,
        deleteUserAllQuestionDiseases,
        deleteQuestionDiseasesAnswer,
    }
}

export default useQuestions
