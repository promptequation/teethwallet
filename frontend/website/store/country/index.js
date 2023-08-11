import { getField, updateField } from "vuex-map-fields";
import { gql } from "nuxt-graphql-request";

const SET_COUNTRIES = "SET_COUNTRIES"

export const state = () => ({
  countries: []
});

export const getters = {
  getField,
  countries(state) {
    return state.countries
  }
};

export const mutations = {
  updateField,
  [SET_COUNTRIES](state, payload) {
    state.countries = payload
  }
};

export const actions = {

  async fetchCountryList() {
    const query = gql`
      query {
        countryList {
          code
          name
        }
      }
    `;



    const result = await this.$graphql.default.request(query);
    return result;
  },
  async fetchSignupFieldsData() {
    const query = gql`
      query {
        countryList {
          code
          name
        }
        multiLanguage {
          id
          name
          code
        }
        nationalityList {
          code
          name
        }
      }
    `;



    const result = await this.$graphql.default.request(query);
    let { countryList, nationalityList, multiLanguage } = result;
    return { countryList, nationalityList, multiLanguage };
  }
};
