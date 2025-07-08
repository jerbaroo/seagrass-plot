import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits.basemap import Basemap
from sys import argv
from typing import List


def draw(
    beds: List[pd.DataFrame],
    llcrnrlat: float,
    llcrnrlon: float,
    urcrnrlat: float,
    urcrnrlon: float,
    image_path: str,
    map_label: str,
    points_label: str,
    arrow_color="white",
    arrow_fontsize=26,
    arrow_headwidth=15,
    arrow_length=0.1,
    arrow_text="N",
    arrow_width=5,
    arrow_x=0.93,
    arrow_y=0.93,
    bed_alpha=0.5,
    bed_color="green",
    figsize=(16, 12),
    legend_fontsize=16,
    legend_loc="lower right",
    point_alpha=0.9,
    point_color="white",
    point_size=3,
    scale_barstyle="fancy",
    scale_fontcolor="white",
    scale_fontsize=16,
    scale_lat_frac=0.92,
    scale_length=200,
    scale_lon_frac=0.86,
    scale_units="m",
    verbose=True,
):

    plt.figure(figsize=figsize)

    # Set up coordinates of our map.
    bmap = Basemap(
        llcrnrlat=llcrnrlat,
        llcrnrlon=llcrnrlon,
        urcrnrlat=urcrnrlat,
        urcrnrlon=urcrnrlon,
        resolution="h",
        epsg=5520,
    )

    def plot_bed_points(bed: pd.DataFrame, label=False):
        """Plot each of the coordinate points in given DataFrame."""
        for i, (lon, lat) in enumerate(zip(bed["lon"], bed["lat"])):
            xpt, ypt = bmap(lon, lat)
            bmap.plot(
                xpt,
                ypt,
                "o",
                markersize=point_size,
                color=point_color,
                alpha=point_alpha,
                label=None if (i > 0) or not label else points_label,
            )

    def plot_bed_fill(bed: pd.DataFrame, label=False):
        """Fill between all the coordinate points in given DataFrame."""
        pts = [bmap(lon, lat) for lon, lat in zip(bed["lon"], bed["lat"])]
        # Duplicate last point at beginning, to ensure we have a full circle.
        pts.append(pts[0])
        pts = np.array(pts)
        plt.fill_between(
            pts.T[0],
            pts.T[1],
            facecolor=bed_color,
            alpha=bed_alpha,
            label=map_label if label else None,
        )

    for i, bed in enumerate(beds):
        label = i == 0  # Only add to legend once.
        plot_bed_fill(bed, label=label)
        plot_bed_points(bed, label=label)

    def scale_lon(frac=scale_lon_frac):
        """Longitute on map calculated from fraction in [0 1]"""
        return (llcrnrlon * frac) + (urcrnrlon * (1 - frac))

    def scale_lat(frac=scale_lat_frac):
        """Latitude on map calculated from fraction in [0 1]"""
        return (llcrnrlat * frac) + (urcrnrlat * (1 - frac))

    bmap.drawmapscale(
        lon=scale_lon(),
        lat=scale_lat(),
        lon0=scale_lon(),
        lat0=scale_lat(),
        length=scale_length,
        barstyle=scale_barstyle,
        units=scale_units,
        fontcolor=scale_fontcolor,
        fontsize=scale_fontsize,
    )

    plt.annotate(
        arrow_text,
        xy=(arrow_x, arrow_y),
        xytext=(arrow_x, arrow_y - arrow_length),
        arrowprops=dict(
            facecolor=arrow_color,
            headwidth=arrow_headwidth,
            width=arrow_width,
        ),
        ha="center",
        va="center",
        fontsize=arrow_fontsize,
        color=arrow_color,
        xycoords=plt.gca().transAxes,
    )

    bmap.arcgisimage(service="World_Imagery", verbose=verbose, xpixels=1500)
    plt.legend(loc=legend_loc, fontsize=legend_fontsize)
    plt.savefig(image_path)


if __name__ == "__main__":
    draw(
        list(map(pd.read_xml, argv[8:])),
        image_path=argv[1],
        map_label=argv[2],
        points_label=argv[3],
        llcrnrlat=float(argv[4]),
        llcrnrlon=float(argv[5]),
        urcrnrlat=float(argv[6]),
        urcrnrlon=float(argv[7]),
    )
