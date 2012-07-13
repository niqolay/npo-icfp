using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace Miner
{
  public abstract class GameObject
  {
    public Map map { get; set; }
    public Score score { get; set; }
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
      if (!IsInBounds(newX, newY))
      {
        reason = string.Format("Out of bounds. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      if (map.Objects[newX, newY] is Wall)
      {
        reason = string.Format("can't go to wall. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      if (map.Objects[newX, newY] is ClosedLift)
      {
        reason = string.Format("can't go to closed lift. Current ({0}; {1}). Going to ({2}; {3})", x, y, newX, newY);
        return false;
      }
      return true;
    }

    protected bool IsInBounds(int newX, int newY)
    {
      return (newY >= 0 && newY < map.m && newX >= 0 && newX < map.n);
    }

    protected void DoMove(int newX, int newY)
    {
      map.Objects[this.x, this.y] = GameObject.Empty;
      this.x = newX;
      this.y = newY;
      map.Objects[this.x, this.y] = this;
    }
  }

  public class Empty : GameObject
  {
    protected override void InternalMove(char action)
    {
    }

    public override char Code { get { return ' '; } }
  }

  public class Grass : GameObject
  {
    protected override void InternalMove(char action)
    {
    }

    public override char Code { get { return '.'; } }
  }

  public class Wall : GameObject
  {
    protected override void InternalMove(char action)
    {
    }

    public override char Code { get { return '#'; } }
  }

  public class ClosedLift : GameObject
  {
    protected override void InternalMove(char action)
    {
      if (!map.Objects.OfType<Lambda>().Any())
      {
        map.Objects[this.x, this.y] = new OpenedLift() { map = map, x = x, y = y };
        Debug.WriteLine("Lift has just opened!!!");
      }

    }

    public override char Code { get { return 'L'; } }
  }

  public class OpenedLift : GameObject
  {
    protected override void InternalMove(char action)
    {

    }

    public override char Code { get { return 'O'; } }
  }

  public class Lambda : GameObject
  {
    protected override void InternalMove(char action)
    {

    }

    public override char Code { get { return '\\'; } }
  }

  public class DeadRobot : GameObject
  {
    protected override void InternalMove(char action)
    {

    }

    public override char Code { get { return '+'; } }
  }  
}
