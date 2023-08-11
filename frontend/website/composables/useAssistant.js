import { useStore, computed, reactive } from "@nuxtjs/composition-api";
import { provideToast, useToast } from "vue-toastification/composition";

const useAssistant = () => {
    provideToast({
        timeout: 4000,
        position: "bottom-center"
    });
    const toast = useToast();

    const { dispatch, getters } = useStore();

    const assistants = reactive({ items: [], total: 0 });

    const userProfile = getters["auth/getUserProfile"];
    const companyId = computed(() =>
        parseInt(userProfile?.doctor?.company?.id)
    );

    const fetchAssistantsByCompanyId = async options => {
        const filter = {
            companyId: companyId.value,
            first: parseInt(options.itemsPerPage),
            offset: options.page * options.itemsPerPage - options.itemsPerPage,
            name: options.name
        };

        const { allAssistants } = await dispatch(
            "assistant/fetchAssistantsByCompanyId",
            filter
        );
        assistants.items = allAssistants.edges.map(assistant => assistant.node);
        assistants.total = allAssistants.totalCount;
    };

    const sendAssistantEmailInvitation = async email => {
        try {
            const { sendEmailInvitation } = await dispatch(
                "assistant/sendEmailInvitation",
                email
            );
            toast.info(sendEmailInvitation.response || `${$t('toastMessage.Something is wrong!')}`);
        } catch (error) {
            toast.error(
                error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`
            );
        }
    };

    return {
        fetchAssistantsByCompanyId,
        assistants,
        sendAssistantEmailInvitation
    };
};

export default useAssistant;
