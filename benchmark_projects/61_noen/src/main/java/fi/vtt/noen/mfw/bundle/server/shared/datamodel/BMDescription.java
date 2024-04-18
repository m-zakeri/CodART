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

package fi.vtt.noen.mfw.bundle.server.shared.datamodel;

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.Transient;


/**
 * Describes a base measure in terms of BM class, BM name, BM description, and measurement target.
 * Annotations are for persistence with JPA (DB storage).
 *
 * @author Teemu Kanstren
 */
@Entity
@Table(name="bm_description")
public class BMDescription implements Comparable {
  private final static Logger log = new Logger(BMDescription.class);

  //automatically generated id value from JPA/DB
  @GeneratedValue
  @Id
  @Column(name="id", nullable=false, updatable=false)
  private Long bmId;

  //the class of base measure. not used for anything atm. but could be used to group BM types together.
  @Column(name="class")
  private String bmClass;

  //the name of a base measure
  @Column(name="name")
  private String bmName;

  //the target of measurement
  @ManyToOne(fetch= FetchType.EAGER)
  private TargetDescription target;

  //the description of the base measure. free form text for human consumption.
  @Column(name="description")
  private String bmDescription;

  @Column(name="data_type")
  private Type dataType;

  public enum Type {
    STRING, BOOLEAN, NUMERIC
  }

  public BMDescription() {
  }

  public BMDescription(TargetDescription target, String bmClass, String bmName, String bmDescription) {
    this.target = target;
    this.bmClass = bmClass;
    this.bmName = bmName;
    this.bmDescription = bmDescription;
    this.dataType = Type.STRING;
  }

  public BMDescription(TargetDescription target, String bmClass, String bmName, String bmDescription, Type dataType) {
    this.target = target;
    this.bmClass = bmClass;
    this.bmName = bmName;
    this.bmDescription = bmDescription;
    this.dataType = dataType;
  }

  @Transient
  public String getMeasureURI() {
    return Const.createMeasureURI(target.getTargetType(), target.getTargetName(), bmClass, bmName);
  }

  public String getBmDescription() {
    return bmDescription;
  }

  public String getBmName() {
    return bmName;
  }

  public String getBmClass() {
    return bmClass;
  }

  public TargetDescription getTarget() {
    return target;
  }

  public long getBmId() {
    return bmId;
  }

  public Type getDataType() {
    return dataType;
  }

  /**
   * Check if this is the same as the given one. Comparison is based on the measureURI.
   * Could probably be turned into equals..
   *
   * @param desc What we are comparing against.
   * @return True if they have the same measureURI.
   */
  public boolean matches(BMDescription desc) {
    return desc.getMeasureURI().equals(getMeasureURI());
  }

  /**
   * Check if this BM matches a measurement values. That is, is the value a value for this BM.
   * Comparison based on the measureURI.
   *
   * @param value What we are comparing against.
   * @return True if they have the same measureURI.
   */
  public boolean matches(Value value) {
    return value.getMeasureURI().equals(getMeasureURI());
  }

  @Override
  public String toString() {
    return getMeasureURI();
  }

  //for the comparator interface
  public int compareTo(Object o) {
    BMDescription other = (BMDescription) o;
    return getMeasureURI().compareTo(other.getMeasureURI());
  }
}
