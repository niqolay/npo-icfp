using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace Miner
{
  public abstract class GameObject
  {
    public Map Map { get; set; }
    public int x { get; set; }
    public int y { get; set; }
    public bool IsMovedThisTurn { get; set; }
    public void Move(char action)
    {
      if (!this.IsMovedThisTurn)
      {
        this.IsMovedThisTurn = true;
        this.InternalMove(action);
      }
    }
    protected abstract void InternalMove(char action);

    public static GameObject Empty = new Empty();

    public abstract char Code { get; }

    protected bool IsClear(int newX, int newY, out string reason)
    {
      reason = "123";
      if (newY >= 0 && newY < Map.m && newX >= 0 && newX < Map.n)
        return true;
      reason = string.Format("Out of bounds. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
      return false;
    }

    protected void DoMove(int newX, int newY)
    {
      Map.Objects[this.x, this.y] = GameObject.Empty;
      this.x = newX;
      this.y = newY;
      Map.Objects[this.x, this.y] = this;
    }
  }

  public class Empty: GameObject
  {
    protected override void InternalMove(char action)
    {
    }

    public override char Code { get { return ' '; } }
  }

  public class Robot: GameObject
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
      DoMove(newX, newY);
       Debug.WriteLine(string.Format("Moved to ({0}; {1})", x, y, newX, newY));
    }

    private bool CanGo(int newX, int newY, out string reason)
    {
      //if (Map.Objects[newY, newX] is Empty || Map.Objects[newY, newX] is Lambda || Map.Objects[newY, newX] is Rock)      
      return IsClear(newX, newY, out reason);
    }    
  }

  public class Rock : GameObject
  {
    protected override void InternalMove(char action)
    {
      string dummy;
      if (IsClear(x + 1, y, out dummy))
        DoMove(x + 1, y);
    }

    public override char Code
    {
      get { return '*'; }
    }
  }
}
