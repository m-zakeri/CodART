/*
 * Created on 20.08.2003
 *
 */
package net.sourceforge.ganttproject.document;

import java.io.File;

/**
 * This is a helper class, to create new instances of Document easily.
 * It chooses the correct implementation based on the given path.
 * 
 * @author Michael Haeusler (michael at akatose.de)
 */
public class DocumentCreator {

	/**
	 * Creates an HttpDocument if path starts with "http://" or "https://";
	 * creates a FileDocument otherwise.
	 * 
	 * @param path path to the document
	 * @return an implementation of the interface Document
	 */
	public static Document createDocument(String path) {
		return createDocument(path, null, null);
	}

	/**
	 * Creates an HttpDocument if path starts with "http://" or "https://";
	 * creates a FileDocument otherwise.
	 * 
	 * @param path path to the document
	 * @param user username
	 * @param pass password
	 * @return an implementation of the interface Document
	 */
	public static Document createDocument(String path, String user, String pass) {
		if (null == path)
			return null;
		if (path.toLowerCase().startsWith("http://") ||
			path.toLowerCase().startsWith("https://")) {
			return new HttpDocument(path, user, pass);
		} else {
			return new FileDocument(new File(path));
		}
	}
		
}
