# the below was meant to invalidate only the changed files
# paths=`aws s3 sync ./ s3://biobricks.ai --profile insilica --dryrun | cut -d' ' -f3`
# however, it is more cost efficient to invalidate the whole bucket
# A path that includes the * wildcard counts as one path even if it causes CloudFront to invalidate thousands of files.

hugo -D
aws s3 sync public s3://biobricks.ai --profile insilica
aws cloudfront create-invalidation --distribution-id E2739YSAG8CXB8 --paths "/*"

echo 'check status `aws cloudfront get-invalidation --id {invalidation_id} --distribution-id E2739YSAG8CXB8'