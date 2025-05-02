# Wipe out variables
rm(list = ls())

library("tidyverse")
library("jsonlite")

args <- (commandArgs(trailingOnly = TRUE))
if (length(args) == 1) {
  small_releases <- args[1]
} else {
  cat("usage:  Rscript artist_ntracks.R <small_releases_file>\n", file = stderr())
  stop()
}

count_list <- function(x) {

  clean <- gsub("\\[|\\]|\"", "", x)
  
  parts <- unlist(str_split(clean, ",\\s*"))
  
  return(length(parts[nzchar(parts)]))
}


releases <- read_csv(small_releases) %>%
  select(artists_artist_id, artists_artist_name, tracklist_track_title) %>% 
  drop_na(artists_artist_id, tracklist_track_title) %>% 
  mutate(n_artists = map_int(artists_artist_id, ~ length(fromJSON(.x)))) %>% 
  mutate(n_tracks = map_int(tracklist_track_title, count_list)) %>% 
  drop_na() %>% 
  select(artists_artist_name, n_artists, n_tracks)

write_csv(releases, paste0("artist_ntracks_", small_releases))

