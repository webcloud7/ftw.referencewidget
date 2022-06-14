import App from "./widget/App.vue";
import { createApp } from "vue";
import VueAxios from "vue-axios";
import axios from "axios";
import qs from "qs";

function axiosInstance() {
  const instance = axios.create({
    paramsSerializer: (params) =>
      qs.stringify(params, { arrayFormat: "repeat" }),
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
  });
  return instance;
}

document.querySelectorAll(".reference-widget").forEach((element) => {
  const app = createApp(App);
  app.use(VueAxios, {
    axios: axiosInstance(),
  });
  app.mount(element);
});
