using System;
//using System.Collections.Generic;
using System.Linq;
using System.Text;
using Unit4.CollectionsLib;

namespace מיון_בסיס
{
    class Program
    {
        public static void RadixSort(int[] arr)//O(1)
        {
            int max = arr[0];
            foreach (int x in arr)
            {
                if (x > max)
                    max = x;
            }
            /*int temp = max, i=1;
            while (temp%10!=0)
            {
                temp/=10;
                i++;
            }*/
            RadixSort(arr, 10, max);//1
        }
        public static void RadixSort(int[] arr, int charNum, int highest)//O(n*l) when n is the length of the array and l is the number of digits in the largest number in the array
        {
            if (charNum <= highest * 10)//l
            {
                Queue<int>[] queue = new Queue<int>[10];//1(l)
                int i, j;//1(l)

                for (i = 0; i < 10; i++)//1,10,10(l,10l,10l)
                    queue[i] = new Queue<int>();//1(l)

                foreach (int num in arr)//n(n*l)
                {
                    queue[(num % charNum) / (charNum / 10)].Insert(num);//1(n)(n*l)
                }

                i = 0;//1(l)
                j = 0;//1(l)
                while (i < arr.Length)//n(n*l)
                {
                    while (!queue[j].IsEmpty())//1(n)(n*l)
                    {
                        arr[i] = queue[j].Remove();//1(n)(n*l)
                        i++;//1(n)(n*l)
                    }
                    j++;//1(n)(n*l)
                }
                RadixSort(arr, charNum * 10, highest);//1(l)
            }
        }

        const int L = 16, MAX=1000;

        static void Main(string[] args)
        {
            int[] test = new int[L];
            Random R = new Random();
            int i;
            Console.Write("Original array: ");
            for (i = 0; i < L; i++)
            {
                test[i] = R.Next(MAX+1);
                Console.Write(test[i] + " ");
            }


            Console.WriteLine();
            Console.Write("Sorted array: ");
            RadixSort(test);
            foreach (int x in test)
                Console.Write(x + " ");
            Console.WriteLine();
        }
    }
}
