using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace Miner
{
  public class Robot : GameObject
  {
    public override char Code { get { return 'R'; } }

    protected override void InternalMove(char action)
    {
      switch (action)
      {
        case 'R':
          {
            MoveTo(x + 1, y);
            break;
          }
        case 'L':
          {
            MoveTo(x - 1, y);
            break;
          }
        case 'U':
          {
            MoveTo(x, y - 1);
            break;
          }
        case 'D':
          {
            MoveTo(x, y + 1);
            break;
          }
        case 'W':
          {
            break;
          }
      }
    }

    private void MoveTo(int newX, int newY)
    {
      string reason;
      if (this.CanGo(newX, newY, out reason))
        this.Move(newX, newY);
      else
        Debug.WriteLine(string.Format("Robot can not move: {0}", reason));
    }

    private void Move(int newX, int newY)
    {
      // move rock on go left
      if (newY < this.y && map.Objects[newX, newY] is Rock)
      {
        var rock = map.Objects[newX, newY];
        map.Objects[newX, newY - 1] = rock;
        rock.x = newX;
        rock.y = newY - 1;
        map.Objects[newX, newY] = GameObject.Empty;
      }
      // move rock on go right
      if (newY > this.y && map.Objects[newX, newY] is Rock)
      {
        var rock = map.Objects[newX, newY];
        map.Objects[newX, newY + 1] = rock;
        rock.x = newX;
        rock.y = newY + 1;
        map.Objects[newX, newY] = GameObject.Empty;
      }
      if (map.Objects[newX, newY] is Lambda)
        this.score.LabmdaCollected();
      if (map.Objects[newX, newY] is OpenedLift)
        this.score.Win();
      DoMove(newX, newY);
      Debug.WriteLine(string.Format("Moved to ({0}; {1})", x, y, newX, newY));
    }

    private bool CanGo(int newX, int newY, out string reason)
    {      
      if (!IsClear(newX, newY, out reason))
        return false;
      // go up or down, can't move rock.
      if (newY == this.y && map.Objects[newX, newY] is Rock)
      {
        reason = string.Format("Can't go to rock. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      // go left
      if (newY < this.y && map.Objects[newX, newY] is Rock && !(map.Objects[newX, newY - 1] is Empty))
      {
        reason = string.Format("Can't move rock to left. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      // go right;
      if (newY > this.y && map.Objects[newX, newY] is Rock && !(map.Objects[newX, newY + 1] is Empty))
      {
        reason = string.Format("Can't move rock to right. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      return true;
    }
  }
}
