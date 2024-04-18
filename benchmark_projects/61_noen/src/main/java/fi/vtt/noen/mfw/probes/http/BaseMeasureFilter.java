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

package fi.vtt.noen.mfw.probes.http;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

/**
 * Grabs all HTTP requests coming under a given URL such as http://localhost:8080/helloworld/{hiihaa}
 * where "hiihaa" can be anything. This is then used as defining a given base measure for the variable name
 * given in "hiihaa". The body of the HTTP request is then taken as the measurement value for this base measure.
 * We use filter since no HTTP service on OSGI supports servlet-mapping through URL's. Actually they do not
 * officially support filters either but the Felix extended one does.
 *
 * @author Teemu Kanstren
 */
public class BaseMeasureFilter implements Filter {
  private final static Logger log = new Logger(BaseMeasureFilter.class);
  //key=parameter name, value=latest measure for key
  public static final Map<String, BaseMeasure> values = new HashMap<String, BaseMeasure>();

  public void init(FilterConfig config) throws ServletException {
  }

  public void doFilter(ServletRequest servletRequest, ServletResponse resp, FilterChain chain) throws IOException, ServletException {
    HttpServletRequest req = (HttpServletRequest) servletRequest;
    resp.setContentType("text/plain");
    String name = req.getRequestURL().toString();
    int index = name.lastIndexOf('/');
    //todo: error handling if < 0 index is received
    //we take the name of the base measure, that which is after the last "/" character
    name = name.substring(index+1);

    // Get response data.
    BufferedReader br = new BufferedReader(new InputStreamReader(req.getInputStream()));
    String str;
    String content = "";
    //read the body, the base measure content
    while (null != ((str = br.readLine()))) {
      content += str;
    }
    br.close();

    log.debug("Received BM '"+name+"' from '"+req.getRemoteAddr()+" with value:"+content);
    values.put(name, new BaseMeasure(content));

    PrintWriter out = resp.getWriter();
    out.println("hello:"+name+" -- "+content);
    out.close();
  }

  public void destroy() {
  }
}
