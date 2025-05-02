# Wipe out variables
rm(list = ls())

library("tidyverse")
library("jsonlite")

args <- (commandArgs(trailingOnly = TRUE))
if (length(args) == 1) {
  small_releases <- args[1]
} else {
  cat("usage:  Rscript network_artist_genre.R <small_releases_file>\n", file = stderr())
  stop()
}


split_genres <- function(x) {
  if (str_starts(x, "\\[")) {
    
    content <- str_remove_all(x, "^\\[|\\]$")
    parts <- str_split(content, '"\\s*,\\s*"')[[1]]
    parts <- str_remove_all(parts, '"')
    return(parts)
  }
  return(x)
}

extract_name <- function(row) {
  if (str_starts(row, "\\[")) {
    first_name <- str_match(row, '^\\["([^"]+)"')
    return(first_name[, 2])
  }
  
  return(str_trim(row))
}



releases <- read_csv(small_releases) %>%
  filter(releases_release_master_id_is_main_release == T) %>% 
  select(artists_artist_name, release_genres_genre, releases_release_title) %>% 
  drop_na() %>% 
  mutate(artists_artist_name = str_trim(map_chr(artists_artist_name, extract_name))) %>% 
  mutate(genre_list = map(release_genres_genre, split_genres)) %>%
  unnest_longer(genre_list) %>%
  rename(genre = genre_list)
  
write_csv(releases, paste0("network_", small_releases))



