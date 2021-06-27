const {generatePages} = require("./conf/TemplateSystem");
const VueLoaderPlugin = require("vue-loader/lib/plugin")
const path = require("path")
const CopyWebpackPlugin = require("copy-webpack-plugin")
const CompressionWebpackPlugin = require("compression-webpack-plugin")
//mode是webpack后来添加的，而这里需要做些预处理，所以必须解析参数
const argString = process.argv.join();
let mode = "production";
if (argString.indexOf('mode=development') !== -1) {
  mode = "development";
} else if (argString.indexOf("mode=production") !== -1) {
  mode = "production";
} else if (argString.indexOf("webpack-dev-server") !== -1) {
  mode = "development";
}
console.log(`mode=${mode}`)
const distPath = path.join(__dirname, "./dist")
const webpackConfig = {
  mode: mode,
  entry: {
    //entry通过模板配置自动生成
  },
  output: {
    path: distPath,
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        test: /\.worker\.(js|ts)$/, //以.worker.js结尾的文件将被worker-loader加载
        loader: 'worker-loader',
        options: {
          name: "[name][hash].worker.js",
        }
      },
      {
        test: /\.css$/,
        use: ["vue-style-loader", "css-loader"]
      },
      {
        test: /\.less$/,
        use: ["vue-style-loader", "css-loader", "less-loader"]
      },
      {
        test: /\.ts$/,
        use: ['ts-loader']
      },
      {
        test: /\.(png|jpg|gif|mp3|svg|ttf|woff|eot|woff2|ogg|wav)$/,
        loader: "url-loader",
        options: {
          name: "[name].[ext]?[hash]",
          limit: 8192
        }
      }
    ]
  },
  resolve: {
    extensions: [".ts", ".js", ".vue"],
    alias: {
      vue: "vue/dist/vue.js",
    }
  },
  plugins: [
    new VueLoaderPlugin(),
    new CopyWebpackPlugin([
      {
        from: path.join(__dirname, "./static")
      }
    ]),
    {
      condition: mode === "production",
      ifTrue: new CompressionWebpackPlugin({
        test: new RegExp("\\.(" + ["js", "css"].join("|") + ")$"),
        // asset: "[path].gz[hash]",
        algorithm: "gzip",
        threshold: 10240,
        minRatio: 0.8
      })
    },
  ],
  devServer: {
    contentBase: distPath,
    proxy: {
      "/api": "http://localhost:5001",
      "/res": "http://localhost:5001",
    },
    host: "0.0.0.0",
    port: 8081,
    hot: true,
    disableHostCheck: true,
    historyApiFallback: {
      rewrites: [{from: /^\/$/, to: "/Index.html"}]
    }
  }
}
module.exports = generatePages(webpackConfig);
