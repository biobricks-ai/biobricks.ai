#!/usr/bin/env Rscript
mode <- commandArgs(trailingOnly = T)[[1]]

if(mode == "deploy"){
  blogdown::build_site()
  system('aws s3 sync public s3://biobricks.ai --profile insilica')
  system('aws cloudfront create-invalidation --distribution-id E2739YSAG8CXB8 --paths "/*"')
}

if(mode == "status"){
  dryrun <- system('aws s3 sync public s3://biobricks.ai --profile insilica --dryrun',intern=T)
  lines  <- strsplit(dryrun,"\\(dryrun\\) upload: ") |> purrr::pluck(1,.default=c())
  cat(sprintf('need to update below %s files\n',length(lines)))
  print(lines)
  inv <- system('aws cloudfront list-invalidations --distribution-id E2739YSAG8CXB8',intern=T)
  inv <- jsonlite::fromJSON(inv)
  print(inv$InvalidationList$Items)
}