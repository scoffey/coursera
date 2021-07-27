package observatory

import com.sksamuel.scrimage.nio.PngWriter
import org.slf4j.LoggerFactory

import java.io.File

object Main extends App {

  val logger = LoggerFactory.getLogger(getClass.getName.stripSuffix("$"))

  def precalculateGrids(years: Iterable[Year]): Map[Year, GridLocation => Temperature] = {
    val sdf = Extraction.getStationsDataFrame()
    years.map(year => {
      logger.info(s"Calculating average local temperatures for year $year...")
      val temperatures = Extraction.getLocalAverageTemperatures(year, sdf)
      logger.info(s"Calculating temperature grid for year $year...")
      (year, Manipulation.makeGrid(temperatures))
    }).toMap
  }

  def imageGeneratorForLayer(layer: Layer)(year: Year, tile: Tile, deviation: GridLocation => Temperature): Unit = {
    val dir = new File(s"target/${layer.layerName.id}/$year/${tile.zoom}")
    if (!dir.exists()) {
      dir.mkdirs()
    }

    val file = new File(dir.getPath + s"/${tile.x}-${tile.y}.png")
    if (!file.exists()) {
      logger.info("Generating image: " + file.getAbsolutePath)
      val image = Visualization2.visualizeGrid(deviation, layer.colorScale, tile)
      image.output(file)(PngWriter())
    }
  }

  def generateAllImages(): Unit = {
    val tLayer = Interaction2.availableLayers.find(_.layerName == LayerName.Temperatures).get
    val dLayer = Interaction2.availableLayers.find(_.layerName == LayerName.Deviations).get

    // assuming the temperatures layer includes all the years of the other
    logger.info("Pre-calculating temperature grids for all years in " + tLayer.bounds)
    val grids = precalculateGrids(tLayer.bounds)

    logger.info("Computing temperatures layer")
    Interaction.generateTiles(grids.view, imageGeneratorForLayer(tLayer))

    logger.info("Computing normal temperatures")
    val gridSelection = (1975 to 1989).map(grids)
    val normals = Manipulation.makeCoordsMap(gridLocation => {
      // optimization of Manipulation.average with precalculated grids
      val temperatures = gridSelection.view.map(_(gridLocation))
      temperatures.sum / temperatures.size
    })

    logger.info("Computing deviations layer")
    Interaction.generateTiles(dLayer.bounds.view.map(year => {
      // optimization of Manipulation.deviation with precalculated grids
      val deviations = Manipulation.makeCoordsMap(gridLocation => {
        grids(year)(gridLocation) - normals(gridLocation)
      })
      (year, deviations)
    }), imageGeneratorForLayer(dLayer))

    logger.info("Done!")
  }

  // Main program (can take 1h+ to run)
  generateAllImages()
}
