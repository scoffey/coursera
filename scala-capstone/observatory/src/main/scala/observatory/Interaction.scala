package observatory

import com.sksamuel.scrimage.{Image, Pixel}
import observatory.Visualization.{interpolateColor, predictTemperature}

import scala.math._

/**
  * 3rd milestone: interactive visualization
  */
object Interaction extends InteractionInterface {

  /**
    * @param tile Tile coordinates
    * @return The latitude and longitude of the top-left corner of the tile, as per http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    */
  def tileLocation(tile: Tile): Location = {
    val n = pow(2, tile.zoom)
    val r = atan(sinh(Pi * (1 - 2 * tile.y / n)))
    Location(r * 180 / Pi, tile.x / n * 360 - 180)
  }

  /**
    * @param temperatures Known temperatures
    * @param colors Color scale
    * @param tile Tile coordinates
    * @return A 256×256 image showing the contents of the given tile
    */
  def tile(temperatures: Iterable[(Location, Temperature)], colors: Iterable[(Temperature, Color)], tile: Tile): Image = {
    makeImage(colors, tile, predictTemperature(temperatures, _))
  }

  /**
    * Generates all the tiles for zoom levels 0 to 3 (included), for all the given years.
    * @param yearlyData Sequence of (year, data), where `data` is some data associated with
    *                   `year`. The type of `data` can be anything.
    * @param generateImage Function that generates an image given a year, a zoom level, the x and
    *                      y coordinates of the tile and the data to build the image from
    */
  def generateTiles[Data](
    yearlyData: Iterable[(Year, Data)],
    generateImage: (Year, Tile, Data) => Unit
  ): Unit = {
    val ts = for {
      (year, data) <- yearlyData
      zoom <- 0 to 3
      x <- 0 until (1 << zoom)
      y <- 0 until (1 << zoom)
    } yield (year, Tile(x, y, zoom), data)

    ts.par.foreach(generateImage.tupled)
  }

  /**
    * Helper method that creates a 256×256 image given a color scale and a location to temperature mapper function.
    *
    * @param colors Color scale
    * @param tile Tile coordinates
    * @param locationToTemperature Function that returns the temperature for a given location
    * @return A 256×256 image showing the contents of the given tile
    */
  def makeImage(colors: Iterable[(Temperature, Color)], tile: Tile, locationToTemperature: Location => Temperature): Image = {
    val width = 256
    val height = 256

    val baseZoom = 8
    val (x0, y0) = (tile.x * (1 << baseZoom), tile.y * (1 << baseZoom))
    val zoom = tile.zoom + baseZoom

    val coords = for {
      y <- 0 until height
      x <- 0 until width
    } yield (x, y)

    val pixels = coords
      .map({ case (x, y) => tileLocation(Tile(x + x0, y + y0, zoom)) })
      .map(locationToTemperature)
      .map(interpolateColor(colors, _))
      .map(color => Pixel(color.red, color.green, color.blue, 127))
      .toArray

    Image(width, height, pixels)
  }

}
