import { getField, updateField } from 'vuex-map-fields';
import { gql } from 'nuxt-graphql-request';
import { SET_PAGES } from './types'

export const state = () => ({
    pages: [],
    errors: []
})

export const getters = {
    getField,
    getPageById: (state) => (id) => {
        return state.pages.find(page => page.id === id)
    }
}

export const mutations = {
    updateField,
    [SET_PAGES] (state, payload) {
        state.pages = payload
    }
}

export const actions = {
    async fetchAllPages ({ commit, dispatch }) {
        const query = gql`query {
            allPages {
                id
                title
                subtitle
                body
                image
                pubDate
                changeDate
                slug
                author{
                   name
                   image
                }
                tags {
                    id
                    name
                }
            }
        }`;

        const { allPages } = await this.$graphql.default.request(query)
            .catch(error => console.log(error));

        commit(SET_PAGES, allPages);
    },

    async fetchPage ({ commit }, id) {
        const query = gql`query($id: Int){
              page(pageId: $id) {
                id
                title
                subtitle
                body
                image
                pubDate
                changeDate
                slug
                author{
                   name
                   image
                }
            }
        }`;

        const variables = { id };

        const { page } = await this.$graphql.default.request(query, variables)
            .catch(error => console.log(error));

        return page || {}
    },
    showError ({ state }, msg) {
        state.errors.push(msg)

    }
}
