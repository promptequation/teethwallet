import { useContext } from "@nuxtjs/composition-api";

const useNuxtTranslator = () => {
    const { app } = useContext();
    const { i18n } = app;
    const $t = (module) => {
        return i18n.t(module);
    };
    return {
        $t
    }
};

export default useNuxtTranslator;
