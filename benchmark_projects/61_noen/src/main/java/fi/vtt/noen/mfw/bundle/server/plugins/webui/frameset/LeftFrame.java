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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.frameset;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.availabilitypage.AvailabilityPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage.BMListPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmreportspage.BMReportsPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmresultspage.BMResultsPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.eventlistpage.EventListPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.historypage.HistoryPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwinformationpage.MFWInformationPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage.ProbeListPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probeparameterpage.ProbeParameterPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.subscribetobmpage.SubscribeToBMPage;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.updatepage.UpdatePage;
import org.apache.wicket.Page;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.link.Link;

/**
 * @author Teemu Kanstren
 */
public class LeftFrame extends WebPage {
  private final static Logger log = new Logger(LeftFrame.class);

  /**
   * Link that, when clicked, changes the frame target's frame class (and as that is a shared
   * model which is also being used by the 'master page' {@link BodyFrame}, changes are
   * immediately reflected) and set the response page to the top level page {@link BodyFrame}.
   * Tags that use this link should have a <code>target="_parent"</code> attribute, so that the
   * top frame will be refreshed.
   */
  private static final class ChangeFramePageLink extends Link {
    private static final long serialVersionUID = 1L;

    /**
     * parent frame class.
     */
    private final BodyFrame bodyFrame;

    /**
     * this link's target.
     */
    private final Class<? extends Page> pageClass;

    /**
     * Construct.
     *
     * @param <C>
     * @param id
     * @param bodyFrame
     * @param pageClass
     */
    public <C extends Page> ChangeFramePageLink(String id, BodyFrame bodyFrame, Class<C> pageClass) {
      super(id);
      this.bodyFrame = bodyFrame;
      this.pageClass = pageClass;
    }

    /**
     * @see org.apache.wicket.markup.html.link.Link#onClick()
     */
    @Override
    public void onClick() {
      // change frame class
      bodyFrame.getFrameTarget().setFrameClass(pageClass);

      // trigger re-rendering of the page
      setResponsePage(bodyFrame);
    }
  }

  private static final long serialVersionUID = 1L;

  /**
   * Constructor
   *
   * @param index parent frame class
   */
  public LeftFrame(BodyFrame index) {
    add(new ChangeFramePageLink("linkToHistoryPage", index, HistoryPage.class));
    add(new ChangeFramePageLink("linkToProbesPage", index, ProbeListPage.class));
    add(new ChangeFramePageLink("linkToBMPage", index, BMListPage.class));
    add(new ChangeFramePageLink("linkToEventsPage", index, EventListPage.class));
//    add(new ChangeFramePageLink("linkToDMPage", index, DerivedMeasuresPage.class));
//    add(new ChangeFramePageLink("linkToUpdatePage", index, UpdatePage.class));
//    add(new ChangeFramePageLink("linkToMFWInformationPage", index, MFWInformationPage.class));
//    add(new ChangeFramePageLink("linkToAvailabilityPage", index, AvailabilityPage.class));
//    add(new ChangeFramePageLink("linkToProbeParameterPage", index, ProbeParameterPage.class));
//    add(new ChangeFramePageLink("linkToSubscribeToBMPage", index, SubscribeToBMPage.class));
//    add(new ChangeFramePageLink("linkToBMResultsPage", index, BMResultsPage.class));
//    add(new ChangeFramePageLink("linkToBMReportsPage", index, BMReportsPage.class));
  }

  /**
   * No need for versioning this frame.
   *
   * @see org.apache.wicket.Component#isVersioned()
   */
  @Override
  public boolean isVersioned() {
    return false;
  }
}
