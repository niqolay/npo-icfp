using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Miner
{
  class Engine
  {
    public Map map { get; private set; }

    public Engine(int m, int n)
    {
      map = new Map(n, m);
      FillEmpty();
      map.Objects[0, 0] = new Robot() { Map = map, x = 0, y = 0};
      map.Objects[3, 3] = new Rock() { Map = map, x = 3, y = 3 };
    }

    private void ForEach(Action<GameObject> action)
    {
            for (int i = 0; i < map.n; i++)
              for (int j = 0; j < map.m; j++)
              {
                action(map.Objects[i, j]);
              }
    }

    public void Do(char action)
    {
      ForEach(e => e.Move(action));
      ForEach(e => e.IsMovedThisTurn = false);
    }

    private void FillEmpty()
    {
      for (int i = 0; i < map.n; i++)
        for (int j = 0; j < map.m; j++)
          map.Objects[i, j] = GameObject.Empty;
    }
  }
}
