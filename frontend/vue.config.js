const { defineConfig } = require('@vue/cli-service')
const YAML = require('yaml')
const fs = require("fs");
const file = fs.readFileSync('../config.yaml', 'utf8')
config = YAML.parse(file)

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: config["host"]["frontend"],
    port: config["port"]["frontend"], // 端口
    proxy: {
      '/api': {
      target: config["docker"] ? "http://backend:5008" : "http://127.0.0.1:5008",
      changeOrigin: true,
      pathRequiresRewrite: {
        "^/api":""
      }
    },
    '/_uploads': {
      target: config["docker"] ? "http://backend:5008" : "http://127.0.0.1:5008",
      changeOrigin: true,
      pathRequiresRewrite: {
        "^/_uploads":""
      }
    }
  }
  },
  
  // transpileDependencies: ['@arcgis']
})

