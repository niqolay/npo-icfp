using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Miner
{
  public class Rock : GameObject
  {
    protected override void InternalMove(char action)
    {
      string dummy;
      var newX = x + 1;
      var newY = y;
      if (IsClear(newX, newY, out dummy) && map.Objects[newX, newY] is Empty )
      {
        DoMove(newX, newY);
        CheckRobotKilledByMe();
        return;
      }
      var belowX = x + 1;
      var belowY = y;
      var rightX = x;
      var rightY = y + 1;
      var rightBelowX = x + 1;
      var rightBelowY = y + 1;
      var leftBelowX = x + 1;
      var leftBelowY = y - 1;
      // Стоим на камне или лямбде и справа свободно.
      if (IsInBounds(belowX, belowY) && (map.Objects[belowX, belowY] is Rock || map.Objects[belowX, belowY] is Lambda))
      {

        if (IsInBounds(rightX, rightY) && map.Objects[rightX, rightY] is Empty)
        {

          if (IsInBounds(rightBelowX, rightBelowY) && map.Objects[rightBelowX, rightBelowY] is Empty)
          {
            DoMove(rightBelowX, rightBelowY);
            CheckRobotKilledByMe();
            return;
          }
        }
      }
      // Стоим на камне, справа занято хотя бы одно и слева свободно.
      if (IsInBounds(belowX, belowY) && (map.Objects[belowX, belowY] is Rock))
      {
        if (!(IsInBounds(belowX, belowY) && map.Objects[belowX, belowY] is Empty) ||
            !(IsInBounds(rightBelowX, rightBelowY) && map.Objects[rightBelowX, rightBelowY] is Empty))
          if (IsInBounds(leftBelowX, leftBelowY) && map.Objects[leftBelowX, leftBelowY] is Empty)
          {
            DoMove(leftBelowX, leftBelowY);
            CheckRobotKilledByMe();
            return;
          }
      }

    }

    private bool IsRobot(int checkX, int checkY)
    {
      return map.Objects[checkX, checkY] is Robot;
    }

    

    private void CheckRobotKilledByMe()
    {
      if (x < map.n - 1 && IsRobot(x + 1, y))
        map.RobotKilled(x + 1, y);
    }

    public override char Code
    {
      get { return '*'; }
    }
  }
}
