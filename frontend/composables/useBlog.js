import { useStore, useFetch } from '@nuxtjs/composition-api'

const useBlog = () => {
    const store = useStore()

    const fetchAllPages = () => {
        useFetch(async () => {
            if (store.state.website.pages?.length > 0) return

            await store.dispatch('website/fetchAllPages')
        })
    }

    const fetchPage = async (id) => {
        const response = await store.dispatch('website/fetchPage', id)

        return response
    }

    return { fetchAllPages, fetchPage }

}

export default useBlog;