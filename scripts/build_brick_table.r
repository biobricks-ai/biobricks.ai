library(stringr)
library(purrr)
library(httr)

# get all repos
repos_json <- httr::GET("https://api.github.com/orgs/biobricks-ai/repos?per_page=100&page=1") |>
    httr::content()

repos_info <- repos_json |>
# filter out 
purrr::discard(~ .x$svn_url |> basename() %in% 
c("biobricks-r", "biobricks-issues", "bricktools", "hello-brick", "biobricks.ai","github-actions")) |>
# get readme url
    purrr::map(function(x) {
    y <- list()
    y$repo <- x$svn_url
    y$default_branch <- x$default_branch
    y$readme <- paste0("https://raw.githubusercontent.com/biobricks-ai/",x$svn_url |> basename() ,"/", y$default_branch, "/README.md")
    y$readme_md <- httr::GET(y$readme) |> httr::content()
    y
})

md_rows <- repos_info |>
# process readme into table entry
purrr::map(function(x) {
    y <- list()
    y$badge <- x$readme_md |> stringr::str_extract("<a.*")
    y$description <- x$readme_md |> stringr::str_match("Description[\\n\\r]*>\\s*(.*)") |> purrr::pluck(2) |> trimws()
    y$brick_name <- paste0("[", x$repo |> basename() ,"](", x$repo, ")")
    paste0("|", y$brick_name, "|", y$description, "|", y$badge, "|")
}) |> unlist() |> sort() |> paste(collapse="\n")

paste0("| Brick | Description | Bricktools Status |\n","|---|---|---|\n", md_rows) |> writeLines("SUMMARY.md")
