/**
 * 为了减小打包之后的代码体积，我们会把一些库拆分出来，使用CDN的方式加载这些库
 * 外部库包括两类：Js和css。
 * */
export class ExternalJs {
  name: string = "";
  outterName: string = "";
  url: string = "";
}

export const ExternalJsList: ExternalJs[] = [
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
]

export class ExternalCss {
  name: string = "";
  local: string = "";
  url: string = "";
}

export const ExternalCssList: ExternalCss[] = [
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
]

/**
 * 模板系统配置
 * */
const distPath = "../dist";
const genPath = "../gen";

export class Template {
  jsTemplate: string = "";
  htmlTemplate: string = "";
  files: string = "";
  externalJs: string[] = [];//外部js列表
  externalCss: string[] = [];//外部css列表
  genPath: string = "";//生成的js的路径
  distPath: string = "";//生成的html的路径
}

//目录为相对当前文件
export const TemplateList: Template[] = [
  {
    jsTemplate: "../template/main.js",
    htmlTemplate: "../template/Blog.html",
    files: "../pages/*.vue",
    externalJs: ['vue', 'element-ui', 'vue-router'],
    externalCss: ['font-awesome', "element-ui"],
    genPath,
    distPath,
  },
]
