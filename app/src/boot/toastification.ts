import { boot } from 'quasar/wrappers';
import Toast, { PluginOptions, POSITION } from 'vue-toastification';

export default boot(({ app }) => {
  const options: PluginOptions = {
    position: POSITION.BOTTOM_CENTER,
    maxToasts: 1,
  };

  app.use(Toast, options);
});
