package calculator

object Polynomial extends PolynomialInterface:
  def computeDelta(a: Signal[Double], b: Signal[Double],
      c: Signal[Double]): Signal[Double] = Signal { b() * b() - 4 * a() * c() }

  def computeSolutions(a: Signal[Double], b: Signal[Double],
      c: Signal[Double], delta: Signal[Double]): Signal[Set[Double]] = Signal {
    val minusb = -b()
    val d = delta()
    val denom = 2 * a()

    if (denom == 0)
      Set(c() / minusb)  // unless b == 0 (infinite solutions)
    else if (d < 0)
      Set()
    else if (d == 0)
      Set(minusb / denom)
    else
      Set(
        (minusb + Math.sqrt(d)) / denom,
        (minusb - Math.sqrt(d)) / denom
      )
  }
