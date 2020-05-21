import ElementUI from "element-ui"
import Vue from "vue"
import VueRouter from "vue-router"
import component from "{{component}}"
import GameStore from "../js/GameStore.js";
import {VueHammer} from 'vue2-hammer'

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(VueHammer)

new Vue({
  el: "#app",
  store: GameStore,
  render(createElement) {
    return createElement(component)
  }
})
