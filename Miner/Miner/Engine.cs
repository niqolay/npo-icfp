﻿using System;
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
        var m = lines[0].Count();
        var n = lines.Count();
        var newMap = new Map(n, m);
        for (int i = 0; i < newMap.n; i++)
            for (int j = 0; j < newMap.m; j++)
            {
                var code = lines[i][j];
                var element = CreateObjectByCode(code);
                element.Map = newMap;
                element.x = i;
                element.y = j;
                newMap.Objects[i, j] = element;
            }
        return newMap;
    }

    private GameObject CreateObjectByCode(char code)
    {
        switch (code)
        {
            case 'R': return new Robot();
            case 'L': return new ClosedLift();
            case 'O': return new OpenedLift();
            case '*': return new Rock();
            case '#': return new Wall();
            case ' ': return GameObject.Empty;
            case '\\': return new Lambda();
            case '.': return new Grass();
        }
        return null;
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
