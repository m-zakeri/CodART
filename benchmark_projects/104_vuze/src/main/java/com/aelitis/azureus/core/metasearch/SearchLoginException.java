package com.aelitis.azureus.core.metasearch;

public class SearchLoginException extends SearchException {
	
	public SearchLoginException(Throwable t) {
		super(t);
	}
	
	public SearchLoginException(String description,Throwable t) {
		super(description,t);
	}
	
	public SearchLoginException(String description) {
		super(description);
	}

}
