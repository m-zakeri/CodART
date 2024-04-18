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

package fi.vtt.noen.mfw.bundle.server.plugins.webui;

import fi.vtt.noen.mfw.bundle.common.Logger;
import org.apache.wicket.protocol.http.WicketFilter;

import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Used to hack around the classloader constraints in OSGI and Wicket.
 *
 * @author Teemu Kanstren
 */
public class WebUIWicketFilter extends WicketFilter {
  private final static Logger log = new Logger(WebUIWicketFilter.class);

  @Override
  public void init(FilterConfig config) throws ServletException {
    log.debug("initializing filter:"+config);
    try {
      super.init(config);
    } catch (ServletException e) {
      e.printStackTrace();
    }
    log.debug("initialized");
  }

  //this provides Wicket with a working classloader to create the web page objects via reflection, and while still
  //running inside OSGI.
  @Override
  protected ClassLoader getClassLoader() {
//    log.debug("getting classloader:"+this.getClass().getClassLoader());
    try {
      return this.getClass().getClassLoader();
    } catch (RuntimeException e) {
      e.printStackTrace();
      throw e;
    }
  }

/*
  @Override
  protected String getFilterPath(HttpServletRequest request) {
    return "/ui/";
  }
*/
  @Override
  public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
//    log.debug("filter request");
    HttpServletRequest httpReq = null;
    try {
      httpReq = (HttpServletRequest) request;
    } catch (Exception e) {
      e.printStackTrace();
    }
//    log.debug("filtering:"+httpReq.getPathInfo());
    super.doFilter(request, response, chain);
  }

  @Override
  public boolean doGet(HttpServletRequest servletRequest, HttpServletResponse servletResponse) throws ServletException, IOException {
//    log.debug("getting");
    try {
      return super.doGet(servletRequest, servletResponse);
    } catch (ServletException e) {
      e.printStackTrace();
      throw e;
    } catch (IOException e) {
      e.printStackTrace();
      throw e;
    }
  }
}
