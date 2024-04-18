/*
 * Copyright (C) 2009 VTT Technical Research Centre of Finland.
 *
 * This file is part of NOEN framework.
 *
 * NOEN framework is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2.
 *
 * NOEN framework is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

package fi.vtt.noen.testgen.parser;

import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.SAXException;
import org.xml.sax.Attributes;

/**
 * @author Teemu Kanstrén
 */
public class NoenParser extends DefaultHandler {
  public void startDocument() throws SAXException {
  }

  public void endDocument() throws SAXException {
  }

  public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
    //qname=tagi
    for (int i = 0 ; i < attributes.getLength() ; i++) {
      String qname = attributes.getQName(i);
      String value = attributes.getValue(i);
    }
  }

  public void characters(char ch[], int start, int length) throws SAXException {
    //tagin sisältö..
  }

  public void endElement(String uri, String localName, String qName) throws SAXException {
  }
}
