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

package fi.vtt.noen.mfw.updater;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.osgi.framework.BundleException;

import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

/**
 * An updater service implementation to replace old instances of bundles in a running OSGI system.
 * TODO: Needs to be updated to handle all problems of real system, currently it is proof of concept level.
 *
 * @author Teemu Kanstren
 */
public class BundleUpdaterImpl implements BundleActivator, BundleUpdater {
  private BundleContext bc;

  public void start(BundleContext bc) throws Exception {
    this.bc = bc;
  }

  public void stop(BundleContext bundleContext) throws Exception {

  }

  //TODO remove port when a real comms mechanism is available
  public void update(String id, int port) {
    //TODO: make this pluggable and configurable for distributed stuff and P2P etc.
    try {
      Socket socket = new Socket("localhost", port);
      InputStream in = socket.getInputStream();
      bc.installBundle("noen://bundleserver/"+id, in);
    } catch (IOException e) {
      //TODO handling of errors here..
      e.printStackTrace();
    } catch (BundleException e) {
      e.printStackTrace();
    }

  }
}
