using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

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
  }
}
