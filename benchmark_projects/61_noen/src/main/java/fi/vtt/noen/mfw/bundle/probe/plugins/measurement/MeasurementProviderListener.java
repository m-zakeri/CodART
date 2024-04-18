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

import org.osgi.framework.BundleContext;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.NewServiceListener;

public class MeasurementProviderListener extends NewServiceListener {
  private final MeasurementProviderUser user;

  public MeasurementProviderListener(BundleContext bc, Logger log, MeasurementProviderUser user) {
    super(bc, MeasurementProvider.class, log);
    this.user = user;
  }

  @Override
  public void registered(Object service) {
    user.setMeasurementProvider((MeasurementProvider) service);
  }

  @Override
  public void unregistered(Object service) {
    user.setMeasurementProvider(null);
  }
}
  