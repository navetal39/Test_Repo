using System;
//using System.Collections.Generic;
using System.Linq;
using System.Text;
using Unit4.CollectionsLib;

namespace Hanoi
{
    /// <summary>
    /// A class that allows you to make the famous game, "Hanoi Towers"
    /// </summary>
    class HanoiTowers
    {
        private Stack<int>[] poles;
        private int[] Hights;
        private int discNum;
        public const int PN = 3;

        /// <summary>
        /// Creates a new set for the game, with 3 towers and an ammount of discs between 3 and 10
        /// </summary>
        /// <param name="numOfDiscs">the ammount of discs in the game</param>
        public HanoiTowers(int numOfDiscs)
        {
            if (!(numOfDiscs >= 3 && numOfDiscs <= 10))
                numOfDiscs = PN;
            discNum = numOfDiscs;
            this.poles = new Stack<int>[PN];
            this.Hights=new int[PN];
            int i;
            for (i = 0; i < PN; i++)
            {
                this.poles[i] = new Stack<int>();
                Hights[i] = 0;
            }
            for (i = numOfDiscs; i > 0; i--)
            {
                poles[0].Push(i);
            }
            Hights[0] = numOfDiscs;
        }
        /// <summary>
        /// If possible, moves the top disc from one tower to another and returning true. returning false otherwise.
        /// </summary>
        /// <param name="fromPoleNum">The number of the pole you wish to take the disc from</param>
        /// <param name="toPoleNum">The number of the pole you wish to add the disc to</param>
        /// <returns>Was the move successfull or not</returns>
        public bool MoveDisc(int fromPoleNum, int toPoleNum)
        {
            fromPoleNum--;
            toPoleNum--;
            if (fromPoleNum <= 3 && fromPoleNum >= 0 && toPoleNum <= 3 && toPoleNum >= 0)
                if (!poles[fromPoleNum].IsEmpty() && poles[toPoleNum].Top() > poles[fromPoleNum].Top())
                {
                    poles[toPoleNum].Push(poles[fromPoleNum].Pop());
                    Hights[fromPoleNum]--;
                    Hights[toPoleNum]++;
                    return true;
                }
                else
                    return false;
            else
                return false;
        }
        /// <summary>
        /// Returns the ammount of discs on all poles
        /// </summary>
        /// <returns>The ammount of all discs</returns>
        public int GetNumOfDiscs()
        {
            return this.discNum;
        }
        /// <summary>
        /// Returns the ammount of discs on a specific pole
        /// </summary>
        /// <param name="poleNum">The number of the pole you wish to check</param>
        /// <returns>The ammount of discs on the chosen pole</returns>
        public int GetNumOfDiscs(int poleNum)
        {
            poleNum--;
            return this.Hights[poleNum];
        }
        /// <summary>
        /// Returns the top disc on a specific pole
        /// </summary>
        /// <param name="poleNum">The number of the pole you wish to check</param>
        /// <returns>The highest disc on the chosen pole</returns>
        public int GetSizeTopDisk(int poleNum)
        {
            poleNum--;
            if (!this.poles[poleNum].IsEmpty())
                return this.poles[poleNum].Top();
            else
                return 0;
        }
        /// <summary>
        /// Returns True if a specific pole is empty, or false otherwise
        /// </summary>
        /// <param name="poleNum">The number of the pole you wish to check</param>
        /// <returns>Is the pole empty of discs or not</returns>
        public bool IsEmpty(int poleNum)
        {
            poleNum--;
            return this.poles[poleNum].IsEmpty();
        }
        /// <summary>
        /// Returns the state of the game in a form of a designed string
        /// </summary>
        /// <returns>The state of the game in an enhanced view</returns>
        public override string ToString()
        {
            string returning = "";
            int i, j, numTemp, remaining;
            Stack<int> stackTemp = new Stack<int>();
            for (i = 0; i < PN; i++)
            {
                remaining = 20;
                returning += "||";
                returning += System.Environment.NewLine;
                returning += "||";
                while (!this.poles[i].IsEmpty())
                    stackTemp.Push(poles[i].Pop());
                while (!stackTemp.IsEmpty())
                {
                    numTemp = stackTemp.Pop();
                    returning += numTemp;
                    returning += "-";
                    remaining -= 2;
                    if (numTemp == 10)
                        remaining--;
                    this.poles[i].Push(numTemp);
                }
                for (j=remaining; j >= 0; j--)
                    returning += "-";
                returning+=("#"+(i+1));
                returning += System.Environment.NewLine;
                returning += "||";
                returning += System.Environment.NewLine;
                returning += System.Environment.NewLine;
            }
            return returning;
        }
    }
}
