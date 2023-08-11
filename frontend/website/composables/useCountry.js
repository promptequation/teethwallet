import { useStore, reactive } from "@nuxtjs/composition-api";


const useCountry = () => {
    const { dispatch } = useStore();

    const countries = reactive({items: []});

    const signupFieldsData = reactive({countryList: [], multiLanguage: [], nationalityList: []});
    
    const searchCountries = async () => {
      countries.items = await dispatch("country/fetchCountryList");
    };

    const getSignupFieldsData = async () => {
      const result = await dispatch("country/fetchSignupFieldsData");
      const {countryList, multiLanguage, nationalityList} = result;
      signupFieldsData.countryList = countryList;
      signupFieldsData.multiLanguage = multiLanguage;
      signupFieldsData.nationalityList = nationalityList;
    }
  
    return {
      searchCountries,
      getSignupFieldsData,
      signupFieldsData,
      countries,
    };
};
export default useCountry;

  