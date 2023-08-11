<template>
    <v-app>
        <website-app-bar />
        <v-main class="landing-page-background tw-flex tw-items-center">
            <nuxt class="landing-page-background" />
        </v-main>
        <website-footer />
    </v-app>
</template>

<script>
import Vue from "vue";
import upperFirst from "lodash/upperFirst";
import camelCase from "lodash/camelCase";
import AOS from "aos";
import "aos/dist/aos.css";

const requireComponent = require.context("@components/base", true, /\.vue$/);

for (const file of requireComponent.keys()) {
    const componentConfig = requireComponent(file);
    const name = file
        .replace(/index.js/, "")
        .replace(/^\.\//, "")
        .replace(/\.\w+$/, "");
    const componentName = upperFirst(camelCase(name));

    Vue.component(
        `Base${componentName}`,
        componentConfig.default || componentConfig
    );
}

export default {
    name: "WebsiteLayout",
    components: {
        WebsiteAppBar: () => import("@components/layout/website/WebsiteAppBar"),
        WebsiteFooter: () => import("@components/layout/website/WebsiteFooter")
    },
    mounted() {
        AOS.init();
    }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@200;300;400;500;600;700;800;900;1000&display=swap");

* {
    font-family: "Nunito", sans-serif !important;
}

html {
    scroll-behavior: smooth;
}
</style>
