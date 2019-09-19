"use strict";

// get captions from microsoft vision api

let request = require('request');

function getCaption(image) {

  return new Promise(function(resolve, reject) {
    request.post({
      uri: 'https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze',
      headers: {
        'Ocp-Apim-Subscription-Key': process.env.ms_key1
      },
      json: true,
      body: {
        url: image
      },
      qs: {
        visualFeatures: 'Description'
      }
    }, (error, response, body) => {

      if (error) {
        reject('api error', error);
      } else {
//
//         { description:
//            { tags:
//               [ 'plane',
//                 'large',
//                 'boat',
//                 'hanging',
//                 'colorful',
//                 'air',
//                 'blue',
//                 'umbrella',
//                 'flying' ],
//              captions: [ [Object] ] },
//           requestId: 'ca2104a9-ac46-4d21-8f28-4d6e3ee77121',
//           metadata: { width: 768, height: 1024, format: 'Jpeg' } }
//
        let caption = body.description && body.description.captions && body.description.captions.length && body.description.captions[0].text;

        if (!caption && body.description && body.description.tags && body.description.tags.length) {
          caption = body.description.tags[0];
        }

        if (!caption) {

          reject(body);

        // body:
        //  { statusCode: 429,
        //    message: 'Rate limit is exceeded. Try again in 1 seconds.' } }

        // body:
        // { code: 'InvalidImageUrl',
        //   message: 'Image URL is not accessible.' } }


        } else {
          resolve(caption);
        }
      }
    });

  });

}

// let image = 'http://functals.s3.amazonaws.com/functal-20150524050802146.jpg';
//
// getCaption(image).then(caption => {
//   console.log('get-captions', caption);
// });

exports.getCaption = getCaption;
