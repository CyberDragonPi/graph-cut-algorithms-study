library(dplyr)
library(ggplot2)

folder_path <- "data/results_csv"
csv_files <- list.files(path = folder_path, pattern = "*.csv", full.names = TRUE)

all <- lapply(csv_files, function(f) {
  df <- read.csv(f)
  df$algorithm <- tools::file_path_sans_ext(basename(f))
  df
})
big <- bind_rows(all)

results_summary <- big %>%
  group_by(algorithm) %>%
  summarise(
    Total_Graphs = n(),
    Finished_Under_3min = sum(min_cut != -1),
    Percent_Finished = round(Finished_Under_3min / Total_Graphs * 100, 2),
    Max_Nodes = max(ifelse(min_cut != -1, nodes, NA), na.rm = TRUE),
    Max_Edges = max(ifelse(min_cut != -1, edges, NA), na.rm = TRUE)
  )

print("Completion rate summary:")
print(results_summary)

opt <- big %>%
  filter(grepl("min_cut_partition_results$", algorithm)) %>%   # files ending with partition_results
  filter(min_cut != -1) %>%
  select(graph, nodes, edges, opt_cut = min_cut)


greedy_files <- c("min_cut_greedy_results", "min_cut_greedy_partition_results")

precision_list <- list()

for (g_alg in greedy_files) {
  
  gdata <- big %>%
    filter(algorithm == g_alg, min_cut != -1) %>%
    select(graph, nodes, edges, greedy_cut = min_cut)
  
  cmp <- inner_join(opt, gdata, by = c("graph", "nodes", "edges")) %>%
    mutate(
      abs_err = abs(greedy_cut - opt_cut),
      rel_err = ifelse(opt_cut > 0, abs_err / opt_cut, NA),
      exact_match = abs_err == 0
    )
  
  worst_abs_row <- cmp[which.max(cmp$abs_err), ]
  worst_rel_row <- cmp[which.max(cmp$rel_err), ]
  
  precision_summary <- cmp %>%
    summarise(
      comparisons = n(),
      mean_abs_error = round(mean(abs_err), 3),
      mean_rel_error = round(mean(rel_err, na.rm = TRUE), 3),
      exact_match_rate = round(mean(exact_match) * 100, 2),
      max_abs_error = max(abs_err, na.rm = TRUE),
      max_rel_error = round(max(rel_err, na.rm = TRUE), 3)
    )
  
  precision_summary$algorithm <- g_alg
  precision_summary$worst_abs_graph <- worst_abs_row$graph
  precision_summary$worst_rel_graph <- worst_rel_row$graph
  
  precision_list[[g_alg]] <- precision_summary
  
  err_data <- cmp %>% filter(abs_err > 0)
  
  if (nrow(err_data) > 0) {
    p <- ggplot(err_data, aes(x = abs_err)) +
      geom_histogram(binwidth = 1, color = "black", fill = "steelblue") +
      labs(
        title = paste("Histogram of Absolute Errors (non-zero) for Greedy Partition"),
        x = "Absolute Error",
        y = "Frequency"
      ) +
      theme_minimal(base_size = 8)
    
    ggsave(
      filename = paste0("hist_abs_error_", g_alg, ".png"),
      plot = p,
      width = 4, height = 3, dpi = 200
    )
    
    print(p)  
  } else {
    message("All results for ", g_alg, " were exact (no error > 0)")
  }
}