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

package fi.vtt.noen.mfw.bundle.probe.plugins.measurement;

import fi.vtt.noen.mfw.bundle.common.Logger;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;

/**
 * Creates threads for the thread pool. Delegates to Executors.detaultThreadFactory with the difference that
 * all threads created as defined as daemon threads.
 *
 * @author Teemu Kanstren
 */
public class MeasurementThreadFactory implements ThreadFactory {
  private final static Logger log = new Logger(MeasurementThreadFactory.class);
  private final ThreadFactory delegate = Executors.defaultThreadFactory();

  public static void main(String[] args) throws Exception {
    ScheduledThreadPoolExecutor executor = new ScheduledThreadPoolExecutor(1, new MeasurementThreadFactory());
    executor.scheduleAtFixedRate(new Runnable() {
      public void run() {
        System.out.println("hello");
      }
    }, 0, 100, TimeUnit.MILLISECONDS);
    Thread.sleep(500);
    
  }

  public Thread newThread(Runnable r) {
    log.debug("new thread created");
    Thread t = delegate.newThread(r);
    t.setDaemon(true);
    return t;
  }
}
