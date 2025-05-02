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


extract_labels <- function(row) {
  if (str_starts(row, "\\[")) {
    first_label <- str_match(row, '^\\["([^"]+)"')
    return(first_label[, 2])
  }
  
  return(str_trim(row))
}


releases <- read_csv(small_releases) %>%
  select(release_labels_label_id, release_labels_label_name) %>% 
  drop_na() %>% 
  mutate(release_labels_label_id = str_trim(map_chr(release_labels_label_id, extract_labels))) %>% 
  mutate(release_labels_label_name = str_trim(map_chr(release_labels_label_name, extract_labels))) %>% 
  group_by(release_labels_label_name) %>% 
  summarize(counts = n()) %>% 
  arrange(desc(counts))

write_csv(releases, paste0("top_labels_", small_releases))