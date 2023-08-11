<template>
    <section class="background tw-absolute tw-bottom tw-right-0 tw-left-0">
        <div class="custom-container">
            <h3 class="tw-text-4xl tw-font-bold tw-pt-32">{{ $t('homePage.Description') }}:</h3>
            <p class="tw-text-xl tw-font-normal pt-10 pb-16">
                💎💎💎 {{ $t('homePage.Footer description') }}
            </p>
            <div class="tw-flex tw-justify-between tw-items-end tw-pb-4">
                <p class="footer-margin">{{ $t('homePage.Copyright') }} OeHMP</p>
                <img src="@/static/home/logo.svg" alt="logo" />
                <img src="@/static/home/footer-desc.png" alt="footer-desc" />
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: "WebFooter",

    data: () => ({
        social: ["Facebook", "Twitter", "Instagram", "Linkedin"]
    })
};
</script>

<style>
.background {
    background-image: url(@/static/home/bg-footer.svg);
    background-color: #c6dee1 !important;
    background-size: calc(100% + 10px);
    background-position: top center;
}

.footer-margin {
    margin-bottom: 0 !important;
    margin-right: 100px;
}

.tw-bottom {
    bottom: -30rem;
}
</style>
