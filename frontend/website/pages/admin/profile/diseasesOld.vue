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

                  <span class="text-h6 blue-grey--text text--darken-3">Associated Diseases</span>
                </v-col>
                <v-col cols="auto">
                  <ActionButton :deleteBtn="false" @click:discard="dicardAll"></ActionButton>
                </v-col>
              </v-row>
            </v-card-title>

            <v-card-text>
              <v-container fluid>
                <v-row>
                  <v-col>
                    <h2>Do you suffer from</h2>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Heart Problems?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.heartProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Kidney diseases?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.kidneyProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class=" tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500">
                      Are you taking any medication?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.medicationProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-text-field v-if="questionsModelObject.medicationProblem.textInput == 'Y'"
                        v-model="questionsModelObject.medicationInputField.textInput" dense hide-details
                        placeholder="Drag Name" class="pt-0 m-0"></v-text-field>
                    </v-radio-group>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">Diabetes?</h3>
                    <v-radio-group v-model="questionsModelObject.diabetesProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Hypertension?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.hypertensionProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class=" tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500">
                      Do you have any infectious diseases?
                    </h3>
                    <v-radio-group class="sub-radio" v-model="questionsModelObject.infectiousProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <div v-if="questionsModelObject.infectiousProblem.textInput == 'Y'">
                        <v-radio-group hide-details class="pt-0 mt-0"
                          v-model="questionsModelObject.infectiousOptions.textInput">
                          <v-radio color="green" value="hepatitis" label="Hepatitis"></v-radio>
                          <v-radio color="green" value="tuberculosis" label="Tuberculosis"></v-radio>
                          <v-radio color="green" value="hiv " label="HIV"></v-radio>
                          <v-radio color="green" value="syphilis" label="Syphilis"></v-radio>
                          <v-radio color="green" value="o" label="Others"></v-radio>
                        </v-radio-group>
                        <v-text-field v-if="questionsModelObject.infectiousOptions.textInput == 'hepatitis'"
                          v-model="questionsModelObject.infectiousHepatitisInputField.textInput" dense
                          placeholder="Drag Name" class="m-0">
                        </v-text-field>
                        <v-text-field v-if="questionsModelObject.infectiousOptions.textInput == 'o'"
                          v-model="questionsModelObject.infectiousOthersInputField.textInput" dense
                          placeholder="Drag Name" class="m-0">
                        </v-text-field>
                      </div>
                    </v-radio-group>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Blood diseases?
                    </h3>
                    <v-radio-group class="sub-radio" v-model="questionsModelObject.bloodProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <div v-if="questionsModelObject.bloodProblem.textInput == 'Y'">
                        <v-radio-group hide-details class="pt-0 mt-0"
                          v-model="questionsModelObject.bloodOptions.textInput">
                          <v-radio color="green" value="anemia" label="Anemia"></v-radio>
                          <v-radio color="green" value="hemophilia" label="Hemophilia"></v-radio>
                          <v-radio color="green" value="o" label="Others"></v-radio>
                        </v-radio-group>
                        <v-text-field v-if="questionsModelObject.bloodOptions.textInput === 'o'"
                          v-model="questionsModelObject.bloodOtherInputField.textInput" dense
                          placeholder="Bload Diseases Name" class="m-0">
                        </v-text-field>
                      </div>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Liver diseases?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.liverProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Stomach diseases?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.stomachProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <v-radio color="green" value="D" label="I don't know"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Are you a smoker?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.smokerProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class=" tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500">
                      Do you have epilepsy?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.epilepsyProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                    </v-radio-group>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class="tw-border-2 tw-border-gray-800">
                      Are you, or have you been under radio/chemotherapy
                      treatment?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.chemotherapyProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class=" tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500">
                      Are you allergic to any medicine or medical device?
                    </h3>
                    <v-radio-group class="sub-radio" v-model="questionsModelObject.allergicDrugProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                      <div v-if="questionsModelObject.allergicDrugProblem.textInput == 'Y'">
                        <v-radio-group hide-details class="pt-0 mt-0"
                          v-model="questionsModelObject.allergicDrugOptions.textInput">
                          <v-radio color="green" value="aspirin" label="Aspirin"></v-radio>
                          <v-radio color="green" value="sulfamides" label="Sulfamides"></v-radio>
                          <v-radio color="green" value="anesthetics" label="Anesthetics"></v-radio>
                          <v-radio color="green" value="penicillins" label="Penicillins"></v-radio>
                          <v-radio color="green" value="nichel" label="Nichel"></v-radio>
                          <v-radio color="green" value="chromium-cobalt" label="Chromium/Cobalt"></v-radio>
                          <v-radio color="green" value="acrylic" label="Acrylic"></v-radio>
                          <v-radio color="green" value="latex" label="Latex"></v-radio>
                          <v-radio color="green" value="others" label="Others"></v-radio>
                        </v-radio-group>
                        <v-text-field v-if="questionsModelObject.allergicDrugOptions.textInput == 'others'"
                          v-model="questionsModelObject.allergicDrugOtherOptionInputField.textInput" dense
                          placeholder="Drag Name" class="m-0">
                        </v-text-field>
                      </div>
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12" md="6" lg="4">
                    <h3 class=" tw-text-white tw-border-2 tw-border-gray-800 tw-bg-blue-500">
                      Are there diseases in the family such as cancer, diabetes,
                      cardiac and allergies?
                    </h3>
                    <v-radio-group v-model="questionsModelObject.familyDiseasesProblem.textInput" row>
                      <v-radio color="green" value="Y" label="Yes"></v-radio>
                      <v-radio color="green" value="N" label="No"></v-radio>
                    </v-radio-group>
                  </v-col>
                </v-row>


              </v-container>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </ValidationObserver>
</template>


<script>
import { reactive, onMounted, useStore, computed, watch, useContext } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import ActionButton from "~/components/buttons/ActionButton.vue";
import useQuestions from '@common-composables/useQuestions'

export default {
  name: "Diseases",
  layout: "admin",
  middleware: "patient",
  components: { ValidationObserver, ValidationProvider, ActionButton },
  setup({ }, { root }) {
    const { $t } = useNuxtTranslator()
    const { app } = useContext();
    const { $toast } = app;

    const { getters, commit } = useStore()
    const { fetchQuestionAnswerByUser, createQuestionAnswer, updateQuestionAnswer } = useQuestions()
    const authUser = computed(() => getters["auth/getUserProfile"])

    const getAllAnswers = computed(() => getters["question/getAllAnswers"])

    const questionsModelObject = reactive({
      heartProblem: {
        id: null,
        questionId: 1,
        textInput: ""
      },
      kidneyProblem: {
        id: null,
        questionId: 2,
        textInput: ""
      },
      medicationProblem: {
        id: null,
        questionId: 3,
        textInput: ""
      },
      medicationInputField: {
        id: null,
        questionId: 4,
        textInput: ""
      },
      diabetesProblem: {
        id: null,
        questionId: 5,
        textInput: ""
      },
      hypertensionProblem: {
        id: null,
        questionId: 6,
        textInput: ""
      },
      infectiousProblem: {
        id: null,
        questionId: 7,
        textInput: ""
      },
      infectiousOptions: {
        id: null,
        questionId: 8,
        textInput: ""
      },
      infectiousHepatitisInputField: {
        id: null,
        questionId: 9,
        textInput: ""
      },
      infectiousOthersInputField: {
        id: null,
        questionId: 10,
        textInput: ""
      },
      bloodProblem: {
        id: null,
        questionId: 11,
        textInput: ""
      },
      bloodOptions: {
        id: null,
        questionId: 12,
        textInput: ""
      },
      bloodOtherInputField: {
        id: null,
        questionId: 13,
        textInput: ""
      },
      liverProblem: {
        id: null,
        questionId: 14,
        textInput: ""
      },
      stomachProblem: {
        id: null,
        questionId: 15,
        textInput: ""
      },
      smokerProblem: {
        id: null,
        questionId: 16,
        textInput: ""
      },
      epilepsyProblem: {
        id: null,
        questionId: 17,
        textInput: ""
      },
      chemotherapyProblem: {
        id: null,
        questionId: 18,
        textInput: ""
      },
      allergicDrugProblem: {
        id: null,
        questionId: 19,
        textInput: ""
      },
      allergicDrugOptions: {
        id: null,
        questionId: 20,
        textInput: ""
      },
      allergicDrugOtherOptionInputField: {
        id: null,
        questionId: 21,
        textInput: ""
      },
      familyDiseasesProblem: {
        id: null,
        questionId: 22,
        textInput: ""
      },
    })

    watch(getAllAnswers, () => {
      for (let eachPropertity in questionsModelObject) {
        if (Object.prototype.hasOwnProperty.call(questionsModelObject, eachPropertity)) {
          if (questionsModelObject[eachPropertity].questionId) {
            const answer = getAllAnswers.value.find(newAnswer => {
              return Number(newAnswer.questionId) === Number(questionsModelObject[eachPropertity].questionId)
            })
            if (answer) {
              questionsModelObject[eachPropertity].id = answer.id
              questionsModelObject[eachPropertity].questionId = answer.questionId
              questionsModelObject[eachPropertity].textInput = answer.textInput
            }
          }
        }
      }
    })

    const handleUpdate = async () => {
      commit('SET_OVERLAY', true)
      commit('SET_LOADING', true)

      for (let eachPropertity in questionsModelObject) {
        if (Object.prototype.hasOwnProperty.call(questionsModelObject, eachPropertity)) {
          const answer = questionsModelObject[eachPropertity]
          if (answer.id) {
            await updateQuestionAnswer({
              id: Number(answer.id),
              questionId: answer.questionId,
              userId: Number(authUser.value?.id),
              textInput: answer.textInput,
              updatedById: Number(authUser.value?.id)
            })
          } else {
            await createQuestionAnswer({
              questionId: Number(answer.questionId),
              userId: Number(authUser.value?.id),
              textInput: answer.textInput,
              createdById: Number(authUser.value?.id),
              updatedById: Number(authUser.value?.id)
            })
          }
        }
      }

      $toast.success(`${ $t('toastMessage.Diseases Successfully updated!') }`);
      await fetchQuestionAnswerByUser({
        userId: Number(authUser.value?.id)
      })

      commit('SET_OVERLAY', false)
      commit('SET_LOADING', false)
    };

    const dicardAll = async () => {
      await fetchQuestionAnswerByUser({
        userId: Number(authUser.value?.id)
      })
    };

    onMounted(async () => {
      await fetchQuestionAnswerByUser({
        userId: Number(authUser.value?.id)
      })
    })

    return {
      handleUpdate,
      dicardAll,
      questionsModelObject
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
