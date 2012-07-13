using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Miner
{
  public class Score
  {
    public int Value { get; private set; }

    private int lambdasCollected;

    internal void RobotKilled(int x, int y)
    {
      this.Value = 0;
    }

    internal void Abort()
    {
      this.Value += lambdasCollected * 25;
    }

    internal void Win()
    {
      this.Value += lambdasCollected * 50;
    }

    internal void LabmdaCollected()
    {
      this.Value += 25;
      this.lambdasCollected++;
    }

    internal void Move()
    {
      this.Value--;
    }
  }
}
