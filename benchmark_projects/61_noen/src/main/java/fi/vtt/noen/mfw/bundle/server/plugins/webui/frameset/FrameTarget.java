/*
 * Copyright (C) 2010-2011 VTT Technical Research Centre of Finland.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

package fi.vtt.noen.mfw.bundle.server.plugins.webui.frameset;

import org.apache.wicket.IClusterable;
import org.apache.wicket.Page;


/**
 * The right hand side of the bottom frame.
 * base borrowed from wicket examples.
 */
public final class FrameTarget implements IClusterable {
  private static final long serialVersionUID = 1L;

  private Class<? extends Page> frameClass;

  public FrameTarget() {
  }

  public <C extends Page> FrameTarget(Class<C> frameClass) {
    this.frameClass = frameClass;
  }

  public Class<? extends Page> getFrameClass() {
    return frameClass;
  }

  public <C extends Page> void setFrameClass(Class<C> frameClass) {
    this.frameClass = frameClass;
  }
}