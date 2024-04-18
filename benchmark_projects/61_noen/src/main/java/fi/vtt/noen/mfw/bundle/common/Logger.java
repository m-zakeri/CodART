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

import org.slf4j.LoggerFactory;
import sf.net.sinve.trace.Trace;
import sf.net.sinve.trace.data.Param;

/**
 * A wrapper for all logging to enable one to hack the provider and trace creation independent of the actual logging framework.
 *
 * @author Teemu Kanstren
 */
public class Logger extends Trace {
  private final org.slf4j.Logger log;

  public Logger(String name) {
    super(name);
    this.log = LoggerFactory.getLogger(name);
  }

  public Logger(Class aClass) {
    super(aClass);
    this.log = LoggerFactory.getLogger(aClass);
  }

  @Override
  public void start(String name, Param... params) {
    log.debug("Started :"+name);
  }

  @Override
  public void complete(String name, Param... params) {
    super.complete(name, params);
    log.debug("Completed :"+name);
  }

  @Override
  public void debug(String s) {
    log.debug(s);
  }

  @Override
  public void debug(String s, Throwable throwable) {
    log.debug(s, throwable);
  }

  @Override
  public void info(String s) {
    log.info(s);
  }

  @Override
  public void info(String s, Throwable throwable) {
    log.info(s, throwable);
  }

  @Override
  public void error(String s) {
    log.error(s);
  }

  @Override
  public void error(String s, Throwable throwable) {
    log.error(s, throwable);
  }
}
