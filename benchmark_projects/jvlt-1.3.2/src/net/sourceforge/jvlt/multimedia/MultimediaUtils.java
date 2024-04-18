package net.sourceforge.jvlt.multimedia;

import java.io.IOException;

import net.sourceforge.jvlt.JVLT;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.utils.Config;

public class MultimediaUtils {
	public static final String[] AUDIO_FILE_EXTENSIONS = { "wav", "wave",
			"aif", "aifc", "aiff", "au", "snd" };
	public static final String[] IMAGE_FILE_EXTENSIONS = { "gif", "jpg",
			"jpeg", "png", "tif", "tiff" };

	public static MultimediaFile getMultimediaFileForName(String name) {
		Config conf = JVLT.getConfig();
		String[] custom_extensions = conf.getStringListProperty(
				"custom_extensions", new String[0]);
		for (String customExtension : custom_extensions) {
			if (name.toLowerCase().endsWith("." + customExtension)) {
				CustomMultimediaFile file = new CustomMultimediaFile(name);
				String[] ext_props = conf.getStringListProperty("extension_"
						+ customExtension, new String[0]);
				if (ext_props.length < 2) {
					file.setCommand("");
					file.setType(MultimediaFile.OTHER_FILE);
				} else {
					file.setCommand(ext_props[1]);
					file.setType(Integer.parseInt(ext_props[0]));
				}

				return file;
			}
		}

		for (String element : AUDIO_FILE_EXTENSIONS) {
			if (name.toLowerCase().endsWith("." + element)) {
				return new AudioFile(name);
			}
		}

		for (String element : IMAGE_FILE_EXTENSIONS) {
			if (name.toLowerCase().endsWith("." + element)) {
				return new ImageFile(name);
			}
		}

		return new CustomMultimediaFile(name, MultimediaFile.OTHER_FILE);
	}

	public static void playAudioFiles(Entry entry) throws IOException {
		String[] mm_files = entry.getMultimediaFiles();
		for (String mmFile : mm_files) {
			MultimediaFile mm_file = MultimediaUtils
					.getMultimediaFileForName(mmFile);
			if (mm_file.getType() == MultimediaFile.AUDIO_FILE) {
				((AudioFile) mm_file).play();
			}
		}
	}
}
