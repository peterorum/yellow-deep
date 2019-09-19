const s3 = require('./s3-client')
const getCaption = require('./get-caption').getCaption

s3.list('functals').then(function(result) {
  if (result.count === 0) {
    console.log('No files')
  } else {
    const filenames = result.files.map(f => f.Key)

    const filename = filenames[Math.floor(Math.random() * filenames.length)]

    const imageUrl = `https://functals.s3.amazonaws.com/${filename}`

    getCaption(imageUrl).then(
      caption => console.log(`${imageUrl} ${caption}`),
      err => console.error(err)
    )
  }
})
