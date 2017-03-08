"use strict";

var s3 = require("s3");
var upload = exports = module.exports = {}

upload.toS3 = uploadDirToS3



function uploadDirToS3(dir, options) {

    var client = s3.createClient({
        maxAsyncS3: 20,
        s3RetryCount: 3,
        s3RetryDelay: 1000,
        multipartUploadThreshold: 20971520,
        multipartUploadSize: 15728640,
        s3Options: {
            accessKeyId: options.aws.id,
            secretAccessKey: options.aws.secret,
            region: options.aws.region,
        },
    });

    var params = {
        localDir: dir,
        deleteRemoved: true,

        s3Params: {
            Bucket: options.aws.bucket,
            Prefix: options.aws.dir,
        }
    };

    var uploader = client.uploadDir(params);
    uploader.on("error", function(err) {
        console.log("cannot sync:", err.stack)
    })
    uploader.on("progress", function() {
        console.log("progress", uploader.progressAmount, uploader.progressTotal);
    })
    uploader.on("end", function() {
        console.log("done uploading");
    })

}