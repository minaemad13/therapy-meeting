module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  // Enable purge
  purge: ['./templates/**/*.html', './static/**/*.js'],
  mode: 'jit',
}
