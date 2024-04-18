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

package fi.vtt.noen.mfw.bundle.common;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;

import java.util.Properties;

/**
 * Base class for createing OSGI bundleactivators for the plugins.
 *
 * @author Teemu Kanstren
 */
public abstract class BaseActivator implements BundleActivator {
  protected final Logger log;

  protected BaseActivator(Logger log) {
    this.log = log;
  }

  protected void registerPlugin(BundleContext bc, KnowledgeSource plugin, Properties props, String name) throws Exception {
    String[] names = new String[2];
    names[0] = KnowledgeSource.class.getName();
    names[1] = name;
    bc.registerService(names, plugin, props);
  }


}
