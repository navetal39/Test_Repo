using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Hanoi
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Hello! Welcome to the game of Hanoi Towers!"+System.Environment.NewLine+"Enter the number of discs you wish to play with:");
            HanoiTowers game=new HanoiTowers(int.Parse(Console.ReadLine()));
            Console.WriteLine(System.Environment.NewLine+"You are now playing with " + game.GetNumOfDiscs() + " Discs");
            Console.WriteLine("The towers are ready. Have fun!"+System.Environment.NewLine);
            int action, tempNum1, tempNum2;
            bool quit=false;
            while ((!game.IsEmpty(1) || !game.IsEmpty(2))&&!quit)
            {
                Console.WriteLine("The poles:");
                Console.WriteLine(game);
                Console.WriteLine("What would you like to do? Pick a number:");
                Console.WriteLine("================================================================");
                Console.WriteLine("1: Move a disc");
                Console.WriteLine("2: Get the number of discs you play with");
                Console.WriteLine("3: Get the number of discs on a specific pole");
                Console.WriteLine("4: Get the size of the highest disc on a specific pole");
                Console.WriteLine("5: Quit the game");
                Console.WriteLine("================================================================");
                Console.Write("Your choice:");
                action = int.Parse(Console.ReadLine());
                switch (action)
                {
                    case 1:
                        Console.Write("Enter the number of pole you wish to take a disc from: ");
                        tempNum1 = int.Parse(Console.ReadLine());
                        Console.Write("Enter the number of pole you wish to move the disc to: ");
                        tempNum2 = int.Parse(Console.ReadLine());
                        if (game.MoveDisc(tempNum1, tempNum2))
                            Console.WriteLine("The move was successful");
                        else
                            Console.WriteLine("The move wasen't successful!");
                        break;
                    case 2:
                        Console.WriteLine("You are playing with " + game.GetNumOfDiscs() + " Discs");
                        break;
                    case 3:
                        Console.Write("Enter the number of the pole you wish to check: ");
                        tempNum1 = int.Parse(Console.ReadLine());
                        Console.WriteLine("There are " + game.GetNumOfDiscs(tempNum1) + " discs on pole number "+tempNum1);
                        break;
                    case 4:
                        Console.Write("Enter the number of the pole you wish to check: ");
                        tempNum1=int.Parse(Console.ReadLine());
                        Console.WriteLine("The highest (and smallest) disc on pole number "+tempNum1+" is "+game.GetSizeTopDisk(tempNum1));
                        break;
                    case 5:
                        quit = true;
                        break;
                    default:
                        Console.WriteLine("ERROR! Can't Identify the correct action! Please try again!");
                        break;
                }
                Console.WriteLine(System.Environment.NewLine);
            }
            if (quit)
                Console.WriteLine("Thank's for playing, and good luck next time!");
            else
                Console.WriteLine("Congratulations! You Won! Come again later to try again!");
        }
    }
}
