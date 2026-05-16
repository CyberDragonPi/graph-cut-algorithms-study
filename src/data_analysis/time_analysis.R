library(dplyr)
library(ggplot2)

folder_path <- "data/results_csv"
csv_files <- list.files(path = folder_path, pattern = "*.csv", full.names = TRUE)

# Load all CSVs and combine
all <- lapply(csv_files, function(f) {
  df <- read.csv(f)
  df$algorithm <- tools::file_path_sans_ext(basename(f))
  df
})
big <- bind_rows(all)

# Filter only rows where algorithm finished (min_cut != -1)
valid <- big %>% filter(min_cut != -1)
valid$algorithm <- recode(valid$algorithm,
                          "min_cut_greedy_results" = "Greedy edge removal",
                          "min_cut_greedy_partition_results" = "Greedy partition",
                          "min_cut_partition_results" = "Exhaustive Partition",
                          "min_cut_removing_edges_results" = "Exhaustive Edge Subset"
)

ops_by_nodes <- valid %>%
  group_by(algorithm, nodes) %>%
  summarise(
    avg_ops = mean(basic_operations, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(log_ops = log10(avg_ops))

ops_by_edges <- valid %>%
  group_by(algorithm, edges) %>%
  summarise(
    avg_ops = mean(basic_operations, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(log_ops = log10(avg_ops))
         
         
 p1 <- ggplot(ops_by_nodes, aes(x = nodes, y = log_ops, color = algorithm)) +
      geom_line() + geom_point() +
      labs(
      title = "Log Basic Operations vs Number of Nodes",
      x = "Number of Nodes (|V|)",
      y = "log10(Basic Operations)"
      ) +
      theme_minimal()
 
ggsave("log_ops_vs_nodes.pdf", p1, width = 6, height = 4)
print("Saved: log_ops_vs_nodes.png")
print(p1)
         
         
p2 <- ggplot(ops_by_edges, aes(x = edges, y = log_ops, color = algorithm)) +
        geom_line() + geom_point() +
        labs(
        title = "Log Basic Operations vs Number of Edges",
        x = "Number of Edges (|E|)",
        y = "log10(Basic Operations)"
        ) +
        theme_minimal()

ggsave("log_ops_vs_edges.pdf", p2, width = 6, height = 4)
print("Saved: log_ops_vs_nedges.pdf")

print(p1)


sol_by_nodes <- valid %>%
  group_by(algorithm, nodes) %>%
  summarise(
    avg_solutions = mean(solutions_tested, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(log_solutions = log10(avg_solutions))

p_solutions_nodes <- ggplot(sol_by_nodes,
                            aes(x = nodes, y = log_solutions, color = algorithm)) +
  geom_line() + geom_point() +
  labs(
    title = "Log Solutions Tested vs Number of Nodes",
    x = "Number of Nodes (|V|)",
    y = "log10(Solutions Tested)"
  ) +
  theme_minimal()

ggsave("log_solutions_vs_nodes.pdf", p_solutions_nodes,
       width = 6, height = 4)

print("Saved: log_solutions_vs_nodes.pdf")
print(p_solutions_nodes)

corr_table <- valid %>%
  group_by(algorithm) %>%
  summarise(
    n = n(),
    correlation = cor(solutions_tested, basic_operations, use = "complete.obs"),
    .groups = "drop"
  )

print("Correlation between solutions tested and basic operations:")
print(corr_table)

filtered <- valid %>% 
  filter(algorithm != "Exhaustive Edge Subset")

time_by_nodes <- filtered %>%
  group_by(algorithm, nodes) %>%
  summarise(
    avg_time = mean(time_elapsed, na.rm = TRUE),
    .groups = "drop"
  )

p4 <- ggplot(time_by_nodes, aes(x = nodes, y = avg_time, color = algorithm)) +
  geom_line() + geom_point() +
  scale_y_log10() +
  labs(title = "Runtime vs Number of Nodes",
       x = "Number of Nodes (|V|)",
       y = "Runtime (seconds, log scale)") +
  theme_minimal()

ggsave("time_vs_nodes.pdf", p4,
       width = 6, height = 4)