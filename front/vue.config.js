module.exports = {
  devServer: {
    // headers: {
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Credentials': 'true',
    //   'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS,POST,PUT',
    //   'Access-Control-Allow-Headers':
    //     'Origin, X-Requested-With, Content-Type, Accept, Authorization',
    // },
    proxy: 'http://20.245.26.188:8000/',
    // port: 8666
  }
}