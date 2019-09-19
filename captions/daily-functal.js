const graph = require('fbgraph')

const s3 = require('./s3-client')
const getCaption = require('./get-caption').getCaption
const twit = require('./tweet-media');

// post to facebook

function posttofacebook(imageUrl, caption) {

  graph.setAccessToken(process.env.fb_df_access_token)

  // get page accounts
  graph.get('me/accounts', function(err, res) {
    const fbpage = res.data.find(p => p.name === 'Daily Functal')

    // change access token to page's
    graph.setAccessToken(fbpage.access_token)

    const message = `"${caption}" #fractal #functal #digitalart`

    var post = {
      message,
      url: imageUrl
    }

    // post to page photos
    graph.post('/' + fbpage.id + '/photos', post, function(/*err, res*/) {
      // console.log(res)
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
          // posttofacebook(imageUrl, caption)

          // download file to /tmp

          const tmpFile  = '/tmp/functal.jpg';

          s3.download(bucket, filename, tmpFile).then(function() {

            twit.tweet(`"${caption}" #fractal #functal #digitalart`, tmpFile, function() {});

          })


        }
      },
      err => console.error(err)
    )
  }
})
