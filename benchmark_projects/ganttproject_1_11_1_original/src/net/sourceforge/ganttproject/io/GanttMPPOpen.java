/*
 * file:       GanttMPPOpen.java
 * author:     Jon Iles
 * copyright:  (c) Tapster Rock Limited 2005
 * date:       10/01/2005
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
import java.io.InputStream;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.GanttTree;

import com.tapsterrock.mpp.MPPFile;


/**
 * This class implements the mechanism used to import Microsoft Project
 * data from an MPP file into the GanttProject application.
 */
public class GanttMPPOpen extends GanttMPXJOpen
{
   /**
    * Constructor.
    */
   public GanttMPPOpen (GanttTree tasks, GanttProject project)
   {
      super (tasks, project);
   }

   /**
    * @see GanttMPXJOpen#load(java.io.File)
    */
   public boolean load (File file)
   {
      return (load(MPPFile.class, file, null));
   }

   /**
    * @see GanttMPXJOpen#load(InputStream is)
    */
   public boolean load (InputStream is)
   {
      return (load(MPPFile.class, null, is));
   }
}
