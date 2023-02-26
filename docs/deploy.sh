# the below was meant to invalidate only the changed files
# paths=`aws s3 sync ./ s3://biobricks.ai --profile insilica --dryrun | cut -d' ' -f3`
# however, it is more cost efficient to invalidate the whole bucket
# A path that includes the * wildcard counts as one path even if it causes CloudFront to invalidate thousands of files.

sphinx-build -b html source build/html
aws s3 sync build/html s3://biobricks.ai

# create invalidation request and get id
did=E1NKAT94ILTVEK
req=`aws cloudfront create-invalidation --distribution-id $did --paths "/*"`
id=`echo $req | jq '.Invalidation.Id'`
# strip quotes from id
id=`echo $id | sed 's/"//g'`

# keep checking status until complete
status="IN_PROGRESS"
while [ $status = "IN_PROGRESS" ]; do
    echo "Invalidation in progress..."
    sleep 3
    req=`aws cloudfront get-invalidation --id $id --distribution-id $did`
    status=`echo $req | jq '.Invalidation.Status'`
done

# print final status
echo "Invalidation complete."