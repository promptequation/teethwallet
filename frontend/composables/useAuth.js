//injecting until vuetify use vue3 (mobile quasar using vue3)
import { reactive, ref, useStore, useRouter } from '@nuxtjs/composition-api';
import { useToast, provideToast } from "vue-toastification/composition";
import useNuxtTranslator from "~/../composables/useNuxti18n";

const useAuth = () => {
    const { $t } = useNuxtTranslator()
    const store = useStore()
    const router = useRouter()
    const toast = useToast()
    const redirect = {
        login: "/admin"
    };
    const step = ref('login')
    const registerStep = ref('step1')

    const formInitialState = {
        username: '',
        email: '',
        password: '',
        birthdate: '',
        address: '',
        country: null,
        nationality: null,
        language: null,
        isCaregiver: false
    }
    const form = reactive({ ...formInitialState })

    const resetForm = () => Object.assign(form, formInitialState)

    const signUpObjectConversions = (formData) => {
        return formData;
    }

    const signUp = async (userData) => {
        try {
            userData = Object.assign({}, signUpObjectConversions(userData));
            userData.nationality = parseInt(userData.nationality, 10);
            await store.dispatch('auth/signUp', userData)
            toast.success(`${$t('toastMessage.Success! We sent an email to finish registration')}`)
            step.value = 'login'
            // resetForm()
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }

    const signIn = async (userData) => {
        try {
            const { tokenAuth } = await store.dispatch('auth/signIn', userData)
            await store.dispatch('auth/setUserProfile', tokenAuth.token)
            if (tokenAuth.user.isFirstLogin === false) {
                router.push(redirect.login)
            } else {
                router.push("/admin/profile/diseases");
            }
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }
    const emailVerify = async ({ token, uuid }) => {
        try {
            await store.dispatch('auth/emailVerify', { token, uuid })
        } catch (error) {
            toast.error(error.response?.errors[0]?.message || `${$t('toastMessage.Something is wrong!')}`)
        }
    }

    const logout = async () => {
        await store.dispatch('auth/logout')
        router.push("/start")
    }

    return { signUp, signIn, resetForm, logout, form, step, registerStep, emailVerify }
}

export default useAuth