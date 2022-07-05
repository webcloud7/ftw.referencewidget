const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");

const package_json = require("./package.json");
const mf_config = require("@patternslib/patternslib/webpack/webpack.mf");
const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = (env) => {
  let config = {
    mode: env.prod ? "production" : "development",
    devtool: env.prod ? "source-map" : "inline-source-map",
    entry: {
      "referencewidget.min": path.resolve(
        __dirname,
        "./ftw/referencewidget/resources/src/main.js"
      ),
    },
    output: {
      path: path.resolve(
        __dirname,
        "./ftw/referencewidget/resources/dist"
      ),
      chunkFilename: "chunks/[contenthash].min.js",
      clean: true, // Clean directory before compiling
    },
    resolve: {
      alias: {
        "@": path.resolve(
          __dirname,
          "./ftw/referencewidget/resources/src/widget"
        ),
      },
    },
    plugins: [
      new VueLoaderPlugin(),
      new MiniCssExtractPlugin({
        filename: "[name].css",
        // chunkFilename: "[id].css",
      }),
      new webpack.DefinePlugin({
        // Drop Options API from bundle
        __VUE_OPTIONS_API__: "true",
        __VUE_PROD_DEVTOOLS__: "true",
      }),
    ],
    module: {
      rules: [
        {
          test: /\.vue$/,
          use: ["vue-loader"],
        },
        {
          test: /\.scss$/,
          use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
        },
      ],
    },
    optimization: {
      minimize: env.prod,
      minimizer: [
        new CssMinimizerPlugin(),
        new TerserPlugin({
          include: /(\.js$)/,
          extractComments: false,
          terserOptions: {
            output: {
              comments: false,
            },
          },
        }),
      ],
    },
  };

  config.plugins.push(
    mf_config({
      filename: "referencewidget-remote.min.js",
      package_json: package_json,
      remote_entry: config.entry["referencewidget.min"],
      shared: {
        referencewidget: {
          singleton: true,
          requiredVersion: package_json.dependencies["referencewidget"],
        },
      },
    })
  );

  return config;
};
