module.exports = {
    extends: [
      'plugin:vue/vue3-recommended'
    ],
    rules: {
      'vue/multi-word-component-names': 'off',
        'vue/no-parsing-error': [
            2, {
                'x-invalid-end-tag': false,
            },
        ]

    }
  }
