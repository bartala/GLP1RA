library(igraph)

# --- 1. DATA PREP ---
df_edges <- g_edgelist

if(ncol(df_edges) >= 3) {
  colnames(df_edges)[3] <- "weight" 
} else {
  df_edges$weight <- 1
}
g <- graph_from_data_frame(df_edges, directed = FALSE)

# --- 2. SIZING ---
rescale_vals <- function(x, min_sz, max_sz) {
  if (length(x) == 0) return(numeric(0))
  if (min(x, na.rm=TRUE) == max(x, na.rm=TRUE)) return(rep(max_sz, length(x)))
  (x - min(x, na.rm=TRUE)) / (max(x, na.rm=TRUE) - min(x, na.rm=TRUE)) * (max_sz - min_sz) + min_sz
}

raw_strength <- strength(g, weights = E(g)$weight)
V(g)$size <- rescale_vals(raw_strength, min_sz = 10, max_sz = 40) 
E(g)$width <- rescale_vals(E(g)$weight, min_sz = 0.5, max_sz = 4.0)

# --- 3. CLUSTERING ---
communities <- cluster_louvain(g, weights = E(g)$weight)
V(g)$cluster <- communities$membership
num_clusters <- max(communities$membership)

# --- 4. COLORS ---
nano_palette <- c("#D55E00", "#0072B2", "#009E73", "#CC79A7", 
                  "#E69F00", "#56B4E9", "#F0E442", "#222222")
V(g)$color <- nano_palette[(V(g)$cluster %% length(nano_palette)) + 1]

# --- 5. LATTICE LAYOUT ---
cluster_counts <- table(V(g)$cluster)
sorted_clusters <- names(sort(cluster_counts, decreasing = TRUE))

cols_per_row <- 3
spacing_x <- 26 
spacing_y <- 26   

layout_matrix <- matrix(0, nrow = vcount(g), ncol = 2)
label_matrix  <- matrix(0, nrow = vcount(g), ncol = 2)
align_vec     <- numeric(vcount(g))

for (i in seq_along(sorted_clusters)) {
  cid <- as.numeric(sorted_clusters[i])
  grid_col <- (i - 1) %% cols_per_row
  grid_row <- floor((i - 1) / cols_per_row)
  
  xc <- grid_col * spacing_x
  yc <- -(grid_row * spacing_y)
  
  idx <- which(V(g)$cluster == cid)
  idx <- idx[order(V(g)$size[idx], decreasing = TRUE)]
  
  n_nodes <- length(idx)
  radius_cluster <- 6.0 + (n_nodes * 0.12)
  
  if (n_nodes == 1) {
    layout_matrix[idx, 1] <- xc
    layout_matrix[idx, 2] <- yc
    label_matrix[idx, 1]  <- xc
    label_matrix[idx, 2]  <- yc - 1.5
    align_vec[idx]        <- 0.5
  } else {
    angle_step <- 2 * pi / n_nodes
    for (j in seq_along(idx)) {
      angle <- (j - 1) * angle_step + (pi / 2)
      
      # Node Position
      r_jitter <- radius_cluster + runif(1, -0.1, 0.1) 
      layout_matrix[idx[j], 1] <- xc + r_jitter * cos(angle)
      layout_matrix[idx[j], 2] <- yc + r_jitter * sin(angle)
      
      # Label Position Logic
      if (j %% 2 == 0) {
        dist_factor <- 0.75
      } else {
        dist_factor <- 1.15
      }
      
      label_matrix[idx[j], 1] <- xc + (r_jitter * dist_factor) * cos(angle)
      label_matrix[idx[j], 2] <- yc + (r_jitter * dist_factor) * sin(angle)
      
      #  Alignment
      if (abs(cos(angle)) < 0.1) {
        align_vec[idx[j]] <- 0.5 
      } else {
        align_vec[idx[j]] <- ifelse(cos(angle) > 0, 0, 1)
      }
    }
  }
}

# --- 6. PLOT ---
num_rows <- ceiling(num_clusters / cols_per_row)
pdf_h <- 2 + (num_rows * 5)
pdf_w <- 2 + (cols_per_row * 4.2) 

device_func <- if (capabilities("cairo")) cairo_pdf else pdf
device_func("louvain_lattice_tight.pdf", width = pdf_w, height = pdf_h)

par(mar = c(0.1, 0.1, 0.1, 0.1), bg = "white")

plot(g,
     layout = layout_matrix,
     rescale = FALSE,
     xlim = range(label_matrix[,1]) + c(-3, 3), 
     ylim = range(label_matrix[,2]) + c(-3, 3),
     
     vertex.size = V(g)$size * 6, 
     vertex.color = V(g)$color,
     vertex.frame.color = "white",
     vertex.frame.width = 1.3,
     vertex.label = NA, 
     
     edge.color = adjustcolor("#777777", alpha.f = 0.25),
     edge.width = E(g)$width, 
     edge.curved = 0.3
)

# Draw Labels
for (k in 1:vcount(g)) {
  text(x = label_matrix[k, 1], 
       y = label_matrix[k, 2], 
       labels = V(g)$name[k], 
       cex = 0.9, 
       col = "black", 
       font = 2,
       adj = align_vec[k]) 
}

# Cluster Titles
for (i in seq_along(sorted_clusters)) {
  cid <- as.numeric(sorted_clusters[i])
  grid_col <- (i - 1) %% cols_per_row
  grid_row <- floor((i - 1) / cols_per_row)
  xc <- grid_col * spacing_x
  yc <- -(grid_row * spacing_y)
  
  col_clust <- V(g)$color[which(V(g)$cluster == cid)[1]]
  
  idx <- which(V(g)$cluster == cid)
  n <- length(idx)
  r_c <- 6.0 + (n * 0.12)
  
  text(x = xc, y = yc - (r_c + 4), 
       labels = paste("Cluster", cid), 
       col = col_clust, 
       cex = 1.5, font = 2)
}

dev.off()
