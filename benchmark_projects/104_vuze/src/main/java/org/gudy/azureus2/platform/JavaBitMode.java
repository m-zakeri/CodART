package org.gudy.azureus2.platform;

import org.gudy.azureus2.core3.util.Constants;

public class JavaBitMode
{
	public static void main(String[] args) {
		String prop = System.getProperty ("sun.arch.data.model");
		if (prop == null) prop = System.getProperty ("com.ibm.vm.bitmode");
		if (prop == null) prop = Constants.is64Bit ? "64" : "32"; 
		System.out.print(prop);
	}
}
