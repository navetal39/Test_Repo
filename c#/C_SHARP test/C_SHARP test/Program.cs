using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace C_SHARP_test
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] arr=new int[7];
            for(int i=1; i<=7; i++)
            {
                arr[i-1]=i;
            }
            foreach (int i in arr)
            {
                int b = i * i * i;
                Console.WriteLine(b);
            }
        }
    }
}
