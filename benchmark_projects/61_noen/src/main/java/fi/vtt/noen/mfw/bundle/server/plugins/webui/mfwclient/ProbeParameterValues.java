
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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import java.util.ArrayList;
import java.util.List;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element ref="{http://www.bugyobeyond.org/SAC_MFW/}ProbeParameterValue" maxOccurs="unbounded"/>
 *       &lt;/sequence>
 *       &lt;attribute name="probe_id" use="required" type="{http://www.w3.org/2001/XMLSchema}long" />
 *       &lt;attribute name="sac_id" use="required" type="{http://www.w3.org/2001/XMLSchema}long" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "probeParameterValue"
})
@XmlRootElement(name = "ProbeParameterValues")
public class ProbeParameterValues {

    @XmlElement(name = "ProbeParameterValue", required = true)
    protected List<ProbeParameterValue> probeParameterValue;
    @XmlAttribute(name = "probe_id", required = true)
    protected long probeId;
    @XmlAttribute(name = "sac_id", required = true)
    protected long sacId;

    /**
     * Gets the value of the probeParameterValue property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the probeParameterValue property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getProbeParameterValue().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link ProbeParameterValue }
     * 
     * 
     */
    public List<ProbeParameterValue> getProbeParameterValue() {
        if (probeParameterValue == null) {
            probeParameterValue = new ArrayList<ProbeParameterValue>();
        }
        return this.probeParameterValue;
    }

    /**
     * Gets the value of the probeId property.
     * 
     */
    public long getProbeId() {
        return probeId;
    }

    /**
     * Sets the value of the probeId property.
     * 
     */
    public void setProbeId(long value) {
        this.probeId = value;
    }

    /**
     * Gets the value of the sacId property.
     * 
     */
    public long getSacId() {
        return sacId;
    }

    /**
     * Sets the value of the sacId property.
     * 
     */
    public void setSacId(long value) {
        this.sacId = value;
    }

}
