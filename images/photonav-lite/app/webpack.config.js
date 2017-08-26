var ExtractTextPlugin = require('extract-text-webpack-plugin');
var webpack = require('webpack');

let config = {
  entry: [
    './src/index.js'
  ],
  output: {
    path: __dirname,
    publicPath: '/',
    filename: './bundle.js'
  },
  module: {
    loaders: [
      {
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          presets: ['react', 'es2015', 'stage-1']
        }
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('css!sass')
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin('./style.css', {
      allChunks: true
    })
  ],
  resolve: {
    extensions: ['', '.js', '.jsx'],
    alias: { soundmanager2: 'soundmanager2/script/soundmanager2-nodebug-jsmin.js' }
  },
  devServer: {
    historyApiFallback: true,
    contentBase: './'
  }
};


if (process.env.NODE_ENV === 'production') {
  config.plugins.push(
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    })
  )
  config.plugins.push(
    new webpack.optimize.UglifyJsPlugin()
  )
}

module.exports = config
