<template>
  <!-- <v-card class="tw-h-full">
    <v-card-title class="text-h6 font-weight-regular justify-space-between">
      <span>{{ currentQuestion.name }}</span>
      <v-avatar color="primary lighten-2" class="subheading white--text" size="24"
        v-text="questions ? questions.length : 0">
      </v-avatar>
    </v-card-title>

    <v-window v-model="stepIndex">
      <v-window-item :value="index" v-for="(question, index) in questions">
        <v-card-text>
          <v-radio-group hide-details row class="pt-0 mt-0">
            <v-radio color="green" value="hepatitis" label="Yes"></v-radio>
            <v-radio color="green" value="tuberculosis" label="No"></v-radio>
          </v-radio-group>
        </v-card-text>
      </v-window-item>
    </v-window>
    <v-divider></v-divider>

    <v-card-actions>
      <v-btn :disabled="stepIndex === 0" text @click="stepIndex--">
        Back
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn :disabled="stepIndex === questions.length - 1" color="primary" depressed @click="stepIndex++">
        Next
      </v-btn>
    </v-card-actions>
  </v-card> -->

  <v-card>
    <v-stepper v-model="stepIndex" height="350px">
      <v-stepper-items>
        <v-stepper-content
          :step="index"
          v-for="(question, index) in questions"
          :key="index"
        >
          <!-- <validation-observer ref="errorReset" v-slot="{ handleSubmit }">
            <v-form
              @submit.prevent="handleSubmit(submitQuestion(question, index))"
            > -->
          <v-card class="mb-12" height="200px">
            <v-card-text>
              <v-card-title class="tw-pl-0">
                {{ question.title }}
              </v-card-title>

              <!-- <validation-provider
                    v-slot="{ errors, valid, dirty }"
                    rules="required"
                    vid="patient"
                  > -->
              <!-- :error-messages="errors"
                      :success="valid && dirty" -->
              <v-radio-group
                name="patient"
                hide-details
                row
                class="pt-0 mt-0"
                v-if="question.questionType === 'RADIO_BUTTON'"
                v-model="question.userAnswer.answer"
              >
                <v-radio
                  :name="option.answer"
                  color="green"
                  :value="option.id"
                  :label="option.answer"
                  :key="index"
                  v-for="(option, index) in question.questionResponses"
                ></v-radio>
              </v-radio-group>
              <!-- </validation-provider> -->
              <v-row v-if="question.questionType === 'MULTIPLE_SELECTION'">
                <v-col
                  cols="12"
                  sm="2"
                  md="2"
                  :key="index"
                  v-for="(option, index) in question.questionResponses"
                >
                  <v-checkbox
                     class="align-"
                    :key="index"
                    v-model="question.userAnswer.answer"
                    :value="option.id"
                    :label="option.answer"
                    color="green"
                    @change="
                      updateMultiSelectOptionQuestionAnswers(
                        question,
                        option.id
                      )
                    "
                    hide-details
                  ></v-checkbox>
                </v-col>
              </v-row>
              <!-- <validation-provider
                    v-slot="{ errors, valid, dirty }"
                    rules="required"
                    vid="patient"
                  > -->
              <!-- :error-messages="errors"
                      :success="valid && dirty" -->
              <v-text-field
                v-if="question.questionType === 'TEXT_FIELD'"
                label="Outlined"
                outlined
                dense
                v-model="question.userAnswer.answer"
              ></v-text-field>
              <!-- </validation-provider> -->
            </v-card-text>
          </v-card>
          <div class="d-flex tw-justify-between">
            <v-btn
              text
              @click="previousQuestion(question, index)"
              :disabled="stepIndex === 0"
            >
              Back
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
              :disabled="nextDisable"
              @click="submitQuestion(question, Number(index))"
            >
              Next
            </v-btn>
          </div>
          <!-- </v-form>
          </validation-observer> -->
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-card>
</template>

<script lang="ts">
import {
  ref,
  computed,
  useRoute,
  useRouter,
  onMounted,
  useStore,
  useContext,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import userSurvey from "~/../composables/useSurvey";

interface defineQuestionType {
  id: number;
  title?: string;
  xmlQuestionId?: string | number;
  isConditionalQuestion?: boolean;
  questionType?: string;
  parentQuestion?: string;
  serialNo: number;
  questionResponses?: any;
  userAnswer?: any;
}

interface selectedAnswerType {
  id?: number;
  answer: any;
  xmlQuestionId: number;
  tragetXmlQuestionIds: number[];
}

export default {
  name: "QuestionSurvey",
  layout: "admin",
  middleware: "doctor",
  setup({}) {
    const { app } = useContext();
    const { $t } = useNuxtTranslator()
    const { $toast } = app;
    const route = useRoute();
    const router = useRouter();
    const { getters, commit } = useStore();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const {
      fetchAppointmentSurveys,
      fetchSurveyWithQuestions,
      createAppointmentSurveyAnswer,
      createAppointmentSurveyQuestionResponse,
      updateAppointmentSurveyQuestionResponse,
      deleteAppointmentSurveyQuestionResponse,
      surveryQuestionFinished,
      errors,
    } = userSurvey();

    const errorReset = ref();
    const selectedAnswer = ref<any>({});
    const selectMulipleOptions = ref<any[]>([]);
    const stepIndex = ref<number>(999999999999);
    const nextDisable = ref(false);
    const appointmentId = route.value.query?.appointmentId;

    const questions = computed(() => {
      return JSON.parse(JSON.stringify(getters["survey/questions"]));
    });
    const allQuestions = computed(() => {
      return getters["survey/allQuestions"];
    });
    const appointmentSurvey = computed(
      () => getters["survey/appointmentSurvey"]
    );
    // const currentQuestion = computed(() => {
    //   return questions.value[stepIndex.value];
    // });

    const findNextQuestions = async (
      targetIds: number[],
      currentQuestion: defineQuestionType,
      nextIndexNumber: number | string
    ) => {
      const newQs = allQuestions?.value.filter(
        (question: defineQuestionType) => {
          return targetIds.includes(Number(question.xmlQuestionId));
        }
      );

      const sortQuestions = newQs.sort(function (
        q1: defineQuestionType,
        q2: defineQuestionType
      ) {
        return q1.serialNo - q2.serialNo;
      });

      await commit("survey/PUSH_TARGET_QUESTION", {
        currentQuestion,
        newQs: sortQuestions,
        nextIndexNumber,
      });
    };

    const jupmNextRootQuestion = async (nextIndexNumber: number) => {
      if (questions.value.length > nextIndexNumber) {
        stepIndex.value++;
      } else {
        await surveryQuestionFinished({
          appointmentSurveyId: Number(appointmentSurvey.value?.id),
          surveyId: Number(appointmentSurvey.value?.survey.id),
          appointmentId: Number(appointmentSurvey.value?.appointment.id),
          isFinished: true,
          createdById: Number(authUser.value?.id),
          updatedById: Number(authUser.value?.id),
        });
        $toast.success(`${ $t('toastMessage.Your survey is successfully finished') }`);
        router.push("/admin/appointments");
      }
    };

    const storeQuestionResponse = async (
      question: defineQuestionType,
      selectedAnswer: selectedAnswerType
    ) => {
      let response = null;
      if (question.userAnswer.appointmentSurveyQuestionResponseId) {
        const res = await updateAppointmentSurveyQuestionResponse({
          appointmentSurveyQuestionResponseId: Number(
            question.userAnswer.appointmentSurveyQuestionResponseId
          ),
          appointmentSurveyId: Number(appointmentSurvey.value?.id),
          surveyQuestionId: Number(question.id),
          questionResponseId: Number(selectedAnswer.id),
          responseValue: "",
          createdById: Number(authUser.value?.id),
          updatedByID: Number(authUser.value?.id),
        });
        response =
          res.updateAppointmentSurveyQuestionResponse
            ?.appointmentSurveyQuestionResponse.id;
      } else {
        const res = await createAppointmentSurveyQuestionResponse({
          appointmentSurveyId: Number(appointmentSurvey.value?.id),
          surveyQuestionId: Number(question.id),
          questionResponseId: Number(selectedAnswer.id),
          responseValue: "",
          createdById: Number(authUser.value?.id),
          updatedByID: Number(authUser.value?.id),
        });
        response =
          res.createAppointmentSurveyQuestionResponse
            ?.appointmentSurveyQuestionResponse.id;
      }
      return response;
    };

    const submitQuestion = async (
      question: defineQuestionType,
      index: number
    ) => {
      removeExistingQuestions(question, index);
      const nextIndexNumber: number = Number(index) + 1;

      if (question.userAnswer.answer || question.questionType === "LABEL") {
        if (question.questionType === "RADIO_BUTTON") {
          const answer = question.questionResponses.find(
            (answer: selectedAnswerType) => {
              return Number(answer.id) === Number(question.userAnswer.answer);
            }
          );
          let appointmentSurveyQuestionResponseId = await storeQuestionResponse(
            question,
            answer
          );
          if (appointmentSurveyQuestionResponseId) {
            question.userAnswer.appointmentSurveyQuestionResponseId =
              appointmentSurveyQuestionResponseId;
            commit("survey/UPDATE_QUESTION_ANSWER", question);
            if (answer?.tragetXmlQuestionIds.length > 0) {
              await findNextQuestions(
                answer.tragetXmlQuestionIds,
                question,
                nextIndexNumber
              );
              stepIndex.value++;
              selectedAnswer.value = {};
            } else {
              jupmNextRootQuestion(nextIndexNumber);
            }
          } else {
            alert("error");
          }
        } else if (question.questionType === "MULTIPLE_SELECTION") {
          const surveyAnswers = question.questionResponses.filter(
            (answer: selectedAnswerType) => {
              return question.userAnswer.answer.includes(answer.id);
            }
          );
          let targetXmlIds: number[] = [];
          surveyAnswers.forEach((selectedAnswer: selectedAnswerType) => {
            targetXmlIds = targetXmlIds.concat(
              selectedAnswer.tragetXmlQuestionIds
            );
          });
          if (
            question.userAnswer.appointmentSurveyQuestionResponseId.length > 0
          ) {
            let id;
            for (id of question.userAnswer
              .appointmentSurveyQuestionResponseId) {
              await deleteAppointmentSurveyQuestionResponse({
                appointmentSurveyQuestionResponseId: id,
              });
            }
          }
          let newAQRIds: number[] = [];
          let newQRIds: number[] = [];
          let questionResponse;
          for (questionResponse of surveyAnswers) {
            const res = await createAppointmentSurveyQuestionResponse({
              appointmentSurveyId: Number(appointmentSurvey.value?.id),
              surveyQuestionId: Number(question.id),
              questionResponseId: Number(questionResponse.id),
              responseValue: "",
              createdById: Number(authUser.value?.id),
              updatedByID: Number(authUser.value?.id),
            });
            newQRIds.push(questionResponse.id);
            if (
              res.createAppointmentSurveyQuestionResponse
                ?.appointmentSurveyQuestionResponse.id
            ) {
              newAQRIds.push(
                res.createAppointmentSurveyQuestionResponse
                  ?.appointmentSurveyQuestionResponse.id
              );
            }
          }
          question.userAnswer.appointmentSurveyQuestionResponseId = newAQRIds;
          question.userAnswer.answer = newQRIds;
          commit("survey/UPDATE_QUESTION_ANSWER", question);
          if (targetXmlIds.length > 0) {
            await findNextQuestions(targetXmlIds, question, nextIndexNumber);
            selectMulipleOptions.value = [];
          } else {
            jupmNextRootQuestion(nextIndexNumber);
            selectMulipleOptions.value = [];
          }
        } else if (question.questionType === "TEXT_FIELD") {
          let appointmentSurveyQuestionResponseId = null;
          // create
          if (question.userAnswer.appointmentSurveyQuestionResponseId) {
            // update
            const res = await updateAppointmentSurveyQuestionResponse({
              appointmentSurveyQuestionResponseId: Number(
                question.userAnswer.appointmentSurveyQuestionResponseId
              ),
              appointmentSurveyId: Number(appointmentSurvey.value?.id),
              surveyQuestionId: Number(question.id),
              questionResponseId: "",
              responseValue: question.userAnswer.answer,
              createdById: Number(authUser.value?.id),
              updatedByID: Number(authUser.value?.id),
            });
            appointmentSurveyQuestionResponseId =
              res.updateAppointmentSurveyQuestionResponse
                ?.appointmentSurveyQuestionResponse.id;
          } else {
            const res = await createAppointmentSurveyQuestionResponse({
              appointmentSurveyId: Number(appointmentSurvey.value?.id),
              surveyQuestionId: Number(question.id),
              questionResponseId: "",
              responseValue: question.userAnswer.answer,
              createdById: Number(authUser.value?.id),
              updatedByID: Number(authUser.value?.id),
            });
            appointmentSurveyQuestionResponseId =
              res.createAppointmentSurveyQuestionResponse
                ?.appointmentSurveyQuestionResponse.id;
          }

          question.userAnswer.appointmentSurveyQuestionResponseId =
            appointmentSurveyQuestionResponseId;
          commit("survey/UPDATE_QUESTION_ANSWER", question);
          jupmNextRootQuestion(nextIndexNumber);
        } else {
          jupmNextRootQuestion(nextIndexNumber);
        }
      } else {
        $toast.error(
          `Please ${
            question.questionType === "TEXT_FIELD" ? "type" : "select"
          } your survey`
        );
      }
    };

    // const questionAnswerSelect = (
    //   question: defineQuestionType,
    //   $event: any
    // ) => {
    //   // selectedAnswer.value = question.questionResponses.find((answer) => {
    //   //   return answer.answer === $event;
    //   // });
    //   selectedAnswer.value = $event;
    //   // console.log(question);
    //   // console.log($event);
    // };

    const updateMultiSelectOptionQuestionAnswers = (
      question: defineQuestionType,
      id: number
    ) => {
      commit("survey/UPDATE_MULTIPLE_QUESTION_ANSWER", { question, id });
    };

    const previousQuestion = (question: defineQuestionType, index: number) => {
      removeExistingQuestions(question, index);
      stepIndex.value--;
      nextDisable.value = false;
    };

    const removeExistingQuestions = (
      question: defineQuestionType,
      index: number
    ) => {
      let tragetXmlQuestionIds: number[] = [];
      question.questionResponses.forEach((answer: selectedAnswerType) => {
        tragetXmlQuestionIds = tragetXmlQuestionIds.concat(
          answer.tragetXmlQuestionIds
        );
      });
      commit("survey/REMOVE_QUESTIONS", { tragetXmlQuestionIds, index });
    };

    onMounted(async () => {
      await fetchAppointmentSurveys({
        appointmentId,
      });

      if (appointmentSurvey.value && appointmentSurvey.value.isFinished) {
        $toast.warning(`${ $t('toastMessage.Appointment Successfully Deleted!') }`);
        router.push("/admin/appointments");
      } else {
        await fetchSurveyWithQuestions({
          surveyId: Number(appointmentSurvey.value?.survey.id),
          appointmentSurveyId: Number(appointmentSurvey.value?.id),
        });
      }

      stepIndex.value = 0;
    });

    return {
      stepIndex,
      nextDisable,
      questions,
      submitQuestion,
      selectMulipleOptions,
      previousQuestion,
      updateMultiSelectOptionQuestionAnswers,
      errorReset,
    };
  },
};
</script>

<style>
</style>
