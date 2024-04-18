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

package fi.vtt.noen.mfw.bundle.server.plugins.rest;


//import java.util.Date;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import javax.ws.rs.core.MediaType;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.UniformInterfaceException;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.filter.HTTPBasicAuthFilter;

import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.BaseMeasure;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ClientRequest;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.FrameworkInfo;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.HistoryRequest;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.MeasurementHistory;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.MeasurementValue;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Parameter;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Probe;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ProbesInfo;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Session;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Target;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwinformationpage.MFWInformationPage;


/**
 * @author Teemu Kanstren
 */
public class TestClient {
  public static void main(String[] args) throws Exception {
    Client client = Client.create();
//    MessageDigest md = MessageDigest.getInstance( "SHA-256" );
//    String pass = new String( md.digest( "password".getBytes() ) );
    String pass = "password";
    // add authentication filter, it'll be always added to request as authorization header
    client.addFilter(new HTTPBasicAuthFilter("username", pass));
    WebResource wr = client.resource("http://localhost:8080/rest/");

    try {
      FrameworkInfo info = wr.path("client/mfwinformation").accept(MediaType.APPLICATION_XML).get(FrameworkInfo.class);
      System.out.println("MFW Information: ");
      if (info != null) {
        System.out.println("  Id: " + info.getId());
        System.out.println("  Name: " + info.getName());
      }
    } catch (Exception e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }

    Session session = null;
    try {
      ClientRequest c = new ClientRequest("TestClient", "http://localhost:8088/rest/");
      session = wr.path("client/register").accept(MediaType.APPLICATION_XML).post(Session.class, c);
    } catch (UniformInterfaceException uie) {
      int status = uie.getResponse().getStatus();
      System.out.println("Response status: " + status);
      // TODO Auto-generated catch block
      uie.printStackTrace();
    }

    if (session != null) {
      System.out.println("Session id: " + session.getId());
    }

    ProbesInfo probes = null;
    try {
      probes = wr.path("client/probes").accept(MediaType.APPLICATION_XML).get(ProbesInfo.class);
      System.out.println("Probes: ");

      for (Target target : probes.getTargets()) {
        System.out.println("  Target: " + target.getId() + "," + target.getName() + "," + target.getType());
      }

      for (BaseMeasure bm : probes.getBaseMeasures()) {
        System.out.println("  BaseMeasure: " + bm.getId() + "," + bm.getDescription() + "," + bm.getTargetid());
      }

      for (Probe p : probes.getProbes()) {
        System.out.println("  Probe: " + p.getId() + "," + p.getName() + "," + p.getBmid());

        if (p.getId().equals("16")) {
          ProbeConfiguration x = new ProbeConfiguration();
          ArrayList<Parameter> y = new ArrayList<Parameter>();
          y.add(new Parameter("x", "120px"));
          y.add(new Parameter("y", "60px"));
          x.setValues(y);
          try {
            wr.path("client/probeconfiguration/" + p.getId()).type(MediaType.APPLICATION_XML).post(x);
          } catch (UniformInterfaceException uie) {
            if (uie.getResponse().getStatus() == ClientResponse.Status.NOT_ACCEPTABLE.getStatusCode()) {
              System.out.println("    Cannot set parameters for " + p.getId());
            }
          }
        }

        ProbeConfiguration pc = wr.path("client/probeconfiguration/" + p.getId()).accept(MediaType.APPLICATION_XML).get(ProbeConfiguration.class);
        if (pc != null) {
          ArrayList<Parameter> params = pc.getValues();
          if (params != null) {
            for (Parameter param : pc.getValues()) {
              System.out.println("    Config: " + param.getKey() + "->" + param.getValue());
            }
          }
        }
      }
    } catch (Exception e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    MeasurementHistory history = null;
    try {
      HistoryRequest r = new HistoryRequest();
      ArrayList<Long> bms = new ArrayList<Long>();
      bms.add(2L);
      r.setBms(bms);
      Calendar c = Calendar.getInstance();
      c.set(2011, 4, 16, 13, 59, 0);
      r.setStart(c.getTimeInMillis());
      c.setTimeInMillis(System.currentTimeMillis());
      r.setEnd(c.getTimeInMillis());
      history = wr.path("client/history").accept(MediaType.APPLICATION_XML).post(MeasurementHistory.class, r);
      System.out.println("History: ");

      for (MeasurementValue value : history.getValues()) {
        System.out.println("  " + value.getBmid() + "(" + value.getTimestamp() + "): " + value.getValue());
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
