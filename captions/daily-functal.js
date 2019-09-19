const graph = require('fbgraph')
const tumblr = require('tumblr.js')

const s3 = require('./s3-client')
const getCaption = require('./get-caption').getCaption
const twit = require('./tweet-media')

// post to facebook

function posttofacebook(imageUrl, message) {
  return new Promise(function(resolve, reject) {
    graph.setAccessToken(process.env.fb_df_access_token)

    // get page accounts
    graph.get('me/accounts', function(err, res) {
      const fbpage = res.data.find(p => p.name === 'Daily Functal')

      // change access token to page's
      graph.setAccessToken(fbpage.access_token)

      var post = {
        message,
        url: imageUrl
      }

      // post to page photos
      graph.post('/' + fbpage.id + '/photos', post, function(err, res) {
        console.log(res)

        if (err) {
          console.log(err)
          reject(err)
        }
        else {
          resolve()
        }
      })
    })
  })
}

// tumblr

function posttotumblr(message, imageUrl) {
  return new Promise(function(resolve, reject) {
    const tumblrClient = tumblr.createClient({
      consumer_key: process.env.tumblr_df_consumer_key,
      consumer_secret: process.env.tumblr_df_consumer_secret,
      token: process.env.tumblr_df_token,
      token_secret: process.env.tumblr_df_token_secret
    })

    var options = {
      caption: message,
      source: imageUrl
    }

    tumblrClient.createPhotoPost('functal', options, function(err, data) {
      if (err) {
        console.log(err)
        reject(err)
      }

      console.log(data)
      resolve()
    })
  })
}

// get random image & caption

s3.list('functals').then(function(result) {
  if (result.count === 0) {
    console.log('No files')
  } else {
    const filenames = result.files.map(f => f.Key)

    const filename = filenames[Math.floor(Math.random() * filenames.length)]

    const bucket = 'functals'

    const imageUrl = `https://${bucket}.s3.amazonaws.com/${filename}`

    getCaption(imageUrl).then(
      caption => {
        console.log(`${imageUrl} ${caption}`)

        if (caption) {
          const message = `"${caption}" #fractal #functal #digitalart`

          posttofacebook(imageUrl, message).then(() => {}, () => {})

          posttotumblr(message, imageUrl).then(() => {}, () => {})

          // download file to /tmp

          const tmpFile = '/tmp/functal.jpg'

          s3.download(bucket, filename, tmpFile).then(function() {
            twit.tweet(message, tmpFile).then(() => {}, () => {})
          })
        }
      },
      err => console.error(err)
    )
  }
})
