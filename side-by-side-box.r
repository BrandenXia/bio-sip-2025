library(tidyr)
library(dplyr)
library(ggplot2)

df <- read.csv("genes.csv", stringsAsFactors = FALSE)

# Filter data for LG1 and LG13 separately
df_LG1 <- df %>% filter(region == "LG1")
df_LG13 <- df %>% filter(region == "LG13")

prepare_plot_data <- function(data) {
  data %>%
    select(old_geneid, start, end, original_start, original_end) %>%
    pivot_longer(cols = c(start, end, original_start, original_end),
                 names_to = "position_type",
                 values_to = "position") %>%
    mutate(group = ifelse(grepl("original", position_type), "Original", "Current"),
           old_geneid = factor(old_geneid, levels = unique(old_geneid)))
}

plot_gene_positions <- function(plot_data, region_name) {
  ggplot(plot_data, aes(x = old_geneid, y = position, fill = group)) +
    geom_boxplot(
      coef = 0,
      outlier.shape = NA,
      color = "black",
      size = 0.5,
      fatten = 0,
      position = position_dodge(width = 0.9),
      width = 0.5
    ) +
    scale_y_continuous(expand = expansion(mult = c(0.02, 0.02)), breaks = scales::pretty_breaks(n = 6)) +
    coord_cartesian(clip = "off") +
    labs(title = paste("Current vs Original Positions per Gene in", region_name),
    x = "Gene ID",
    y = "Gene Position",
    fill = "Position Group") +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      panel.grid.major.x = element_blank(),
      panel.grid.minor.x = element_blank()
    ) +
    scale_fill_manual(values = c("Current" = "#1f77b4", "Original" = "#ff7f0e"))
  
}

# Prepare data for each region
plot_data_LG1 <- prepare_plot_data(df_LG1)
plot_data_LG13 <- prepare_plot_data(df_LG13)

# Create plots
plot_LG1 <- plot_gene_positions(plot_data_LG1, "LG1")
plot_LG13 <- plot_gene_positions(plot_data_LG13, "LG13")

# Print plots separately
print(plot_LG1)
print(plot_LG13)
