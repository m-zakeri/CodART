
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

package fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice;

import javax.xml.bind.annotation.XmlRegistry;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {


    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link OperationResult }
     * 
     */
    public OperationResult createOperationResult() {
        return new OperationResult();
    }

    /**
     * Create an instance of {@link MFW }
     * 
     */
    public MFW createMFW() {
        return new MFW();
    }

    /**
     * Create an instance of {@link Device }
     * 
     */
    public Device createDevice() {
        return new Device();
    }

    /**
     * Create an instance of {@link GetMFW }
     * 
     */
    public GetMFW createGetMFW() {
        return new GetMFW();
    }

    /**
     * Create an instance of {@link GetAvailability }
     * 
     */
    public GetAvailability createGetAvailability() {
        return new GetAvailability();
    }

    /**
     * Create an instance of {@link Probe }
     * 
     */
    public Probe createProbe() {
        return new Probe();
    }

    /**
     * Create an instance of {@link ProbeParameter }
     * 
     */
    public ProbeParameter createProbeParameter() {
        return new ProbeParameter();
    }

    /**
     * Create an instance of {@link ProbeParameters }
     * 
     */
    public ProbeParameters createProbeParameters() {
        return new ProbeParameters();
    }

    /**
     * Create an instance of {@link ProbeParameterValue }
     * 
     */
    public ProbeParameterValue createProbeParameterValue() {
        return new ProbeParameterValue();
    }

    /**
     * Create an instance of {@link Availability }
     * 
     */
    public Availability createAvailability() {
        return new Availability();
    }

    /**
     * Create an instance of {@link BM }
     * 
     */
    public BM createBM() {
        return new BM();
    }

    /**
     * Create an instance of {@link ProbeParametersRequest }
     * 
     */
    public ProbeParametersRequest createProbeParametersRequest() {
        return new ProbeParametersRequest();
    }

    /**
     * Create an instance of {@link BMResultRequest }
     * 
     */
    public BMResultRequest createBMResultRequest() {
        return new BMResultRequest();
    }

    /**
     * Create an instance of {@link BMResultsRequest }
     * 
     */
    public BMResultsRequest createBMResultsRequest() {
        return new BMResultsRequest();
    }

    /**
     * Create an instance of {@link ProbeParameterValues }
     * 
     */
    public ProbeParameterValues createProbeParameterValues() {
        return new ProbeParameterValues();
    }

}
