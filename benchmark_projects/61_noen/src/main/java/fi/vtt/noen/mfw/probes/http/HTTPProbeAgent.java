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

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgent;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Map;

/**
 * Grabs a base measure from a HTTP request posted at the address http://<address>/{bm-name}.
 * The base measure name is the part in the url and the content is the body of the http request.
 *
 * @author Teemu Kanstren
 */
public class HTTPProbeAgent extends BaseProbeAgent {
  public BaseMeasure measure() {
    return BaseMeasureFilter.values.get(getInformation().getBmName());
  }

  public void startProbe() {
  }

  public void stopProbe() {
  }

  public void setConfiguration(Map<String, String> configuration) {
  }

  public List<ProbeConfiguration> getConfigurationParameters() {
    return null;
  }

  //for self-testing
  public static void main(String[] args) throws Exception {
    // URL of CGI-Bin script.
    URL target = new URL("http://localhost:8081/mfw/bm/os_version");
    HttpURLConnection url = (HttpURLConnection) target.openConnection();
    // Let the run-time system (RTS) know that we want input.
    url.setDoInput(true);
    // Let the RTS know that we want to do output.
    url.setDoOutput(true);
    // No caching, we want the real thing.
    url.setUseCaches(false);
    // Specify the content type.
    url.setRequestProperty("Content-Type", "text/plain");
    // Send POST output.
    url.setRequestMethod("POST");
    DataOutputStream printout = new DataOutputStream(url.getOutputStream());
    String content = "A value has been observed.";
    printout.writeBytes(content);
    printout.flush();
    printout.close();
    // Get response data.
    BufferedReader br = new BufferedReader(new InputStreamReader(url.getInputStream()));
    String str;
    while (null != ((str = br.readLine()))) {
      System.out.println(str);
    }
    br.close();
  }
}
