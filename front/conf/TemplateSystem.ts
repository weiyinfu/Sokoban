import {ExternalJsList, ExternalJs, TemplateList, ExternalCssList, ExternalCss} from "./conf";
import webpackConfigFilter from "./WebpackConfigFilter";

const handlebars = require("handlebars")
const chalk = require("chalk")
const fs = require("fs");
const path = require("path");
const glob = require("glob");

/**
 * 模板系统
 * */
enum Mode {
    development = "development",
    production = "production",
}

//handlebars编译，根据templatePath指定的模板位置，结合context生成到distPath目录下
function handlebarsCompile(template: (context: any) => string, distPath: string, context: any) {
    fs.writeFileSync(distPath, template(context))
}

const jsNameMap: { [index: string]: ExternalJs } = {};
const cssNameMap: { [index: string]: ExternalCss } = {};
ExternalJsList.forEach(e => jsNameMap[e.name] = e);
ExternalCssList.forEach(e => cssNameMap[e.name] = e);

function getWebpackExternal() {
    //webpack的External字段
    const ans: { [index: string]: string } = {}
    ExternalJsList.forEach(item => ans[item.name] = item.outterName);
    return ans;
}

function getExternalJs(externals: string[]): string {
    externals.forEach(external => {
        if (!jsNameMap[external]) {
            throw new Error(`cannot find external with name ${external}`);
        }
    })
    return externals.map(e => `<script src="${jsNameMap[e].url}"></script>`).join('\n');
}

function getExternalCss(externals: string[]): string {
    externals.forEach(external => {
        if (!cssNameMap[external]) {
            throw new Error(`cannot find external with name ${external}`);
        }
    })
    return externals.map(e => `<link href="${cssNameMap[e].url}" rel="stylesheet" />`).join('\n')
}

function getTemplate(templatePath: string) {
    if (!fs.existsSync(templatePath)) throw new Error(`cannot find template ${templatePath}`);
    const template = fs.readFileSync(templatePath).toString("utf8");
    return handlebars.compile(template)
}

function ensureDir(dir: string) {
    if (fs.existsSync(dir)) return;
    const father = path.dirname(dir);
    if (!fs.existsSync(father)) {
        ensureDir(father);
    }
    fs.mkdirSync(dir)
}

export function generatePages(webpackConfig: { [index: string]: any }) {
    //为每个Vue生成html文件
    if (webpackConfig.mode === Mode.production) {
        webpackConfig.externals = getWebpackExternal();
    }

    const visited = new Set<string>();//已经编译过的文件，再次遇到就会跳过
    for (const tem of TemplateList) {
        const templateStyles = getExternalCss(tem.externalCss);
        const templateScripts = getExternalJs(tem.externalJs);
        const htmlTemplate = getTemplate(path.join(__dirname, tem.htmlTemplate));
        const jsTemplate = getTemplate(path.join(__dirname, tem.jsTemplate));
        const files = glob.sync(tem.files, {cwd: __dirname})
        tem.distPath = path.join(__dirname, tem.distPath);
        tem.genPath = path.join(__dirname, tem.genPath);
        //如果dist和gen不存在，创建之
        for (let dir of [tem.distPath, tem.genPath]) {
            console.log(`ensure dir ${dir}`)
            ensureDir(dir);
        }
        if (!files || files.length === 0) {
            console.warn(chalk.red(`${tem.files} cannot match any file of ${tem.htmlTemplate}`));
        }
        for (let file of files) {
            const filepath = path.normalize(path.join(__dirname, file));
            if (fs.lstatSync(filepath).isDirectory()) continue;
            if (visited.has(filepath)) {
                console.log(chalk.red(`File ${file} has already been compiled,now will skip it !`))
            }
            visited.add(filepath);
            const filename = path.parse(filepath).name;
            const jsPath = path.join(tem.genPath, `${filename}.js`)
            const htmlPath = path.join(tem.distPath, `${filename}.html`)
            handlebarsCompile(htmlTemplate, htmlPath, {
                main: `${filename}.js`,
                templateStyles: webpackConfig.mode === Mode.development ? "" : templateStyles,
                templateScripts: webpackConfig.mode === Mode.development ? "" : templateScripts,
            })
            handlebarsCompile(jsTemplate, jsPath, {
                component: path.relative(path.dirname(jsPath), filepath)
            })
            console.log(chalk.green(`compile ${htmlPath} for ${filename} succssfully`))
            console.log(chalk.green(`compile ${jsPath} for ${filename} succssfully`))
            webpackConfig.entry[filename] = [
                './' + path.relative(path.join(__dirname, '..'), jsPath)
            ]
            //打包时需要引入本地的CSS
            if (webpackConfig.mode === Mode.development) {
                const cssFiles = tem.externalCss.map(cssName => cssNameMap[cssName].local);
                webpackConfig.entry[filename] = webpackConfig.entry[filename].concat(cssFiles);
            }
        }
    }
    webpackConfig = webpackConfigFilter(webpackConfig);
    return webpackConfig;
}
