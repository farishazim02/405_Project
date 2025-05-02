# Wipe out variables
rm(list = ls())

library("tidyverse")

args = (commandArgs(trailingOnly = TRUE))
if(length(args) == 1){
  small_artists = args[1]
} else {
  cat('usage:  Rscript process_artists.R <small_artists_file>\n', file = stderr())
  stop()
}

# Load small artists file
artists <- read_csv(small_artists, col_names = F) %>%
  select(X10, X11)

colnames(artists) <- c("artist_id", "artist_name")

# Write the results in a csv file
output_file <- paste0("processed_", small_artists)
write.csv(artists, output_file, row.names = F)