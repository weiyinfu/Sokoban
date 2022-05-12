import {createStore} from 'vuex'
import {wrapUrl} from "../js/lib";
const axios = require("axios");

function saveConfig(config) {
    localStorage.config = JSON.stringify(config)
}

function loadConfig() {
    if (localStorage.config) {
        try {
            return JSON.parse(localStorage.config)
        } catch (e) {
            return null;
        }
    }
    return null;
}

export default createStore({
    state: {
        config: {
            skinIndex: 0,
        },
        index: {},
        maps: [],
        gameDataLoaded: false,
    },
    mutations: {
        initOver(state, payload) {
            state.gameDataLoaded = true;
        },
        initIndexAndMap(state, payload) {
            state.index = payload.index;
            state.maps = payload.maps;
            const config = loadConfig();
            if (config) {
                for (let i of Object.keys(config)) {
                    state.config[i] = config[i];
                }
            }
        },
        setSkinIndex(state, skinIndex) {
            state.config.skinIndex = skinIndex;
            saveConfig(state.config);
        },
        setAnswer(state, {level, qa}) {
            if (!state.maps[level].answer || (this.maps[level].answer.length > qa.a.length)) {
                //更新答案，不用重新加载地图数据了
                state.maps[level].answer = qa.a;
            }
        }
    },
    actions: {
        async init(context) {
            if (context.state.gameDataLoaded) return;
            const [indexResp, mapsResp] = await axios.all([axios.get("index.json"), axios.get(wrapUrl("/api/get_maps"))])
            const index = indexResp.data;
            const maps = mapsResp.data;
            context.commit("initIndexAndMap", {index: index, maps: maps});
            return context.dispatch('loadSkin', context.state.config.skinIndex).then(() => {
                context.commit("initOver");
            })
        },
        loadSkin(context, skinIndex) {
            return new Promise(resolve => {
                //加载皮肤
                console.log(`正在加载皮肤`);
                const skin = context.state.index.skins[skinIndex];
                const imageKeys = Object.keys(skin.images);
                let loaded = 0;//已经加载成功的个数
                for (let k of imageKeys) {
                    if (typeof (skin.images[k]) === "string") {
                        //如果没有加载过，则加载之
                        const img = new Image();
                        img.onload = () => {
                            if (++loaded === imageKeys.length) {
                                context.commit("setSkinIndex", skinIndex);
                                resolve();
                            }
                        }
                        img.src = skin.images[k];
                        skin.images[k] = img;
                    } else {
                        //只要有一个已经加载过了，那就全部都加载过了
                        context.commit("setSkinIndex", skinIndex);
                        resolve();
                    }
                }
            })
        },
    }
})
