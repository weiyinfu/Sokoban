import {createRouter, createWebHashHistory} from 'vue-router'
import GameView from "../component/GameView";
import ProblemSet from "../component/ProblemSet";
import AddProblem from "../component/AddProblem";
import About from "../component/About";

const routes = [
    {path: "/", component: ProblemSet},
    {path: "/game/:game", component: GameView},
    {path: "/add", component: AddProblem},
    {path: "/about", component: About}
    // {
    //     path: '/about',
    //     name: 'About',
    //     // route level code-splitting
    //     // this generates a separate chunk (about.[hash].js) for this route
    //     // which is lazy-loaded when the route is visited.
    //     component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    // }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
