# Wipe out variables
rm(list = ls())

library("tidyverse")

args <- (commandArgs(trailingOnly = TRUE))
if (length(args) == 1) {
  small_releases <- args[1]
} else {
  cat("usage:  Rscript top_labels.R <small_releases_file>\n", file = stderr())
  stop()
}


extract_genre <- function(row) {
  if (str_starts(row, "\\[")) {
    first_genre <- str_match(row, '^\\["([^"]+)"')
    return(first_genre[, 2])
  }
  
  return(str_trim(row))
}


releases <- read_csv(small_releases) %>%
  select(release_genres_genre, releases_release_released, releases_release_master_id, releases_release_master_id_is_main_release) %>% 
  drop_na() %>% 
  mutate(year_release = str_extract(releases_release_released, "\\d{4}")) %>% 
  mutate(year_release = ifelse(year_release == "١٩٩٤", 1994, year_release)) %>%
  mutate(year_release = ifelse(year_release == "２０１２", 2012, year_release)) %>% 
  mutate(year_release = as.numeric(year_release)) %>%
  filter(year_release >= 1925) %>% 
  filter(year_release < 2025) %>% 
  mutate(genres = map_chr(release_genres_genre, extract_genre)) %>%
  drop_na() %>% 
  filter(!(genres %in% c("Non-Music", "Brass & Military", "Children's", "1")))


write_csv(releases, paste0("survival_", small_releases))