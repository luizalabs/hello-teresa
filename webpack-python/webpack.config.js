var baseDir = __dirname + '/hello/static/js';

module.exports = {
  context: baseDir + '/src',
  entry: {
    show: './show.js'
  },
  output: {
    path: baseDir + '/dist',
    filename: '[name].js'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        }
      }
    ]
  }
};
