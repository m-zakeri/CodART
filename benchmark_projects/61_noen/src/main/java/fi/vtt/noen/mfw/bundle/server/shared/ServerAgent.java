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

package fi.vtt.noen.mfw.bundle.server.shared;

import java.util.List;
import java.util.Map;


/**
 * Interface to a server-agent of the MFW.
 *
 * @author Teemu Kanstren
 */
public interface ServerAgent {
  public boolean measurement(long time, String measureURI, int precision, String value, long subscriptionId);
  public void event(long time, String type, String source, String message, long subscriptionId);
  public long register(Map<String, String> properties);
  public boolean keepAlive(long probeId);
  public void unregister(long probeId);
  public void checkSubscriptions(long probeId, List<Long> subscriptionIds);
  public boolean BMReport(long time, String measureURI, String value, long subscriptionId, boolean matchReference, String reference);

}
