package observatory

import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

import java.io.InputStream
import java.time.LocalDate
import scala.io.Source

/**
  * 1st milestone: data extraction
  */
object Extraction extends ExtractionInterface {

  val spark: SparkSession =
    SparkSession
      .builder()
      .appName("Observatory Capstone Project Data Extraction")
      .master("local")
      .getOrCreate()

  val temperaturesSchema: StructType = new StructType()
    .add("STN", StringType, true)
    .add("WBAN", StringType, true)
    .add("Month", IntegerType, true)
    .add("Day", IntegerType, true)
    .add("Fahrenheit", DoubleType, true)

  val stationsSchema: StructType = new StructType()
    .add("STN", StringType, true)
    .add("WBAN", StringType, true)
    .add("Latitude", DoubleType, true)
    .add("Longitude", DoubleType, true)

  /**
    * @param year             Year number
    * @param stationsFile     Path of the stations resource file to use (e.g. "/stations.csv")
    * @param temperaturesFile Path of the temperatures resource file to use (e.g. "/1975.csv")
    * @return A sequence containing triplets (date, location, temperature)
    */
  def locateTemperatures(year: Year, stationsFile: String, temperaturesFile: String): Iterable[(LocalDate, Location, Temperature)] = {
    val sdf = getDataFrame(stationsFile, stationsSchema)
      .na.drop(Seq("Latitude", "Longitude"))
    val tdf = getDataFrame(temperaturesFile, temperaturesSchema)
      .na.drop(Seq("Fahrenheit"))
      .where("Month <> 0")
      .where("Day <> 0")

    def fahrenheitToCelsius(f: Double): Temperature = (f - 32) * 5 / 9.0

    sdf
      .join(tdf, List("STN", "WBAN"))
      .select("Month", "Day", "Latitude", "Longitude", "Fahrenheit")
      .collect()
      .map(row => (
        LocalDate.of(year, row.getAs[Int]("Month"), row.getAs[Int]("Day")),
        Location(row.getAs[Double]("Latitude"), row.getAs[Double]("Longitude")),
        fahrenheitToCelsius(row.getAs[Double]("Fahrenheit"))
      ))
  }

  /**
    * @param records A sequence containing triplets (date, location, temperature)
    * @return A sequence containing, for each location, the average temperature over the year.
    */
  def locationYearlyAverageRecords(records: Iterable[(LocalDate, Location, Temperature)]): Iterable[(Location, Temperature)] = {
    spark.sparkContext.parallelize(records.toSeq).map({
      case (_, location, temp) => (location, temp)
    }).aggregateByKey((0.0, 0))(
      (accum, value) => (accum._1 + value, accum._2 + 1),
      (accum1, accum2) => (accum1._1 + accum2._1, accum1._2 + accum2._2)
    ).mapValues({
      case (sum, count) => sum / count
    }).collect()
  }

  def getDataFrame(fileName: String, schema: StructType): DataFrame = {

    def parseInt(s: String): Int = if (s.isEmpty) 0 else s.toInt

    def parseDouble(s: String): Double = if (s.isEmpty) Double.NaN else s.toDouble

    def parseValue(s: String, dataType: DataType): Any = {
      if (dataType == DoubleType) parseDouble(s)
      else if (dataType == IntegerType) parseInt(s)
      else s
    }

    val fileStream: InputStream = Source.getClass.getResourceAsStream(fileName)
    val rows = Source.fromInputStream(fileStream, "utf-8").getLines().map(line => {
      val records = line.trim.split(",", schema.length)
      Row.fromSeq(records.zip(schema.fields).map(pair => parseValue(pair._1, pair._2.dataType)))
    })
    spark.createDataFrame(spark.sparkContext.parallelize(rows.toSeq), schema)
  }

  /** Main function */
  def main(args: Array[String]): Unit = {
    val records = locateTemperatures(1975, "/stations.csv", "/1975.csv")
    val avgs = locationYearlyAverageRecords(records)
    println(avgs.mkString("\n"))
    spark.close()
  }
}
