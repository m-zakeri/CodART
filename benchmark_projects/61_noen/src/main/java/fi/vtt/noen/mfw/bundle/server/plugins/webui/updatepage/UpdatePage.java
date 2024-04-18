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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.updatepage;

import org.apache.wicket.extensions.ajax.markup.html.form.upload.UploadProgressBar;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.panel.FeedbackPanel;
import org.apache.wicket.markup.html.resources.StyleSheetReference;

/**
 * @author Teemu Kanstr�n
 */
public class UpdatePage extends WebPage {
  public UpdatePage() {
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    createUploadForm();
  }

  public void createUploadForm() {
    // Create feedback panels
    final FeedbackPanel uploadFeedback = new FeedbackPanel("uploadfeedback");
    // Add uploadFeedback to the page itself
    add(uploadFeedback);

    // Add upload form with ajax progress bar
    final UploadForm ajaxSimpleUploadForm = new UploadForm("fileupload");
    ajaxSimpleUploadForm.add(new UploadProgressBar("progress", ajaxSimpleUploadForm));
    add(ajaxSimpleUploadForm);
  }
}
