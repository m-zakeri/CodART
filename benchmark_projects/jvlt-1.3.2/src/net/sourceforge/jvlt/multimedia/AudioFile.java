package net.sourceforge.jvlt.multimedia;

import java.io.File;
import java.io.IOException;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.DataLine;


/**
 * This class represents an audio file that can be played with jVLT. Other audio
 * files (e.g. mp3 and ogg files) are represented by CustomMultimediaFile.
 */
public class AudioFile extends MultimediaFile {
	public AudioFile(String file_name) {
		super(file_name, AUDIO_FILE);
	}

	public AudioFile() {
		this("");
	}

	public void play() throws IOException {
		File f = getFile();
		if (!f.exists() || !f.isFile()) {
			String msg = "File " + f.getAbsolutePath() + " does not exist "
					+ "or cannot be opened.";
			throw new IOException(msg);
		}

		try {
			AudioInputStream stream = AudioSystem.getAudioInputStream(f);
			AudioFormat format = stream.getFormat();
			DataLine.Info info = new DataLine.Info(Clip.class, format);
			Clip clip = (Clip) AudioSystem.getLine(info);
			clip.open(stream);
			clip.start();
		} catch (Exception e) {
			String message = "Cannot open file " + f.getAbsolutePath() + ".";
			throw new IOException(message);
		}
	}
}
