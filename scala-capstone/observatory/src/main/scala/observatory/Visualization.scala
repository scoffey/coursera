package observatory

import com.sksamuel.scrimage.{Image, Pixel}

/**
  * 2nd milestone: basic visualization
  */
object Visualization extends VisualizationInterface {

  /**
    * @param temperatures Known temperatures: pairs containing a location and the temperature at this location
    * @param location Location where to predict the temperature
    * @return The predicted temperature at `location`
    */
  def predictTemperature(temperatures: Iterable[(Location, Temperature)], location: Location): Temperature = {
    import scala.math._
    type Distance = Double

    def distance(a: Location, b: Location): Distance = {
      val avgEarthRadius = 6371 // spatial units are in km
      val deltaLat = toRadians(a.lat - b.lat)
      val deltaLon = toRadians(a.lon - b.lon)
      val sinLat = sin(deltaLat / 2)
      val sinLon = sin(deltaLon / 2)
      val r = sinLat * sinLat + (cos(toRadians(a.lat)) * cos(toRadians(b.lat)) * sinLon * sinLon)
      val deltaSigma = 2 * atan2(sqrt(r), sqrt(1 - r))

      avgEarthRadius * deltaSigma
    }

    def getInverseDistanceWeighting(dts: Iterable[(Distance, Temperature)]): Temperature = {
      val p = 2.3 // customizable fudge factor
      val (ws, is) = dts.map({
        case (distance, temp) => (temp / pow(distance, p), 1 / pow(distance, p))
      }).unzip
      ws.sum / is.sum
    }

    val dts = temperatures.map({
      case (loc, temp) => (distance(location, loc), temp)
    })

    dts.find({
      case (distance, _) => distance < 1.0 // consider same temperature within 1 km
    }).getOrElse(
      (0, getInverseDistanceWeighting(dts))
    )._2
  }

  /**
    * @param points Pairs containing a value and its associated color
    * @param value The value to interpolate
    * @return The color that corresponds to `value`, according to the color scale defined by `points`
    */
  def interpolateColor(points: Iterable[(Temperature, Color)], value: Temperature): Color = {
    val (lowerPairs, higherPairs) = points.partition({
      case (temp, _) => value > temp
    })

    if (lowerPairs.isEmpty) {
      higherPairs.minBy(_._1)._2
    } else if (higherPairs.isEmpty) {
      lowerPairs.maxBy(_._1)._2
    } else {
      val (lowerTemp, lowerColor) = lowerPairs.maxBy(_._1)
      val (upperTemp, upperColor) = higherPairs.minBy(_._1)

      def interpolate(lo: Int, hi: Int): Int = {
        (lo + (value - lowerTemp) / (upperTemp - lowerTemp) * (hi - lo)).round.toInt
      }

      Color(
        interpolate(lowerColor.red, upperColor.red),
        interpolate(lowerColor.green, upperColor.green),
        interpolate(lowerColor.blue, upperColor.blue)
      )
    }
  }

  /**
    * @param temperatures Known temperatures
    * @param colors Color scale
    * @return A 360×180 image where each pixel shows the predicted temperature at its location
    */
  def visualize(temperatures: Iterable[(Location, Temperature)], colors: Iterable[(Temperature, Color)]): Image = {
    val width = 360
    val height = 180

    val coords = for {
      y <- 0 until height
      x <- 0 until width
    } yield (x, y)

    val pixels = coords
      .map({ case (x, y) => Location(height / 2 - y, x - width / 2) })
      .map(predictTemperature(temperatures, _))
      .map(interpolateColor(colors, _))
      .map(color => Pixel(color.red, color.green, color.blue, 255))
      .toArray

    Image(width, height, pixels)
  }

}

