<template>
    <v-sheet min-height="70vh">
        <NewHero />
    </v-sheet>
</template>

<script>
import NewHero from "~/components/sections/NewHero.vue";
export default {
    name: "BaseView",
    components: {
        NewHero
    }
};
</script>
