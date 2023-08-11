import { useContext } from '@nuxtjs/composition-api'

const useDate = () => {
    const { $dayjs } = useContext()

    const convertTimestampToFormat = (value, format) => {
        return $dayjs(value).format(format)
    }

    return {
        convertTimestampToFormat
    }
}

export default useDate;