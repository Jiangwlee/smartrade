// import './assets/main.css'

import { createApp } from "vue";
import { createPinia } from "pinia";
import ElementPlus from "element-plus";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import "element-plus/dist/index.css";
import "@/assets/styles/global.scss";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(router).use(ElementPlus, { locale: zhCn }).use(createPinia());
app.mount("#app");
