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

import fi.vtt.noen.mfw.bundle.server.plugins.webui.frameset.BodyFrame;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.frameset.Home;
import org.apache.wicket.Page;
import org.apache.wicket.Request;
import org.apache.wicket.Response;
import org.apache.wicket.Session;
import org.apache.wicket.protocol.http.WebApplication;
import org.apache.wicket.util.file.Folder;

/**
 * The main Application used by Wicket to create the web ui.
 *
 * @author Teemu Kanstren
 */
public class WebUIWicketApplication extends WebApplication {
  private Folder uploadFolder = null;

  public Class<? extends Page> getHomePage() {
    return BodyFrame.class;
//    return ProbeListPage.class;
  }

  @Override
  public Session newSession(Request request, Response response) {
    return new WebUISession(request);
  }

  @Override
  protected void init() {
    super.init();
    getResourceSettings().setThrowExceptionOnMissingResource(false);

    uploadFolder = new Folder(System.getProperty("java.io.tmpdir"), "wicket-uploads");
    // Ensure folder exists
    uploadFolder.mkdirs();

//    mountBookmarkablePage("/multi", MultiUploadPage.class);
//    mountBookmarkablePage("/single", UploadPage.class);
  }

  public Folder getUploadFolder() {
    return uploadFolder;
  }
}
