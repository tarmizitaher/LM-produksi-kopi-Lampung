#!/usr/bin/env Rscript
# Fig. 1: Study Area Map — Lampung Province, Indonesia
# Two panels: (a) Sumatra context, (b) Lampung detail with kabupaten

library(sf)
library(ggplot2)
library(rnaturalearth)
library(rnaturalearthdata)
library(ggspatial)
library(cowplot)
library(viridis)

# ============================================================
# Data
# ============================================================

# Get Indonesia and Sumatra boundaries
world <- ne_countries(scale = 50, returnclass = "sf")
indonesia <- world[world$admin == "Indonesia", ]
idn_prov <- ne_states(country = "indonesia", returnclass = "sf")
lampung_sf <- idn_prov[grep("Lampung", idn_prov$name), ]
sumatra_provs <- idn_prov[idn_prov$name %in% c(
  "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi",
  "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung",
  "Kepulauan Riau"), ]

# Kabupaten data
kab <- data.frame(
  name = c("Lampung Barat", "Tanggamus", "Lampung Utara", "Way Kanan",
           "Pesisir Barat", "Pesawaran", "Pringsewu",
           "Lampung Selatan", "Lampung Timur", "Lampung Tengah",
           "Bandar Lampung", "Metro", "Mesuji", "Tulang Bawang", "Tulang Bawang Barat"),
  lat = c(-5.02, -5.42, -4.83, -4.65, -5.20, -5.52, -5.36,
          -5.72, -4.75, -4.90, -5.45, -5.11, -4.10, -4.30, -4.45),
  lon = c(104.06, 104.63, 104.88, 104.50, 103.95, 105.08, 104.97,
          105.62, 105.50, 105.20, 105.26, 105.31, 105.40, 105.45, 105.10),
  elev = c(912, 857, 37, 102, 37, 1180, 110, 78, 16, 43, 7, 60, 9, 18, 7),
  prod = c(54252, 34169, 10109, 9753, 3827, 1607, 1582, 499, 284, 351, 152, 1, 40, 34, 19),
  yield = c(987, 810, 418, 439, 564, 421, 528, 598, 470, 561, 872, 778, 480, 368, 561),
  area = c(55193, 42234, 24676, 22193, 6778, 3732, 2414, 823, 603, 637, 156, 1, 88, 89, 54),
  coffee = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE,
             FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE),
  stringsAsFactors = FALSE
)

kab_sf <- st_as_sf(kab, coords = c("lon", "lat"), crs = 4326)
kab_coffee <- kab[kab$coffee, ]
kab_other <- kab[!kab$coffee, ]

# BMKG stations
bmkg <- data.frame(
  name = c("Negeri Sakti", "Kemiling", "Way Semah"),
  lat = c(-5.13, -5.42, -5.07),
  lon = c(105.10, 105.24, 104.42)
)
bmkg_sf <- st_as_sf(bmkg, coords = c("lon", "lat"), crs = 4326)

# ============================================================
# Panel (a): Sumatra context with Indonesia inset
# ============================================================

p_sumatra <- ggplot() +
  geom_sf(data = sumatra_provs, fill = "#d4c5a9", color = "#666", linewidth = 0.3) +
  geom_sf(data = lampung_sf, fill = "#e74c3c", alpha = 0.5, color = "red", linewidth = 0.8) +
  coord_sf(xlim = c(95, 107), ylim = c(-6.5, 6)) +
  annotate("text", x = 100, y = 1.5, label = "SUMATRA", size = 5,
           fontface = "bold", alpha = 0.3, angle = 50) +
  annotate("text", x = 99, y = -4, label = "Indian\nOcean", size = 3.5,
           alpha = 0.4, fontface = "italic") +
  annotate("text", x = 105.5, y = -5, label = "Lampung", size = 3,
           color = "red", fontface = "bold") +
  labs(x = "Longitude (\u00b0E)", y = "Latitude", title = "(a) Lampung Province in Sumatra") +
  theme_minimal(base_family = "serif", base_size = 10) +
  theme(
    panel.background = element_rect(fill = "#d6eaf8", color = NA),
    panel.grid = element_line(color = "white", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 11, hjust = 0.5)
  )

# Indonesia inset
p_inset <- ggplot() +
  geom_sf(data = indonesia, fill = "#d4c5a9", color = "#666", linewidth = 0.2) +
  geom_sf(data = lampung_sf, fill = "red", color = "red", linewidth = 0.5) +
  coord_sf(xlim = c(94, 141), ylim = c(-11, 7)) +
  annotate("rect", xmin = 95, xmax = 107, ymin = -6.5, ymax = 6,
           color = "red", fill = NA, linewidth = 0.5, linetype = "dashed") +
  labs(title = "Indonesia") +
  theme_void(base_family = "serif") +
  theme(
    panel.background = element_rect(fill = "#d6eaf8", color = "black", linewidth = 0.5),
    plot.title = element_text(face = "bold", size = 7, hjust = 0.5),
    plot.margin = margin(1, 1, 1, 1)
  )

# Combine Sumatra + inset
p_a <- ggdraw() +
  draw_plot(p_sumatra) +
  draw_plot(p_inset, x = 0.05, y = 0.60, width = 0.35, height = 0.35)

# ============================================================
# Panel (b): Lampung detail
# ============================================================

p_lampung <- ggplot() +
  # Province boundary
  geom_sf(data = lampung_sf, fill = "#eef5ee", color = "black", linewidth = 0.8) +

  # Other kabupaten (gray squares)
  geom_point(data = kab_other, aes(x = lon, y = lat),
             shape = 15, size = 2.5, color = "gray50", alpha = 0.6) +

  # Coffee kabupaten (colored circles, sized by area)
  geom_point(data = kab_coffee,
             aes(x = lon, y = lat, fill = yield, size = area),
             shape = 21, color = "black", stroke = 0.8) +
  scale_fill_viridis(option = "inferno", limits = c(350, 1050),
                     name = "Mean Productivity\n(kg/ha)") +
  scale_size_continuous(range = c(3, 14), guide = "none") +

  # BMKG stations (blue triangles)
  geom_point(data = bmkg, aes(x = lon, y = lat),
             shape = 24, size = 3, fill = NA, color = "blue", stroke = 1.2) +

  # Labels: coffee kabupaten
  ggrepel::geom_label_repel(
    data = kab_coffee,
    aes(x = lon, y = lat,
        label = paste0(name, "\n(", formatC(area, big.mark = ",", format = "d"),
                       " ha, ", yield, " kg/ha)")),
    size = 2.3, fontface = "bold", family = "serif",
    fill = "white", alpha = 0.85,
    label.padding = unit(0.15, "lines"),
    box.padding = unit(0.5, "lines"),
    segment.color = "gray40", segment.size = 0.3,
    min.segment.length = 0, max.overlaps = 20,
    seed = 42
  ) +

  # BMKG station labels
  ggrepel::geom_text_repel(
    data = bmkg, aes(x = lon, y = lat, label = name),
    size = 2.5, color = "blue", fontface = "bold", family = "serif",
    nudge_y = 0.08, segment.size = 0.3, segment.color = "blue",
    seed = 42
  ) +

  # North arrow and scale
  annotation_north_arrow(
    location = "tr", which_north = "true",
    height = unit(1, "cm"), width = unit(0.7, "cm"),
    style = north_arrow_fancy_orienteering(text_size = 7)
  ) +
  annotation_scale(location = "bl", width_hint = 0.25, text_family = "serif",
                   text_cex = 0.7, line_width = 0.5) +

  coord_sf(xlim = c(103.5, 106.1), ylim = c(-6.1, -3.9)) +
  labs(x = "Longitude (\u00b0E)", y = "Latitude (\u00b0S)",
       title = "(b) Coffee-Producing Districts & BMKG Stations") +

  theme_minimal(base_family = "serif", base_size = 10) +
  theme(
    panel.background = element_rect(fill = "#d6eaf8", color = NA),
    panel.grid = element_line(color = "white", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 11, hjust = 0.5),
    legend.position = "bottom",
    legend.title = element_text(size = 8),
    legend.text = element_text(size = 7),
    legend.key.height = unit(0.3, "cm"),
    legend.key.width = unit(1.5, "cm")
  ) +
  guides(fill = guide_colorbar(title.position = "top", title.hjust = 0.5))

# ============================================================
# Combine panels
# ============================================================

fig1 <- plot_grid(p_a, p_lampung, ncol = 2, rel_widths = c(0.45, 0.55))

outdir <- "/Users/tarmizitaher/Documents/Dummy test/reports/figures"
ggsave(file.path(outdir, "fig1_study_area.png"), fig1,
       width = 14, height = 7, dpi = 300, bg = "white")
ggsave(file.path(outdir, "fig1_study_area.pdf"), fig1,
       width = 14, height = 7, bg = "white")
cat("Saved: fig1_study_area.png + .pdf\n")
