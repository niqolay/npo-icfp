using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace Miner
{
  public class Map
  {
    public GameObject[,] Objects { get; private set; }    

    public Map(int n, int m)
    {
      this.n = n;
      this.m = m;
      this.Objects = new GameObject[n, m];
    }

    public int n { get; set; }

    public int m { get; set; }

    internal void RobotKilled(int x, int y)
    {
      Debug.WriteLine("Robot has just been killed by rock");
      this.Objects[x, y] = new DeadRobot();
    }
  }
}
