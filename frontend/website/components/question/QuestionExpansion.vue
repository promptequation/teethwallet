<template>
    <div>
        <template v-for="(question, index) in getOnlyYesAndDontKnowQuestions">
            <!-- <v-expansion-panels :key="index">
                <v-expansion-panel>
                    <v-expansion-panel-header>
                        {{ question.title }}
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-radio-group class="sub-radio" v-model="question.userAnswer.answer"
                            v-if="question.elementType.name === 'RADIO_BUTTON'" row>

                            <v-radio name="index" color="green" :key="responseIndex" :value="response.id"
                                :label="response.title" v-for="(response, responseIndex) in question.questionResponse">
                            </v-radio>
                        </v-radio-group>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels> -->

            <v-list-item class="pa-0 tw-border-t tw-border-x  tw-border-gray-500 px-2">
                <v-list-item-content class="pa-0">
                    {{ question.title }}
                </v-list-item-content>
                <v-list-item-action>
                    <template v-if="question.type === 'CHECK_BOX'">
                        <span v-for="answer in question.answer">{{ answer }}</span>
                    </template>
                    <template v-else="">
                        {{ question.answer }}
                    </template>
                </v-list-item-action>
            </v-list-item>

        </template>
        <p v-if="getOnlyYesAndDontKnowQuestions.length === 0">{{ $t('singleAppointment.No question found') }}</p>
    </div>
</template>



<script lang="ts">
import { onMounted, useStore, computed, watch, useContext } from "@nuxtjs/composition-api";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import ActionButton from "~/components/buttons/ActionButton.vue";
import useQuestions from '~/../composables/useQuestions'

export default {
    name: "QuestionExpansion",
    components: { ValidationObserver, ValidationProvider, ActionButton },
    props: {
        userId: {
            type: String,
            default: null
        }
    },
    setup(props: any) {
        const { app } = useContext();
        const { getters } = useStore()
        const authUser = computed(() => getters["auth/getUserProfile"])

        const { fetchQuestions } = useQuestions()

        const getOnlyYesAndDontKnowQuestions = computed(() => getters["question/getOnlyYesAndDontKnowQuestions"])

        watch(() => props.userId, async (userid: string) => {
            if (userid) {
                await fetchQuestions({
                    userId: Number(userid),
                    langId: authUser.value?.lang?.id
                })
            }
        })

        onMounted(async () => {
            if (props.userId) {
                await fetchQuestions({
                    userId: Number(props.userId),
                    langId: authUser.value?.lang?.id
                })
            }
        })

        return {
            getOnlyYesAndDontKnowQuestions,
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

