import scala.annotation.tailrec
import scala.collection.mutable

def factorial(i: Int, lowerLimit: Int = 1): Int = {
  assert(lowerLimit >= 0)
  assert(i >= lowerLimit)

  @tailrec
  def factorial(acc: Int, i:Int): Int = {
    if(i <= lowerLimit) {
      return acc
    }
    factorial(acc*i, i-1)
  }
  factorial(1, i)
}

def combination(n: Int, r: Int, repeatAllowed: Boolean = false) = {
  if(!repeatAllowed) {
    factorial(n, n-r)/factorial(r)
  } else {
    factorial(r+n-1, n-1)/factorial(r)
  }
}

combination(12,4,false)

//https://rosettacode.org/wiki/Combinations_with_repetitions#Scala
val N  = 1 to 12
N.combinations(4).toList.length
for(x <- List.fill(4)(N).flatten.combinations(4)) {
  println(x mkString("."))
}
List.fill(2)("ABC").flatten.combinations(2).toList.map(l => l.mkString)
