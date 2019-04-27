const webpack = require('webpack');
const path = require('path');
const MiniCSSExtractPlugin = require('mini-css-extract-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const WebpackAssetsManifest = require('webpack-manifest-plugin');


const assetsPath = path.join(__dirname, 'appengine_flask_security_auth', 'assets')

module.exports = {
    entry: {
        app_scripts: './appengine_flask_security_auth/assets/app.js',
        app_styles: './appengine_flask_security_auth/assets/app.scss',
        app_images: './appengine_flask_security_auth/assets/images.js'
    },
    output: {
        path: path.join(__dirname, 'appengine_flask_security_auth', 'static', 'build'),
        publicPath: `/static/build/`,
        filename: '[name].[hash].js',
        chunkFilename: '[name]_[id].[chunkhash].js'
    },

    plugins: [
        new MiniCSSExtractPlugin({
            filename: '[name].[hash].css',
            chunkFilename: '[name]_[id].[chunkhash].css'
        }),
        new CleanWebpackPlugin(),
        new WebpackAssetsManifest(),
    ],
    module: {
        rules: [{
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                use: [{
                        loader: 'babel-loader',
                        options: {
                            plugins: ['syntax-dynamic-import'],
                            presets: [
                                [
                                    '@babel/preset-env',
                                    {
                                        modules: false
                                    }
                                ]
                            ]
                        },
                    },
                    'eslint-loader',
                ],
            },
            {
                test: /\.(scss|css)$/,
                use: [{
                        loader: MiniCSSExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'sass-loader'
                    }
                ]
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            context: assetsPath,
                            name: '[path][name].[hash].[ext]',
                        }
                    },
                ]
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            context: assetsPath,
                            name: '[path][name].[hash].[ext]',
                        }
                    },
                ]
            }

        ]
    },
};
