
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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.sacservice;

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
 *         &lt;element name="PerDevice" maxOccurs="unbounded">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element ref="{http://www.bugyobeyond.org/MFW_SAC/}BMResult" maxOccurs="unbounded"/>
 *                 &lt;/sequence>
 *                 &lt;attribute name="device_id" use="required" type="{http://www.w3.org/2001/XMLSchema}long" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
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
    "perDevice"
})
@XmlRootElement(name = "BMResults")
public class BMResults {

    @XmlElement(name = "PerDevice", namespace = "", required = true)
    protected List<BMResults.PerDevice> perDevice;
    @XmlAttribute(name = "mfw_id", required = true)
    protected long mfwId;

    /**
     * Gets the value of the perDevice property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the perDevice property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getPerDevice().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link BMResults.PerDevice }
     * 
     * 
     */
    public List<BMResults.PerDevice> getPerDevice() {
        if (perDevice == null) {
            perDevice = new ArrayList<BMResults.PerDevice>();
        }
        return this.perDevice;
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
     *         &lt;element ref="{http://www.bugyobeyond.org/MFW_SAC/}BMResult" maxOccurs="unbounded"/>
     *       &lt;/sequence>
     *       &lt;attribute name="device_id" use="required" type="{http://www.w3.org/2001/XMLSchema}long" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "bmResult"
    })
    public static class PerDevice {

        @XmlElement(name = "BMResult", required = true)
        protected List<BMResult> bmResult;
        @XmlAttribute(name = "device_id", required = true)
        protected long deviceId;

        /**
         * Gets the value of the bmResult property.
         * 
         * <p>
         * This accessor method returns a reference to the live list,
         * not a snapshot. Therefore any modification you make to the
         * returned list will be present inside the JAXB object.
         * This is why there is not a <CODE>set</CODE> method for the bmResult property.
         * 
         * <p>
         * For example, to add a new item, do as follows:
         * <pre>
         *    getBMResult().add(newItem);
         * </pre>
         * 
         * 
         * <p>
         * Objects of the following type(s) are allowed in the list
         * {@link BMResult }
         * 
         * 
         */
        public List<BMResult> getBMResult() {
            if (bmResult == null) {
                bmResult = new ArrayList<BMResult>();
            }
            return this.bmResult;
        }

        /**
         * Gets the value of the deviceId property.
         * 
         */
        public long getDeviceId() {
            return deviceId;
        }

        /**
         * Sets the value of the deviceId property.
         * 
         */
        public void setDeviceId(long value) {
            this.deviceId = value;
        }

    }

}
