/*
 * file:       GanttMPXSaver.java
 * author:     Jon Iles
 * copyright:  (c) Tapster Rock Limited 2005
 * date:       04/02/2005
 */

/*
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by the
 * Free Software Foundation; either version 2.1 of the License, or (at your
 * option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
 * License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

package net.sourceforge.ganttproject.io;

import java.io.File;

import net.sourceforge.ganttproject.GanttResourcePanel;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.IGanttProject;

import com.tapsterrock.mpx.MPXFile;

/**
 * This class allows Gantt Project data to be saved as an MPX file.
 */
public class GanttMPXSaver extends GanttMPXJSaver
{
   /**
    * @see GanttMPXJSaver#GanttMPXJSaver(IGanttProject, GanttTree, GanttResourcePanel)
    */
   public GanttMPXSaver (IGanttProject project, GanttTree tree, GanttResourcePanel resources)
   {
      super (project, tree, resources);
   }
   
   /**
    * @see GanttMPXJSaver#save(File, MPXFile)
    */   
   public void save (File file)
   {
      try
      {
         save(file, new MPXFile ());
      }
      
      catch (Exception ex)
      {
         System.out.println (ex);
      }
   }
}
