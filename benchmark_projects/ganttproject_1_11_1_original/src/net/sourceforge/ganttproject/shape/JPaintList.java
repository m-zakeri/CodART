package net.sourceforge.ganttproject.shape;
/*
*@author Etienne L'kenfack (etienne.lkenfack@itcogita.com)
*/

import java.awt.*;
import javax.swing.*;

public class JPaintList extends JList
{
  public JPaintList(Paint[] list)
  {
    super(list);
    setCellRenderer(new PaintCellRenderer());
    setSelectedIndex(0);
  }

  public Paint getSelectedPaint()
  {
    return (Paint)getSelectedValue();
  }
}

