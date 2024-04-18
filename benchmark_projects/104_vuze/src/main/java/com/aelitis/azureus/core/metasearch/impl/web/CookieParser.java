package com.aelitis.azureus.core.metasearch.impl.web;

import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class CookieParser {
	
	public static boolean cookiesContain(String[] requiredCookies,String cookies) {
		if(cookies == null) return false;
		boolean[] cookieFound = new boolean[requiredCookies.length];
		
		String[] names = getCookiesNames(cookies);
		
		for(int j = 0 ; j < names.length ; j++) {
			String cookieName = names[j];
			for(int i = 0 ; i < requiredCookies.length ;i++) {
				if(requiredCookies[i].equals(cookieName)) {
					cookieFound[i] = true;
				}
			}
		}
		
		for(int i = 0 ; i < cookieFound.length ; i++) {
			if(!cookieFound[i]) return false;
		}
		
		return true;
	}
	
	public static String[] getCookiesNames(String cookies) {
		if(cookies == null) return new String[0];
		
		StringTokenizer st = new StringTokenizer(cookies,"; ");
		List names = new ArrayList();
		
		while(st.hasMoreTokens()) {
			String cookie = st.nextToken();
			int separator = cookie.indexOf("=");
			if(separator > -1) {
				names.add(cookie.substring(0,separator));
			}
		}
		
		String[] result = (String[]) names.toArray(new String[names.size()]);
		
		return result;
	
	}

}
