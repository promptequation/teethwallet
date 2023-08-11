<template>
    <main>
        <!-- Banner Section -->
        <section class="banner-background tw-pt-8">
            <div class="custom-container tw-z-30">
                <div class="bottom-padding tw-relative">
                    <div class="gif-shaper"></div>
                    <h1 class="tw-text-7xl tw-font-black line-height">
                        Oral e-Health <br />
                        Monitoring Platform
                    </h1>
                    <div class="tw-bg-white d-inline-block rounded-50 tw-my-8">
                        <h3 class="tw-text-3xl tw-font-medium tw-px-5 tw-py-2 ">
                            {{
                                $t(
                                    'homePage.Keep track of what makes you smile'
                                )
                            }}
                        </h3>
                    </div>
                    <p class="tw-text-2xl tw-font-medium text-color mb-55 tw-max-w-[600px]">
                        {{
                            $t(
                                'homePage.Working to give you a complete detailed and easy to access and manage in-hand dental clinic record'
                            )
                        }}
                    </p>
                    <nuxt-link to="/start" class="start-button">{{
                        $t("menu.Start now")
                    }}</nuxt-link>
                </div>
            </div>
        </section>

        <section class="main-page-background">
            <div class="custom-container">
                <div class="tw-text-center padding-top">
                    <h3 class="tw-text-4xl tw-font-medium">
                        {{
                            $t(
                                'homePage.Oral e Health Platform gives you the right to store,'
                            )
                        }}
                    </h3>
                    <h3 class="tw-text-4xl tw-font-medium tw-mb-16">
                        {{
                            $t(
                                'homePage.access and share your clinical dental data'
                            )
                        }}
                    </h3>
                </div>
                <div class="tw-flex tw-justify-between tw-pb-10">
                    <div class="tw-mr-5 w-100" v-for="(data, i) in clinicData" :key="i">
                        <div class="icon-box tw-flex tw-justify-center tw-items-center ">
                            <img class="" :src="data.icon" alt="file-icon" />
                        </div>
                        <div class="tw-pl-20 tw-pr-12  tw-text-left">
                            <p class="tw-text-xl tw-font-extrabold tw-pt-6 ">
                                {{ data.title }}
                            </p>
                            <p class="tw-text-x tw-font-medium tw-text-[#646464] tw-pr-20">
                                {{ data.description }}
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Project Sheet Section -->
                <div id="project" class="project-sheet tw-flex tw-justify-center tw-items-center tw-mt-12 tw-mb-16">
                    <img src="@/static/home/description-2.png" class="tw-w-[80%]" alt="description" />
                </div>

                <!-- Description Section -->
                <div class="tw-flex tw-justify-between para-margin tw-pb-40">
                    <div class="main-background">
                        <div class="desc-title tw-mt-0">
                            <p>{{ $t('homePage.Project') }}:</p>
                            <div class="capsule">
                                <p>72636</p>
                            </div>
                        </div>
                        <div class="desc-title">
                            <p>{{ $t('homePage.Title') }}:</p>
                            <div class="capsule">
                                <p>Oral e-Health Monitoring Platform</p>
                            </div>
                        </div>
                        <div class="desc-title">
                            <p>{{ $t('homePage.Acronym') }}:</p>
                            <div class="capsule">
                                <p>OeHMP</p>
                            </div>
                        </div>
                        <div class="tw-flex tw-flex-col tw-items-start my-30">
                            <p class="tw-font-black	tw-text-2xl">
                                {{ $t('homePage.Consortium composition') }}:
                            </p>
                            <div class="capsule ml-0 mt-5">
                                <p>
                                    PromptEquation and Universidade Catolica
                                    Portuguesa
                                </p>
                            </div>
                        </div>
                        <div class="desc-title">
                            <p> {{ $t('homePage.Effective start date') }}:</p>
                            <div class="capsule">
                                <p>1/04/21</p>
                            </div>
                        </div>
                        <div class="desc-title">
                            <p> {{ $t('homePage.Duration') }}:</p>
                            <div class="capsule">
                                <p>30 meses</p>
                            </div>
                        </div>
                        <div class="desc-title">
                            <p>{{ $t('homePage.Funding') }}:</p>
                            <div class="capsule">
                                <p>Portugal2020 - €447,826.53</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="tw-flex tw-justify-between">
                            <p class="tw-opacity-0">.</p>
                            <div class="desc-title tw-mb-8">
                                <p>{{ $t('homePage.Location') }}:</p>
                                <div class="capsule">
                                    <p>Guarda, Portugal</p>
                                </div>
                            </div>
                        </div>
                        <div class="map-border">
                            <iframe
                                src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d16544.635485952604!2d-7.133013115695555!3d40.53671010961285!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd3cfac48ff6c653%3A0x400ebbde4903500!2sGuarda%2C%20Portugal!5e0!3m2!1sen!2sbd!4v1669911320191!5m2!1sen!2sbd"
                                width="650" height="465" style="border:0;" allowfullscreen="" loading="lazy"
                                referrerpolicy="no-referrer-when-downgrade"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import { computed } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";

export default {
    setup() {
        const { $t } = useNuxtTranslator()
        const clinicData = computed(() => {
            return [
                {
                    icon: require("@/static/home/file-icon.png"),
                    title: `${$t("homePage.All your oral health history")}`,
                    description:
                        `${$t("homePage.Manage your dental history with a functional and concise organization")}`,
                },
                {
                    icon: require("@/static/home/chat-icon.png"),
                    title: `${$t("homePage.Chat with your doctors")}`,
                    description:
                        `${$t("homePage.Real-time access to your health care provider message board with free and open communication")}`,
                },
                {
                    icon: require("@/static/home/note-icon.png"),
                    title: `${$t("homePage.All your oral health history")}`,
                    description:
                        `${$t("homePage.Your oral health will no longer stay behind with our alarmistic system")}`,
                }
            ];
        });
        return {
            clinicData
        };
    }
};
</script>

<style scoped>
.gif-shaper {
    border: 1px solid transparent;
    height: 265px;
    width: 416px;
    border-radius: 150px;
    position: absolute;
    top: 185px;
    right: 60px;
    background-image: url(@/static/home/giphy.gif);
    background-position: 52% 65%;
    background-size: calc(100% + 25px);
}

.banner-background {
    background-image: url("@/static/home/header-image.svg") !important;
    background-position: top;
    background-color: #c6dee1;
}

.line-height {
    line-height: 60px;
}

.rounded-50 {
    border-radius: 50px;
}

.text-color {
    color: #7c7c7c;
}

.mb-55 {
    margin-bottom: 55px !important;
}

.bottom-padding {
    padding-bottom: 10rem;
}

.padding-top {
    padding-top: 22rem;
}

.start-button {
    background-color: #bf9dff;
    color: #ffffff;
    align-items: center;
    padding: 15px 103px;
    gap: 10px;
    border-radius: 8px;
}

.main-page-background {
    background-image: url("@/static/home/bg-main.svg");
    background-size: calc(100% + 5px);
    margin-top: -23rem;
}

.icon-box {
    height: 159.42px;
    background: linear-gradient(135deg, #bcd3d6 0%, #d0e9ec 100%);
    box-shadow: -5px 5px 10px rgba(178, 200, 203, 0.2),
        5px -5px 10px rgba(178, 200, 203, 0.2),
        -5px -5px 10px rgba(218, 244, 248, 0.9),
        5px 5px 13px rgba(178, 200, 203, 0.9);
    border-radius: 150px;
}

.map-border iframe {
    border-radius: 25px;
}

.project-sheet {
    background: url("@/static/home/rectangle.png");
    background-size: cover;
    height: 336px;
    width: 100%;
}

.my-30 {
    margin: 30px 0 !important;
}

.desc-title {
    display: flex;
    align-items: center;
    margin-top: 30px;
}

.desc-title p {
    font-weight: 900;
    font-size: 24px;
}

.capsule {
    padding: 0 15px;
    height: 44px;
    margin-left: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #bcd3d6 0%, #d0e9ec 100%);
    box-shadow: -5px 5px 10px rgba(178, 200, 203, 0.2),
        5px -5px 10px rgba(178, 200, 203, 0.2),
        -5px -5px 10px rgba(218, 244, 248, 0.9),
        5px 5px 13px rgba(178, 200, 203, 0.9);
    border-radius: 50px;
}

.capsule p {
    font-size: 24px;
    font-weight: 400;
}

.para-margin p {
    margin: 0px !important;
}

@media only screen and (min-width: 1280px) and (max-width: 1367px) {
    .gif-shaper {
        height: 191px;
        width: 299px;
        top: 183px;
        right: 233px;
    }

    .main-page-background {
        margin-top: -22rem;
    }

    .padding-top {
        padding-top: 20rem;
    }
}

@media only screen and (min-width: 1367px) and (max-width: 1441px) {
    .gif-shaper {
        height: 199px;
        width: 313px;
        top: 170px;
        right: 210px;
    }

    .padding-top {
        padding-top: 21rem;
    }
}

@media only screen and (min-width: 1441px) and (max-width: 1557px) {
    .gif-shaper {
        height: 213px;
        width: 340px;
        top: 171px;
        right: 173px;
    }

    .padding-top {
        padding-top: 23rem;
    }
}

@media only screen and (min-width: 1557px) and (max-width: 1670px) {
    .gif-shaper {
        height: 228px;
        width: 360px;
        top: 141px;
        right: 141px;
    }

    .main-page-background {
        margin-top: -25rem;
    }

    .padding-top {
        padding-top: 24rem;
    }
}

@media only screen and (min-width: 1670px) and (max-width: 1800px) {
    .gif-shaper {
        height: 229px;
        width: 364px;
        top: 141px;
        right: 136px;
    }

    .main-page-background {
        margin-top: -25rem;
    }

    .padding-top {
        padding-top: 25rem;
    }
}

@media only screen and (min-width: 1801px) and (max-width: 2000px) {
    gif-shaper {
        height: 265px;
        width: 416px;
        border-radius: 150px;
        position: absolute;
        top: 185px;
        right: 60px;
    }

    .main-page-background {
        margin-top: -22rem;
    }

    .padding-top {
        padding-top: 25rem;
    }
}

@media only screen and (min-width: 2001px) and (max-width: 2220px) {
    .gif-shaper {
        height: 307px;
        width: 483px;
        top: 54px;
        right: -31px;
        border-radius: 190px
    }

    .main-page-background {
        margin-top: -30rem;
    }

    .padding-top {
        padding-top: 33rem;
    }
}

@media only screen and (min-width: 2221px) and (max-width: 2562px) {
    .gif-shaper {
        height: 357px;
        width: 552px;
        top: 7px;
        right: -137px;
        border-radius: 190px;
    }

    .main-page-background {
        margin-top: -33rem;
    }

    .padding-top {
        padding-top: 37rem;
    }
}
</style>
