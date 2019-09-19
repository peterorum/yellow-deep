;(function() {
    'use strict'

    var s3 = require('s3')

    //----------- s3

    var s3client = s3.createClient({
        maxAsyncS3: 20, // this is the default
        s3RetryCount: 3, // this is the default
        s3RetryDelay: 1000, // this is the default
        multipartUploadThreshold: 20971520, // this is the default (20 MB)
        multipartUploadSize: 15728640, // this is the default (15 MB)
        s3Options: {
            accessKeyId: process.env.s3Key,
            secretAccessKey: process.env.s3Secret,
            region: 'us-east-1'
        }
    })

    //--------- list s3 bucket

    var s3list = function(bucket) {
        return new Promise(function(resolve, reject) {
            var s3files = []

            var lister = s3client.listObjects({
                s3Params: {
                    Bucket: bucket
                }
            })

            lister.on('error', function(err) {
                console.error('unable to list:', err.stack)
                reject()
            })

            lister.on('data', function(data) {
                // console.log('data', data);
                // s3files.push(data.Contents)
                s3files = [...s3files, ...data.Contents]
            })

            lister.on('end', function() {
                var result = {
                    count: lister.objectsFound,
                    files: s3files
                }

                resolve(result)
            })
        })
    }

    //--------- upload to s3

    var s3upload = function(bucket, key, file) {
        return new Promise(function(resolve, reject) {
            console.log('Sending to s3', bucket, key, file)

            var params = {
                localFile: file,

                s3Params: {
                    Bucket: bucket,
                    Key: key,
                    ACL: 'public-read'
                }
            }

            var uploader = s3client.uploadFile(params)

            uploader.on('error', function(err) {
                console.error('unable to upload:', err.stack)
                reject()
            })

            uploader.on('progress', function() {
                // console.log("progress", uploader.progressMd5Amount, uploader.progressAmount, uploader.progressTotal);
            })

            uploader.on('end', function() {
                // console.log("done uploading");
                resolve()
            })

            uploader.on('fileOpened', function() {
                // console.log('file opened');
            })

            uploader.on('fileClosed', function() {
                // console.log('file closed');
            })
        })
    }

    //--------- doenload from s3

    var s3download = function(bucket, key, file) {
        return new Promise(function(resolve, reject) {
            console.log('Downloading from s3', bucket, key, file)

            var params = {
                localFile: file,

                s3Params: {
                    Bucket: bucket,
                    Key: key
                }
            }

            var downloader = s3client.downloadFile(params)

            downloader.on('error', function(err) {
                console.error('unable to download:', err.stack)
                reject()
            })

            downloader.on('progress', function() {
                // console.log("progress", downloader.progressAmount, downloader.progressTotal);
            })

            downloader.on('end', function() {
                // console.log("done downloading");
                resolve()
            })
        })
    }

    //--------- delete from s3

    var s3delete = function(bucket, key) {
        return new Promise(function(resolve, reject) {
            // console.log('Deleting ', bucket, key);

            var S3Params = {
                Bucket: bucket,
                Delete: {
                    Objects: [
                        {
                            Key: key
                        }
                    ]
                }
            }

            var deleter = s3client.deleteObjects(S3Params)

            deleter.on('error', function(err) {
                console.error('unable to delete:', err.stack)
                reject({ error: err })
            })

            deleter.on('end', function() {
                console.log('deleted', bucket, key)

                resolve({})
            })
        })
    }

    //----------- exports

    exports.list = s3list
    exports.upload = s3upload
    exports.download = s3download
    exports.delete = s3delete
})()
