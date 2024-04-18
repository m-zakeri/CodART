package org.jfree.chart.axis;

import org.jfree.chart.ui.RectangleEdge;
import org.jfree.data.category.CategoryDataset;

import java.awt.geom.Rectangle2D;
import java.io.Serializable;

public class CategoryAxisHelper implements Serializable, Cloneable {
    /**
     * The amount of space reserved at the start of the axis.
     */
    private double lowerMargin;
    /**
     * The amount of space reserved at the end of the axis.
     */
    private double upperMargin;
    /**
     * The amount of space reserved between categories.
     */
    private double categoryMargin;

    public double getLowerMargin() {
        return lowerMargin;
    }

    public void setLowerMargin(double lowerMargin) {
        this.lowerMargin = lowerMargin;
    }

    public double getUpperMargin() {
        return upperMargin;
    }

    public void setUpperMargin(double upperMargin) {
        this.upperMargin = upperMargin;
    }

    public double getCategoryMargin() {
        return categoryMargin;
    }

    public void setCategoryMargin(double categoryMargin) {
        this.categoryMargin = categoryMargin;
    }

    /**
     * Returns the Java 2D coordinate for a category.
     *
     * @param anchor        the anchor point.
     * @param category      the category index.
     * @param categoryCount the category count.
     * @param area          the data area.
     * @param edge          the location of the axis.
     * @return The coordinate.
     */
    public double getCategoryJava2DCoordinate(CategoryAnchor anchor,
                                              int category, int categoryCount, Rectangle2D area,
                                              RectangleEdge edge, CategoryAxis categoryAxis) {

        double result = 0.0;
        if (anchor == CategoryAnchor.START) {
            result = getCategoryStart(category, categoryCount, area, edge, categoryAxis);
        } else if (anchor == CategoryAnchor.MIDDLE) {
            result = getCategoryMiddle(category, categoryCount, area, edge, categoryAxis);
        } else if (anchor == CategoryAnchor.END) {
            result = getCategoryEnd(category, categoryCount, area, edge, categoryAxis);
        }
        return result;

    }

    /**
     * Returns the middle coordinate for the specified category.
     *
     * @param category      the category.
     * @param categoryCount the number of categories.
     * @param area          the data area.
     * @param edge          the axis location.
     * @return The coordinate.
     * @see #getCategoryStart(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     * @see #getCategoryEnd(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     */
    public double getCategoryMiddle(int category, int categoryCount,
                                    Rectangle2D area, RectangleEdge edge, CategoryAxis categoryAxis) {

        if (category < 0 || category >= categoryCount) {
            throw new IllegalArgumentException("Invalid category index: "
                    + category);
        }
        return getCategoryStart(category, categoryCount, area, edge, categoryAxis)
                + calculateCategorySize(categoryCount, area, edge) / 2;

    }

    /**
     * Returns the end coordinate for the specified category.
     *
     * @param category      the category.
     * @param categoryCount the number of categories.
     * @param area          the data area.
     * @param edge          the axis location.
     * @return The coordinate.
     * @see #getCategoryStart(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     * @see #getCategoryMiddle(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     */
    public double getCategoryEnd(int category, int categoryCount,
                                 Rectangle2D area, RectangleEdge edge, CategoryAxis categoryAxis) {
        return getCategoryStart(category, categoryCount, area, edge, categoryAxis)
                + calculateCategorySize(categoryCount, area, edge);
    }

    /**
     * Returns the middle coordinate (in Java2D space) for a series within a
     * category.
     *
     * @param categoryIndex the category index.
     * @param categoryCount the category count.
     * @param seriesIndex   the series index.
     * @param seriesCount   the series count.
     * @param itemMargin    the item margin (0.0 &lt;= itemMargin &lt; 1.0);
     * @param area          the area ({@code null} not permitted).
     * @param edge          the edge ({@code null} not permitted).
     * @return The coordinate in Java2D space.
     * @since 1.0.13
     */
    public double getCategorySeriesMiddle(int categoryIndex, int categoryCount,
                                          int seriesIndex, int seriesCount, double itemMargin,
                                          Rectangle2D area, RectangleEdge edge, CategoryAxis categoryAxis) {

        double start = getCategoryStart(categoryIndex, categoryCount, area,
                edge, categoryAxis);
        double end = getCategoryEnd(categoryIndex, categoryCount, area, edge, categoryAxis);
        double width = end - start;
        if (seriesCount == 1) {
            return start + width / 2.0;
        } else {
            double gap = (width * itemMargin) / (seriesCount - 1);
            double ww = (width * (1 - itemMargin)) / seriesCount;
            return start + (seriesIndex * (ww + gap)) + ww / 2.0;
        }
    }

    /**
     * Returns the starting coordinate for the specified category.
     *
     * @param category      the category.
     * @param categoryCount the number of categories.
     * @param area          the data area.
     * @param edge          the axis location.
     * @return The coordinate.
     * @see #getCategoryMiddle(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     * @see #getCategoryEnd(int, int, Rectangle2D, RectangleEdge, CategoryAxis categoryAxis)
     */
    public double getCategoryStart(int category, int categoryCount,
                                   Rectangle2D area, RectangleEdge edge, CategoryAxis categoryAxis) {

        double result = 0.0;
        if ((edge == RectangleEdge.TOP) || (edge == RectangleEdge.BOTTOM)) {
            result = area.getX() + area.getWidth() * lowerMargin;
        } else if ((edge == RectangleEdge.LEFT)
                || (edge == RectangleEdge.RIGHT)) {
            result = area.getMinY() + area.getHeight() * lowerMargin;
        }

        double categorySize = calculateCategorySize(categoryCount, area, edge);
        double categoryGapWidth = categoryAxis.calculateCategoryGapSize(categoryCount, area,
                edge);

        result = result + category * (categorySize + categoryGapWidth);
        return result;
    }

    /**
     * Calculates the size (width or height, depending on the location of the
     * axis) of a category.
     *
     * @param categoryCount the number of categories.
     * @param area          the area within which the categories will be drawn.
     * @param edge          the axis location.
     * @return The category size.
     */
    public double calculateCategorySize(int categoryCount, Rectangle2D area,
                                        RectangleEdge edge) {
        double result;
        double available = 0.0;

        if ((edge == RectangleEdge.TOP) || (edge == RectangleEdge.BOTTOM)) {
            available = area.getWidth();
        } else if ((edge == RectangleEdge.LEFT)
                || (edge == RectangleEdge.RIGHT)) {
            available = area.getHeight();
        }
        if (categoryCount > 1) {
            result = available * (1 - lowerMargin - upperMargin
                    - categoryMargin);
            result = result / categoryCount;
        } else {
            result = available * (1 - lowerMargin - upperMargin);
        }
        return result;
    }

    /**
     * Returns the middle coordinate (in Java2D space) for a series within a
     * category.
     *
     * @param category   the category ({@code null} not permitted).
     * @param seriesKey  the series key ({@code null} not permitted).
     * @param dataset    the dataset ({@code null} not permitted).
     * @param itemMargin the item margin (0.0 &lt;= itemMargin &lt; 1.0);
     * @param area       the area ({@code null} not permitted).
     * @param edge       the edge ({@code null} not permitted).
     * @return The coordinate in Java2D space.
     * @since 1.0.7
     */
    public double getCategorySeriesMiddle(Comparable category,
                                          Comparable seriesKey, CategoryDataset dataset, double itemMargin,
                                          Rectangle2D area, RectangleEdge edge, CategoryAxis categoryAxis) {

        int categoryIndex = dataset.getColumnIndex(category);
        int categoryCount = dataset.getColumnCount();
        int seriesIndex = dataset.getRowIndex(seriesKey);
        int seriesCount = dataset.getRowCount();
        double start = getCategoryStart(categoryIndex, categoryCount, area, edge, categoryAxis);
        double end = getCategoryEnd(categoryIndex, categoryCount, area, edge, categoryAxis);
        double width = end - start;
        if (seriesCount == 1) {
            return start + width / 2.0;
        } else {
            double gap = (width * itemMargin) / (seriesCount - 1);
            double ww = (width * (1 - itemMargin)) / seriesCount;
            return start + (seriesIndex * (ww + gap)) + ww / 2.0;
        }
    }

    public Object clone() {
        try {
            return super.clone();
        } catch (CloneNotSupportedException e) {
            throw new InternalError("Failed to implement Cloneable interface");
        }
    }
}