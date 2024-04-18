package net.sourceforge.jvlt.utils;

import java.io.IOException;

public interface Config {
	String[] getKeys();

	boolean containsKey(String key);

	String getProperty(String key);

	String getProperty(String key, String default_value);

	float getFloatProperty(String key, float default_val);

	int getIntProperty(String key, int default_val);

	boolean getBooleanProperty(String key, boolean default_val);

	String[] getStringListProperty(String key, String[] def);

	String[] getStringListProperty(String key);

	double[] getNumberListProperty(String key, double[] def);
	
	void setProperty(String key, String value);

	void setProperty(String key, boolean value);

	void setProperty(String key, int value);

	void setProperty(String key, float value);

	void setProperty(String key, Object[] values);

	void remove(String key);
	
	public void load() throws IOException;
	
	public void store() throws IOException;
}
