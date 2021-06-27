package reductions

import scala.annotation
import org.scalameter.*

import scala.annotation.tailrec

object ParallelParenthesesBalancingRunner:

  @volatile var seqResult = false

  @volatile var parResult = false

  val standardConfig = config(
    Key.exec.minWarmupRuns := 40,
    Key.exec.maxWarmupRuns := 80,
    Key.exec.benchRuns := 120,
    Key.verbose := false
  ) withWarmer(Warmer.Default())

  def main(args: Array[String]): Unit =
    val length = 100000000
    val chars = new Array[Char](length)
    val threshold = 10000
    val seqtime = standardConfig measure {
      seqResult = ParallelParenthesesBalancing.balance(chars)
    }
    println(s"sequential result = $seqResult")
    println(s"sequential balancing time: $seqtime")

    val fjtime = standardConfig measure {
      parResult = ParallelParenthesesBalancing.parBalance(chars, threshold)
    }
    println(s"parallel result = $parResult")
    println(s"parallel balancing time: $fjtime")
    println(s"speedup: ${seqtime.value / fjtime.value}")

object ParallelParenthesesBalancing extends ParallelParenthesesBalancingInterface:

  /** Returns `true` iff the parentheses in the input `chars` are balanced.
   */
  def balance(chars: Array[Char]): Boolean = {
    def charDelta(c: Char): Int = c match {
      case '(' => 1
      case ')' => -1
      case _ => 0
    }
    @tailrec
    def balanceCount(chars: Array[Char], openCount: Int): Boolean = {
      if (openCount < 0)
        false
      else if (chars.isEmpty)
        openCount == 0
      else
        balanceCount(chars.tail, openCount + charDelta(chars.head))
    }
    balanceCount(chars, 0)
  }

  /** Returns `true` iff the parentheses in the input `chars` are balanced.
   */
  def parBalance(chars: Array[Char], threshold: Int): Boolean = {

    def traverse(idx: Int, until: Int, openCount: Int, closeCount: Int): (Int, Int) = {
      if (idx >= until)
        (openCount, closeCount)
      else
        chars(idx) match {
          case '(' => traverse(idx + 1, until, openCount + 1, closeCount)
          case ')' => {
            if (openCount > 0)
              traverse(idx + 1, until, openCount - 1, closeCount)
            else
              traverse(idx + 1, until, openCount, closeCount + 1)
          }
          case _ => traverse(idx + 1, until, openCount, closeCount)
        }
    }

    def reduce(from: Int, until: Int): (Int, Int) = {
      if (until - from <= threshold)
        traverse(from, until, 0, 0)
      else {
        val mid = from + (until - from) / 2
        val ((lo, lc), (ro, rc)) = parallel(reduce(from, mid), reduce(mid, until))

        if (lo > rc)
          (lo + ro - rc, lc)
        else
          (ro, lc + rc - lo)
      }
    }

    reduce(0, chars.length) == (0, 0)
  }

  // For those who want more:
  // Prove that your reduction operator is associative!

