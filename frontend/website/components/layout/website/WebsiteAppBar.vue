<template>
    <section class="header-background  outer-height">
        <div class="second-background box-shadow custom-container">
            <div
                class="tw-flex tw-justify-between tw-items-center inner-height tw-px-14 tw-mt-5"
            >
                <img src="@/static/home/logo.svg" />
                <div class="d-flex font-family">
                    <nuxt-link class="link-text" to="/">{{ $t('menu.Home') }}</nuxt-link>
                    <nuxt-link
                        class="link-text"
                        :to="{ path: '/', hash: 'project' }"
                        >{{ $t('menu.Project Sheet') }}</nuxt-link
                    >
                    <nuxt-link class="link-text" to="/start"
                        >{{ $t('menu.Start now') }}</nuxt-link
                    >
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
a.nuxt-link-exact-active::after {
    content: "";
    width: 8px;
    height: 8px;
    background: #111111;
    border-radius: 50%;
    display: block;
    left: 50%;
    position: absolute;
    margin-left: -4px;
}
.header-background {
    background-image: url("@/static/home/header-image.svg");
    background-position: top;
    background-color: #c6dee1 !important;
}

.second-background {
    background: linear-gradient(135deg, #bcd3d6 0%, #d0e9ec 100%);
    background-image: url("@/static/home/header-image.svg");
    background-position: bottom;
}

.outer-height {
    height: 155px;
}

.inner-height {
    height: 115px !important;
}

.box-shadow {
    box-shadow: -5px 5px 10px rgba(178, 200, 203, 0.2),
        5px -5px 10px rgba(178, 200, 203, 0.2),
        -5px -5px 10px rgba(218, 244, 248, 0.9),
        5px 5px 13px rgba(178, 200, 203, 0.9);
    border-radius: 20px;
}

.link-text {
    font-size: 24px;
    color: #111111;
    font-weight: 400;
    margin-right: 40px;
    padding: 5px;
    line-height: 25px;
    position: relative;
    letter-spacing: 2.95px;
}
</style>
