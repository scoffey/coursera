package observatory

import com.sksamuel.scrimage.Image

/**
  * 5th milestone: value-added information visualization
  */
object Visualization2 extends Visualization2Interface {

  /**
    * @param point (x, y) coordinates of a point in the grid cell
    * @param d00 Top-left value
    * @param d01 Bottom-left value
    * @param d10 Top-right value
    * @param d11 Bottom-right value
    * @return A guess of the value at (x, y) based on the four known values, using bilinear interpolation
    *         See https://en.wikipedia.org/wiki/Bilinear_interpolation#Unit_Square
    */
  def bilinearInterpolation(
    point: CellPoint,
    d00: Temperature,
    d01: Temperature,
    d10: Temperature,
    d11: Temperature
  ): Temperature = {
    val (x0, y0) = (point.x, point.y)
    val (x1, y1) = (1 - x0, 1 - y0)
    (d00 * x1 * y1
      + d10 * x0 * y1
      + d01 * x1 * y0
      + d11 * x0 * y0)
  }

  /**
    * @param grid Grid to visualize
    * @param colors Color scale to use
    * @param tile Tile coordinates to visualize
    * @return The image of the tile at (x, y, zoom) showing the grid using the given color scale
    */
  def visualizeGrid(
    grid: GridLocation => Temperature,
    colors: Iterable[(Temperature, Color)],
    tile: Tile
  ): Image = {
    import observatory.Interaction.makeImage

    makeImage(colors, tile, {
      case Location(lat, lon) =>
        val (x0, y0) = (lon.floor, lat.floor)
        val (x1, y1) = (lon.ceil, lat.ceil)
        bilinearInterpolation(
          CellPoint(lon - x0, y1 - lat),
          grid(GridLocation(y1.toInt, x0.toInt)),
          grid(GridLocation(y0.toInt, x0.toInt)),
          grid(GridLocation(y1.toInt, x1.toInt)),
          grid(GridLocation(y0.toInt, x1.toInt))
        )
    })
  }

}
