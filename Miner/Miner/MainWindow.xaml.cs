using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Timers;

namespace Miner
{
  /// <summary>
  /// Interaction logic for MainWindow.xaml
  /// </summary>
  public partial class MainWindow : Window
  {

    Engine engine;
    private Timer timer;
    private int currentPosition;

    public MainWindow()
    {
      System.Diagnostics.Trace.Listeners.Add(new System.Diagnostics.ConsoleTraceListener());
      InitializeComponent();
      this.timer = new Timer(500);
      this.timer.Elapsed += new ElapsedEventHandler(timer_Elapsed);
      this.Button_Click(this, new RoutedEventArgs());
    }

    void timer_Elapsed(object sender, ElapsedEventArgs e)
    {
      this.Dispatcher.Invoke(new Action(() =>
      {
        this.Commands.Focus();
        if (currentPosition < Commands.Text.Length)
        {
          Commands.CaretIndex = currentPosition;
          DoAction(Commands.Text[currentPosition]);
        }
        else
        {
          timer.Stop();
          currentPosition = 0;
        }
        currentPosition++;
      }));
    }

    private void Paint()
    {
      this.Score.Text = engine.score.Value.ToString();
      var stringMap = new StringBuilder();
      for (int i = 0; i < engine.map.n; i++)
      {
        for (int j = 0; j < engine.map.m; j++)
          stringMap.Append(engine.map.Objects[i, j].Code);
        stringMap.AppendLine();
      }
      this.Box.Text = stringMap.ToString();
    }

    private void Window_KeyDown(object sender, KeyEventArgs e)
    {
      char? action = null;
      if (e.Key == Key.Left)
        action = 'L';
      else if (e.Key == Key.Right)
        action = 'R';
      else if (e.Key == Key.Up)
        action = 'U';
      else if (e.Key == Key.Down)
        action = 'D';
      else if (e.Key == Key.Z)
        action = 'W';
      else if (e.Key == Key.X)
        action = 'A';
      if (action.HasValue)
      {
        DoAction(action.Value);
      }
    }

    private object locker = new object();

    private void DoAction(char action)
    {
      lock (this.locker)
      {
        var realAction = FixMyBadCoords(action);
        engine.Do(realAction);
        Log.Text += action;
        Paint();
      }
    }

    private char FixMyBadCoords(char action)
    {
      if (action == 'U')
        return 'L';
      if (action == 'D')
        return 'R';
      if (action == 'R')
        return 'D';
      if (action == 'L')
        return 'U';
      return action;
    }

    private void Button_Click(object sender, RoutedEventArgs e)
    {
      this.engine = new Engine(@"maps\contest5.map");
      this.Log.Text = string.Empty;
      this.Paint();
    }

    private void Play(object sender, RoutedEventArgs e)
    {
      this.timer.Start();
    }

    private void Pause(object sender, RoutedEventArgs e)
    {
      this.timer.Stop();
    }

    private void RadioButton_Checked(object sender, RoutedEventArgs e)
    {
      if (((RadioButton)sender).Tag != null)
      this.timer.Interval = int.Parse((string)((RadioButton)sender).Tag);
    }
  }
}
