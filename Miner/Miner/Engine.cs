using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace Miner
{
  class Engine
  {
    public Map map { get; private set; }

    public Engine(string mapFile)
    {
      //map = new Map(n, m);
      //FillEmpty();
      //map.Objects[0, 0] = new Robot() { Map = map, x = 0, y = 0};
      //map.Objects[3, 3] = new Rock() { Map = map, x = 3, y = 3 };
        map = LoadMap(mapFile);
    }

    private Map LoadMap(string mapFile)
    {
        var lines = File.ReadAllLines(mapFile);
        var m = lines.Count();
        var n = lines[0].Count();
        var newMap = new Map(n, m);
        for (int i = 0; i < map.n; i++)
            for (int j = 0; j < map.m; j++)
            {
                var code = lines[i][j];
                newMap.Objects[i, j] = CreateObjectByCode(code, map);
            }
        return newMap;
    }

    private GameObject CreateObjectByCode(char code, Map newMap)
    {
        switch (code)
        {
            case 'R': return new Robot() { Map = newMap };
            case 'L': return new ClosedLift() { Map = newMap };
            case 'O': return new OpenedLift() { Map = newMap };
            case '*': return new Rock() { Map = newMap };
            case '#': return new Wall() { Map = newMap };
            case ' ': return new Robot() { Map = newMap };
            case '\\': return new Robot() { Map = newMap };
        }
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
