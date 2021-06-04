package quickcheck

import org.scalacheck.*
import Arbitrary.*
import Gen.*
import Prop.forAll

abstract class QuickCheckHeap extends Properties("Heap") with IntHeap :
  lazy val genHeap: Gen[H] = for {
    x <- arbitrary[Int]
    h <- oneOf(const(empty), genHeap)
  } yield insert(x, h)

  given Arbitrary[H] = Arbitrary(genHeap)

  // The minimum of a single element heap is its only element
  property("min1") = forAll { (a: Int) =>
    val h = insert(a, empty)
    findMin(h) == a
  }

  // For any heap, adding the minimal element, and then finding it, should return such element
  property("gen1") = forAll { (h: H) =>
    val m = if isEmpty(h) then 0 else findMin(h)
    findMin(insert(m, h)) == m
  }

  // If you insert any two elements into an empty heap, finding the minimum of the resulting heap
  // should get the smallest of the two elements back.
  property("min2") = forAll { (a: Int, b: Int) =>
    val h = insert(b, insert(a, empty))
    findMin(h) == a.min(b)
  }

  // If you insert an element into an empty heap, then delete the minimum, the resulting heap
  // should be empty.
  property("deleteMin1") = forAll { (a: Int) =>
    val h = insert(a, empty)
    deleteMin(h) == empty
  }

  // Given any heap, you should get a sorted sequence of elements when continually finding and
  // deleting minima. (Hint: recursion and helper functions are your friends.)
  property("deleteMin2") = forAll { (h: H) =>
    def helper(heap: H, accum: List[Int]): List[Int] = {
      if (isEmpty(heap)) Nil else findMin(heap) :: helper(deleteMin(heap), accum)
    }
    val list = helper(h, Nil)
    list.sorted == list
  }

  // Finding a minimum of the melding of any two heaps should return a minimum of one or the other.
  property("meld1") = forAll { (h1: H, h2: H) =>
    val m = findMin(meld(h1, h2))
    (isEmpty(h1) || m == findMin(h1)) || (isEmpty(h2) || m == findMin(h2))
  }

  // Deleting the minimum of a 3-element heap should result in a heap with the greatest 2 elements
  // of the 3. (Additional property that makes bogus heaps fail the tests.)
  property("deleteMin3") = forAll{ (a: Int, b: Int, c: Int) =>
    val list = List(a, b, c).sorted.tail
    deleteMin(insert(c, insert(b, insert(a, empty)))) == insert(list.head, insert(list.tail.head, empty))
  }
