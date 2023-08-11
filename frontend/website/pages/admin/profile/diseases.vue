<template>
  <ValidationObserver v-slot="{ handleSubmit }">
    <v-form @submit.prevent="handleSubmit(handleUpdate)">
      <v-row>
        <v-col>
          <v-card>
            <v-card-title class="pa-6">
              <v-row>
                <v-col cols="auto" class="mr-auto">
                  <v-icon large left> mdi-account </v-icon>

                  <span class="text-h6 blue-grey--text text--darken-3">{{ $t('diseases.Associated Diseases') }}</span>
                </v-col>
                <v-col cols="auto">
                  <ActionButton :deleteBtn="false" :resetBtn="true" @click:discard="dicardAll" @click:reset="resetAll">
                  </ActionButton>
                </v-col>
              </v-row>
            </v-card-title>

            <v-card-text>
              <v-container fluid>
                <v-row>
                  <v-col>
                    <h1 class="text">{{ $t('diseases.Do you suffer from') }}</h1>
                  </v-col>
                </v-row>
                <v-row>
                  <template v-for="(question, index) in getAllOfQuestions">
                    <v-col v-if="!question.isConditionalQuestion || question.display" cols="12" md="6" lg="4"
                      :key="index">
                      <v-list-item class="pa-0" @mouseover="showCloseBtn(question)" @mouseleave="hideCloseBtn(question)">
                        <v-list-item-content class="pa-0">
                          <h3 class="tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500 tw-py-1 px-1">
                            {{ question.title }}
                          </h3>
                        </v-list-item-content>

                        <v-list-item-action>
                          <v-btn icon @click="resetQuestion(question)">
                            <v-icon :class="question.hover ? '' : 'd-none'" color="grey lighten-1">mdi-close</v-icon>
                          </v-btn>
                        </v-list-item-action>
                      </v-list-item>


                      <v-radio-group class="sub-radio mt-0" v-model="question.userAnswer.answer"
                        @change="updateRadioTypeQuestionAnswer(question)"
                        v-if="question.elementType.name === 'RADIO_BUTTON'" row>
                        <v-radio name="index" color="green" :key="responseIndex" :value="response.id"
                          :label="response.title" v-for="(response, responseIndex) in question.questionResponse">
                        </v-radio>
                      </v-radio-group>

                      <div v-if="question.elementType.name === 'CHECK_BOX'">
                        <v-checkbox v-model="question.userAnswer.answer" color="green"
                          @change="updateCheckboxQuestionAnswer(response.id, question)" hide-details :key="responseIndex"
                          :value="response.id" :label="response.title"
                          v-for="(response, responseIndex) in question.questionResponse">
                        </v-checkbox>
                      </div>

                      <v-row>
                        <v-col cols="10">
                          <v-text-field v-if="question.elementType.name === 'TEXT_BOX'"
                            @keyup="updateInputTypeQuestionAnswer(question)" v-model="question.userAnswer.answer" dense
                            placeholder="Drag Name" class="m-0">
                          </v-text-field>
                        </v-col>
                      </v-row>
                    </v-col>
                  </template>

                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
    <ConfirmationDialog ref="confirmation" />
  </ValidationObserver>
</template>


<script lang="ts">
import { onMounted, useStore, computed, useContext, ref, reactive } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import ActionButton from "~/components/buttons/ActionButton.vue";
import useQuestions from '~/../composables/useQuestions'
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";

export default {
  name: "Diseases",
  layout: "admin",
  middleware: "patient",
  components: { ValidationObserver, ValidationProvider, ActionButton, ConfirmationDialog },
  setup({ }) {
    const { $t } = useNuxtTranslator()
    const { app } = useContext();
    const { $toast } = app;
    const { getters, commit } = useStore()
    const {
      fetchQuestions,
      createQuestionDiseases,
      createQuestionDiseasesAnswer,
      updateQuestionDiseasesAnswer,
      deleteQuestionDiseases,
      deleteUserAllQuestionDiseases,
      deleteQuestionDiseasesAnswer,
    } = useQuestions()
    const authUser = computed(() => getters["auth/getUserProfile"])
    const confirmation = ref()
    const getAllOfQuestions = computed(() => JSON.parse(JSON.stringify(getters["question/getAllOfQuestions"])))

    const storeUserAnswer = async (question: any) => {
      const { createDisease } = await createQuestionDiseases({
        questionId: Number(question.id),
        userId: Number(authUser.value?.id),
        createdById: Number(authUser.value?.id),
        updatedById: Number(authUser.value?.id)
      })

      if (createDisease && createDisease.disease?.id) {
        if (question.elementType.name === 'CHECK_BOX') {
          let questionResponseId: string | number;
          for (questionResponseId of question.userAnswer.answer) {
            await createQuestionDiseasesAnswer({
              diseasesId: Number(createDisease.disease?.id),
              questionResponseId,
              inputValue: null,
              createdById: Number(authUser.value?.id),
              updatedById: Number(authUser.value?.id)
            })
          }
        } else {
          const questionResponseId = question.elementType.name === 'RADIO_BUTTON' ? question.userAnswer.answer : null
          const inputValue = question.elementType.name === 'TEXT_BOX' ? question.userAnswer.answer : null

          await createQuestionDiseasesAnswer({
            diseasesId: Number(createDisease.disease?.id),
            questionResponseId,
            inputValue,
            createdById: Number(authUser.value?.id),
            updatedById: Number(authUser.value?.id)
          })
        }
      }
    }

    const updateUserAnswer = async (question: any) => {
      if (question.elementType.name === 'CHECK_BOX') {
        await deleteQuestionDiseases({ diseasesId: Number(question.userAnswer.diseasesId) })
        await storeUserAnswer(question)
      } else {
        const questionResponseId = question.elementType.name === 'RADIO_BUTTON' ? question.userAnswer.answer : null
        const inputValue = question.elementType.name === 'TEXT_BOX' ? question.userAnswer.answer : null

        await updateQuestionDiseasesAnswer({
          diseaseAnswerId: Number(question.userAnswer.diseaseanswerId),
          diseasesId: Number(question.userAnswer.diseasesId),
          questionResponseId,
          inputValue,
          updatedById: Number(authUser.value?.id)
        })
      }
    }

    const createOrUpdateAllOfQuestion = async (question: any) => {
      if (question.elementType.name === 'CHECK_BOX') {
        if (question.userAnswer.answer.length > 0) {
          if (question.userAnswer.diseasesId) {
            await updateUserAnswer(question)
          }
          else {
            await storeUserAnswer(question)
          }
        }
      } else {
        if (question.userAnswer.answer) {
          if (question.userAnswer.diseasesId && question.userAnswer.diseaseanswerId) {
            await updateUserAnswer(question)
          }
          else {
            await storeUserAnswer(question)
          }
        }
      }
    }

    const handleUpdate = async () => {
      commit('SET_OVERLAY', true)
      commit('SET_LOADING', true)

      let question: any;
      for (question of getAllOfQuestions.value) {
        await createOrUpdateAllOfQuestion(question)
      }
      await fetchQuestions({
        userId: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      })
      reRenderAllOfQuestion()
      commit('SET_OVERLAY', false)
      commit('SET_LOADING', false)
      $toast.success(`${ $t('toastMessage.Answer Successfully updated') }`)
    };

    const dicardAll = async () => {
      confirmation.value
        .open(`${$t("dialogue.Alert")}`, `${$t("dialogue.Do you want to retrieve the previous answer?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            await fetchQuestions({
              userId: Number(authUser.value?.id),
              langId: authUser.value?.lang?.id
            })
            reRenderAllOfQuestion()
            $toast.success(`${ $t('toastMessage.Successfully retrieve the previous answer') }`)
          }
          return false
        });
    };

    const resetAll = async () => {
      confirmation.value
        .open(`${$t("dialogue.Alert")}`, `${$t("dialogue.Do you want to reset everything?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            commit('SET_OVERLAY', true)
            commit('SET_LOADING', true)
            await deleteUserAllQuestionDiseases({
              userId: Number(authUser.value?.id)
            })
            await fetchQuestions({
              userId: Number(authUser.value?.id),
              langId: authUser.value?.lang?.id
            })
            reRenderAllOfQuestion()
            commit('SET_OVERLAY', false)
            commit('SET_LOADING', false)
            $toast.success(`${ $t('toastMessage.Answers to all questions have been cleared') }`)
          }
          return false
        });
    };

    const resetQuestion = async (question: any) => {
      confirmation.value
        .open(`${$t("dialogue.Alert")}`, `${$t("dialogue.Do you want to reset?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            commit('SET_OVERLAY', true)
            commit('SET_LOADING', true)
            if (question.userAnswer.diseasesId) {
              await deleteQuestionDiseases({ diseasesId: Number(question.userAnswer.diseasesId) })
            }
            commit('question/SET_CLEAR_QUESTION_ANSWER', question)
            commit('SET_OVERLAY', false)
            commit('SET_LOADING', false)
            $toast.success(`${ $t('toastMessage.The question answer cleared') }`)
          }
          return false
        });
    };

    const showCloseBtn = (question: any) => {
      commit('question/SET_QUESTION_HOVE_TRUE', question)
    }

    const hideCloseBtn = (question: any) => {
      commit('question/SET_QUESTION_HOVE_FALSE', question)
    }


    const displayQuestions = (display: boolean, targetAbleQuestionRefId: string | number) => {
      const displayQuestion = getAllOfQuestions.value.find((newQ: any) => {
        return Number(newQ.referenceId) === targetAbleQuestionRefId
      })

      if (displayQuestion && displayQuestion.id) {
        commit('question/SET_UPDATE_QUESTION_DISPLAY', { displayQuestion, display })
      }
    }

    const displayConditionalQuestion = (selectedResponse: any, question: any) => {
      const display = Number(selectedResponse.referenceId) === 1 ? true : false

      if (Number(question.referenceId) === 1002) {
        displayQuestions(display, 1003)

      } else if (Number(question.referenceId) === 1006) {

        displayQuestions(display, 1007)

        if (!display) {
          displayQuestions(display, 1008)
          displayQuestions(display, 1009)
        }

      } else if (Number(question.referenceId) === 1007) {
        if (Number(selectedResponse.referenceId) === 1) {
          displayQuestions(display, 1008)
          displayQuestions(false, 1009)

        } else if (Number(selectedResponse.referenceId) === 5) {
          displayQuestions(true, 1009)
          displayQuestions(false, 1008)

        } else {
          displayQuestions(false, 1008)
          displayQuestions(false, 1009)
        }

      } else if (Number(question.referenceId) === 1010) {
        displayQuestions(display, 1011)

      } else if (Number(question.referenceId) === 1011) {
        const display = question.userAnswer.answer.includes(selectedResponse.id)

        if (selectedResponse.referenceId === 3) {
          displayQuestions(display, 1012)
        }
      } else if (Number(question.referenceId) === 1018) {
        displayQuestions(display, 1019)

        if (!display) {
          displayQuestions(display, 1020)
        }
      } else if (Number(question.referenceId) === 1019) {
        const display = question.userAnswer.answer.includes(selectedResponse.id)

        if (selectedResponse.referenceId === 10) {
          displayQuestions(display, 1020)
        }
      }


    }

    const updateRadioTypeQuestionAnswer = (question: any) => {

      const selectedResponse = question.questionResponse.find((item: any) => {
        return Number(item.id) === Number(question.userAnswer.answer)
      })

      if (selectedResponse) {
        displayConditionalQuestion(selectedResponse, question)
      }

      commit('question/SET_UPDATE_QUESTION_INFOMATION', question)
    }


    const updateInputTypeQuestionAnswer = (question: any) => {
      commit('question/SET_UPDATE_QUESTION_INFOMATION', question)
    }

    const updateCheckboxQuestionAnswer = (checkBoxValue: any, question: any) => {
      const selectedResponse = question.questionResponse.find((item: any) => {
        return Number(item.id) === Number(checkBoxValue)
      })

      if (selectedResponse) {
        displayConditionalQuestion(selectedResponse, question)
      }

      commit('question/SET_UPDATE_CHECK_BOX_TYPE_QUESTION_ANSWERS', { checkBoxValue, question })
    }

    const reRenderAllOfQuestion = () => {
      getAllOfQuestions.value.forEach((question: any) => {

        const selectedResponse = question.questionResponse.find((item: any) => {
          return Number(item.id) === Number(question.userAnswer.answer)
        })

        if (question.elementType.name === 'RADIO_BUTTON' && selectedResponse) {

          const display = Number(selectedResponse.referenceId) === 1 ? true : false


          if (Number(question.referenceId) === 1002) {
            displayQuestions(display, 1003)

          } else if (Number(question.referenceId) === 1006) {
            displayQuestions(display, 1007)

            if (!display) {
              displayQuestions(display, 1008)
              displayQuestions(display, 1009)
            }

          } else if (Number(question.referenceId) === 1007) {
            if (Number(selectedResponse.referenceId) === 1) {

              const displayQuestion = getAllOfQuestions.value.find((newQ: any) => {
                return Number(newQ.referenceId) === 1006
              })
              if (displayQuestion) {
                const selectedResponse = displayQuestion.questionResponse.find((item: any) => {
                  return Number(item.id) === Number(displayQuestion.userAnswer.answer)
                })
                if (selectedResponse && selectedResponse.referenceId === 2) {
                  displayQuestions(false, 1008)
                } else {
                  displayQuestions(true, 1008)
                }
              }
              displayQuestions(false, 1009)

            } else if (Number(selectedResponse.referenceId) === 5) {
              const displayQuestion = getAllOfQuestions.value.find((newQ: any) => {
                return Number(newQ.referenceId) === 1006
              })
              if (displayQuestion) {
                const selectedResponse = displayQuestion.questionResponse.find((item: any) => {
                  return Number(item.id) === Number(displayQuestion.userAnswer.answer)
                })
                if (selectedResponse && selectedResponse.referenceId === 2) {
                  displayQuestions(false, 1009)
                } else {
                  displayQuestions(true, 1009)
                }
              }

              displayQuestions(false, 1008)

            } else {
              displayQuestions(false, 1008)
              displayQuestions(false, 1009)
            }

          } else if (Number(question.referenceId) === 1010) {
            displayQuestions(display, 1011)

          } else if (Number(question.referenceId) === 1018) {
            displayQuestions(display, 1019)

            if (!display) {
              displayQuestions(display, 1020)
            }
          }
        }

        if (question.elementType.name === 'CHECK_BOX') {
          if (Number(question.referenceId) === 1019) {
            const selectedResponse = question.questionResponse.find((item: any) => {
              return Number(item.referenceId) === Number(10)
            })

            if (selectedResponse && selectedResponse.referenceId === 10) {
              const display = question.userAnswer.answer.includes(selectedResponse.id)
              displayQuestions(display, 1020)
            }
          } else if (Number(question.referenceId) === 1011) {
            const selectedResponse = question.questionResponse.find((item: any) => {
              return Number(item.referenceId) === Number(3)
            })

            if (selectedResponse && selectedResponse.referenceId === 3) {
              const display = question.userAnswer.answer.includes(selectedResponse.id)
              displayQuestions(display, 1012)
            }

          }
        }


      });
    }

    onMounted(async () => {
      await fetchQuestions({
        userId: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      })
      reRenderAllOfQuestion()
    })

    return {
      handleUpdate,
      dicardAll,
      resetAll,
      getAllOfQuestions,
      resetQuestion,
      confirmation,
      showCloseBtn,
      hideCloseBtn,
      updateRadioTypeQuestionAnswer,
      updateInputTypeQuestionAnswer,
      updateCheckboxQuestionAnswer,
    };
  },
};
</script>
<style lang="scss" scoped>
::v-deep {
  .sub-radio {
    .v-input__control {
      .v-input__slot {
        .v-input--radio-group__input {
          align-items: flex-start;
        }
      }
    }
  }
}
</style>
