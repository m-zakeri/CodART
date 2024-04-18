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

import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIWicketApplication;
import org.apache.wicket.Application;
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.form.upload.FileUpload;
import org.apache.wicket.markup.html.form.upload.FileUploadField;
import org.apache.wicket.util.file.Files;
import org.apache.wicket.util.file.Folder;
import org.apache.wicket.util.lang.Bytes;

import java.io.File;

/**
 * @author Teemu Kanstren
 */
public class UploadForm extends Form<Void> {
  private FileUploadField fileUploadField;

  public UploadForm(String id) {
    super(id);
    // set this form to multipart mode (allways needed for uploads!)
    setMultiPart(true);
    // Add one file input field
    add(fileUploadField = new FileUploadField("fileinput"));
    // Set maximum size to 100K for demo purposes
    setMaxSize(Bytes.kilobytes(100));
    // this is just to make the unit test happy
    //todo: check wicket unit tests
    setMarkupId("commentForm");
  }

  /**
   * @see org.apache.wicket.markup.html.form.Form#onSubmit()
   */
  @Override
  protected void onSubmit() {
    final FileUpload upload = fileUploadField.getFileUpload();
    if (upload != null) {
      // Create a new file
      File newFile = new File(getUploadFolder(), upload.getClientFileName());
      // Check new file, delete if it allready existed
      checkFileExists(newFile);
      try {
        // Save to new file
        newFile.createNewFile();
        upload.writeTo(newFile);
        info("saved file: " + upload.getClientFileName());
        info("dir:" + getUploadFolder());
      }
      catch (Exception e) {
        throw new IllegalStateException("Unable to write file");
      }
    }
  }

  /**
   * Check whether the file already exists, and if so, try to delete it.
   *
   * @param newFile the file to check
   */
  private void checkFileExists(File newFile) {
    if (newFile.exists()) {
      // Try to delete the file
      if (!Files.remove(newFile)) {
        throw new IllegalStateException("Unable to overwrite " + newFile.getAbsolutePath());
      }
    }
  }

  private Folder getUploadFolder() {
    return ((WebUIWicketApplication) Application.get()).getUploadFolder();
  }
}
