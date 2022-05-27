# Biobricks.ai Static Documentation Page

Deploy with

```
hugo -D
aws s3 sync public s3://biobricks.ai --profile insilica
aws cloudfront create-invalidation --distribution-id E2739YSAG8CXB8 --paths /*
```
