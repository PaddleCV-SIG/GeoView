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
  },
  
  // transpileDependencies: ['@arcgis']
})

