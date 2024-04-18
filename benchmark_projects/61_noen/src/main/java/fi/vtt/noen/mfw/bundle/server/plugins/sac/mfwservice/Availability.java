
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
 *         &lt;element ref="{http://www.bugyobeyond.org/SAC_MFW/}Device" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://www.bugyobeyond.org/SAC_MFW/}BM" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://www.bugyobeyond.org/SAC_MFW/}Probe" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="mfw_id" use="required" type="{http://www.w3.org/2001/XMLSchema}long" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "device",
    "bm",
    "probe"
})
@XmlRootElement(name = "Availability")
public class Availability {

    @XmlElement(name = "Device")
    protected List<Device> device;
    @XmlElement(name = "BM")
    protected List<BM> bm;
    @XmlElement(name = "Probe")
    protected List<Probe> probe;
    @XmlAttribute(name = "mfw_id", required = true)
    protected long mfwId;

    /**
     * Gets the value of the device property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the device property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getDevice().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Device }
     * 
     * 
     */
    public List<Device> getDevice() {
        if (device == null) {
            device = new ArrayList<Device>();
        }
        return this.device;
    }

    /**
     * Gets the value of the bm property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the bm property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getBM().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link BM }
     * 
     * 
     */
    public List<BM> getBM() {
        if (bm == null) {
            bm = new ArrayList<BM>();
        }
        return this.bm;
    }

    /**
     * Gets the value of the probe property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the probe property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getProbe().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Probe }
     * 
     * 
     */
    public List<Probe> getProbe() {
        if (probe == null) {
            probe = new ArrayList<Probe>();
        }
        return this.probe;
    }

    /**
     * Gets the value of the mfwId property.
     * 
     */
    public long getMfwId() {
        return mfwId;
    }

    /**
     * Sets the value of the mfwId property.
     * 
     */
    public void setMfwId(long value) {
        this.mfwId = value;
    }

}
