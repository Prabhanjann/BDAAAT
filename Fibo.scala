import scala.io.StdIn;

object Fibo{
    def main(args : Array[String]) = Unit{
        var a : Int = 1;
        var b : Int = 1;
        var c : Int = 2;
        var n : Int = 0;

        println("Enter the number of terms: ");
        n = StdIn.readInt();

        if(n >= 1)
            println(a);

        if(n >= 2)
            println(b);

        for(i <- 3 to n){
            c = a + b;
            a = b;
            b = c;
            println(c);
        }
    }
}