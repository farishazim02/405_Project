# Wipe out variables
rm(list = ls())

library("tidyverse")

args <- (commandArgs(trailingOnly = TRUE))
if (length(args) == 1) {
  small_releases <- args[1]
} else {
  cat("usage:  Rscript trend_genre_releases.R <small_releases_file>\n", file = stderr())
  stop()
}

extract_genre <- function(row) {
  # If it starts with “[…]”, pull out the first element
  if (str_starts(row, "\\[")) {
    first_genre <- str_match(row, '^\\["([^"]+)"')
    return(first_genre[, 2])
  }
  
  return(str_trim(row))
}

releases <- read_csv(small_releases) %>%
  select(release_genres_genre, releases_release_released) %>%
  drop_na() %>%
  mutate(genres = map_chr(release_genres_genre, extract_genre)) %>%
  mutate(year_release = str_extract(releases_release_released, "\\d{4}")) %>% 
  drop_na(year_release, genres) %>% 
  count(year_release, genres) %>%
  arrange(year_release, desc(n))

write_csv(releases, paste0("trend_genre", small_releases, ".csv"))
