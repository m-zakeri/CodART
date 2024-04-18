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

import org.deckfour.xes.in.XMxmlParser;
import org.deckfour.xes.model.XLog;
import org.deckfour.xes.model.XEvent;
import org.deckfour.xes.model.XAttribute;
import org.deckfour.xes.info.XLogInfo;
import org.deckfour.xes.info.XLogInfoFactory;
import org.deckfour.xes.classification.XEventClassifier;
import org.deckfour.xes.classification.XEventNameClassifier;
import org.deckfour.xes.classification.XEventClass;
import org.processmining.framework.plugin.*;
import org.processmining.framework.plugin.events.ProgressEventListener;
import org.processmining.framework.plugin.events.PluginLifeCycleEventListener;
import org.processmining.framework.plugin.events.Logger;
import org.processmining.framework.plugin.impl.AbstractPluginContext;
import org.processmining.framework.plugin.impl.FieldSetException;
import org.processmining.framework.connections.Connection;
import org.processmining.framework.connections.ConnectionManager;
import org.processmining.framework.providedobjects.ProvidedObjectManager;
import org.processmining.contexts.cli.CLIPluginContext;
import org.processmining.contexts.cli.CLIContext;
import org.processmining.models.graphbased.directed.transitionsystem.State;
import org.processmining.models.graphbased.directed.transitionsystem.Transition;
import org.processmining.plugins.transitionsystem.miner.TSMinerInput;
import org.processmining.plugins.transitionsystem.miner.TSMiner;
import org.processmining.plugins.transitionsystem.miner.TSMinerOutput;
import org.processmining.plugins.transitionsystem.miner.util.TSAbstractions;
import org.processmining.plugins.transitionsystem.miner.util.TSDirections;
import org.processmining.plugins.transitionsystem.miner.util.TSModes;
import org.processmining.plugins.transitionsystem.miner.modir.TSMinerModirInput;
import org.processmining.plugins.transitionsystem.converter.util.TSConversions;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.ByteArrayOutputStream;
import java.util.*;
import java.util.concurrent.Executor;

import fi.vtt.noen.testgen.model.fsm.FSMModel;

/**
 * Uses ProM code to build an FSM from a suitable log file and takes the resulting data
 * structures describing the FSM, turning these into custom formats used for EFSM generation.
 *
 * @author Teemu Kanstrén
 */
public class PromParser {
  public XLog parseLog(InputStream in) {
    try {
      Set<XLog> logs = new XMxmlParser().parse(in);
      Iterator<XLog> i = logs.iterator();
      XLog log = i.next();
      return log;
    } catch (Exception e) {
      throw new RuntimeException("Problem with PROM MXML parser.", e);
    }
  }

  public Collection<String> createFilters(XLogInfo summary) {
    Collection<String> filters = new ArrayList<String>();
    for (XEventClass xe : summary.getIdClasses().getClasses()) {
      filters.add(xe.toString());
    }
    return filters;
  }

  public FSMModel parse(InputStream in) {
    XLog log = parseLog(in);
    XLogInfo summary = XLogInfoFactory.createLogInfo(log);

    CLIPluginContext context = new CLIPluginContext(new CLIContext(), "PROMTest");

    TSMinerInput input = new TSMinerInput(context, log, summary);
//    System.out.println("converter:"+input.getConverterSettings().getUse(TSConversions.KILLSELFLOOPS));
//    input.getConverterSettings().setUse(TSConversions.KILLSELFLOOPS, false);
    TSMinerModirInput modirInput = new TSMinerModirInput();
    modirInput.setUse(true);
    Collection<String> filters = createFilters(summary);
    modirInput.getFilter().addAll(filters);

    modirInput.setAbstraction(TSAbstractions.SEQUENCE);

    modirInput.setHorizon(1);
    modirInput.setFilteredHorizon(1);
    input.setModirSettings(TSDirections.BACKWARD, TSModes.MODELELEMENT, modirInput);
    TSMiner miner = new TSMiner(context);
    TSMinerOutput output = miner.mine(input);

    FSMModel fsm = new FSMModel(output.getTransitionSystem());
    return fsm;
  }
}
