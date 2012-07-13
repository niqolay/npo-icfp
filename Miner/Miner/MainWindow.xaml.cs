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

namespace Miner
{
  /// <summary>
  /// Interaction logic for MainWindow.xaml
  /// </summary>
  public partial class MainWindow : Window
  {

      Engine engine;

    public MainWindow()
    {
      System.Diagnostics.Trace.Listeners.Add(new System.Diagnostics.ConsoleTraceListener());
      InitializeComponent();                 
    }

    private void Paint()
    {      
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
      if (e.Key == Key.D)
        engine.Do('D');
      else if (e.Key == Key.A)
        engine.Do('U');
      else if (e.Key == Key.W)
        engine.Do('L');
      else if (e.Key == Key.S)
        engine.Do('R');
      Paint();
    }

    private void Button_Click(object sender, RoutedEventArgs e)
    {
        this.engine = new Engine(@"maps\contest10.map");
        this.Paint();
    } 
  }
}
