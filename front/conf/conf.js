"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * 为了减小打包之后的代码体积，我们会把一些库拆分出来，使用CDN的方式加载这些库
 * 外部库包括两类：Js和css。
 * */
class ExternalJs {
    constructor() {
        this.name = "";
        this.outterName = "";
        this.url = "";
    }
}
exports.ExternalJs = ExternalJs;
exports.ExternalJsList = [
    {
        name: "vue",
        outterName: "Vue",
        url: "https://cdn.bootcss.com/vue/2.6.6/vue.min.js",
    }, {
        name: "element-ui",
        outterName: "ELEMENT",
        url: "https://cdn.bootcss.com/element-ui/2.4.11/index.js",
    },
    {
        name: "vue-router",
        outterName: "VueRouter",
        url: "https://cdn.bootcss.com/vue-router/3.0.2/vue-router.min.js",
    }
];
class ExternalCss {
    constructor() {
        this.name = "";
        this.local = "";
        this.url = "";
    }
}
exports.ExternalCss = ExternalCss;
exports.ExternalCssList = [
    {
        name: "font-awesome",
        local: "font-awesome/css/font-awesome.min.css",
        url: "https://cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css"
    },
    {
        name: "element-ui",
        local: "element-ui/lib/theme-chalk/index.css",
        url: "https://cdn.bootcss.com/element-ui/2.5.4/theme-chalk/index.css"
    },
];
/**
 * 模板系统配置
 * */
const distPath = "../dist";
const genPath = "../gen";
class Template {
    constructor() {
        this.jsTemplate = "";
        this.htmlTemplate = "";
        this.files = "";
        this.externalJs = []; //外部js列表
        this.externalCss = []; //外部css列表
        this.genPath = ""; //生成的js的路径
        this.distPath = ""; //生成的html的路径
    }
}
exports.Template = Template;
//目录为相对当前文件
exports.TemplateList = [
    {
        jsTemplate: "../template/main.js",
        htmlTemplate: "../template/Blog.html",
        files: "../pages/*.vue",
        externalJs: ['vue', 'element-ui', 'vue-router'],
        externalCss: ['font-awesome', "element-ui"],
        genPath,
        distPath,
    },
];
