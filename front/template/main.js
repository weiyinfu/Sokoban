import ElementUI from "element-ui"
import Vue from "vue"
import VueRouter from "vue-router"
import component from "{{component}}"
import GameStore from "../js/GameStore.js";

Vue.use(ElementUI)
Vue.use(VueRouter)

new Vue({
  el: "#app",
  store: GameStore,
  render(createElement) {
    return createElement(component)
  }
})
