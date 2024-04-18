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

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * Describes a target of measurement. Persisted in order to keep the identifiers the same over restarts. This
 * is to allow the clients to use them in a persistent manner.
 * Annotations are for persistence with JPA (DB storage).
 *
 * @author Teemu Kanstren
 */
@Entity
@Table(name="target_description")
public class TargetDescription {
  @GeneratedValue
  @Id
  @Column(name="id", nullable=false, updatable=false)
  private Long targetId;
  @Column(name="target_type")
  private String targetType;
  @Column(name="target_name")
  private String targetName;

  public TargetDescription() {
  }

  public TargetDescription(String targetType, String targetName) {
    this.targetType = targetType;
    this.targetName = targetName;
  }

  public long getTargetId() {
    return targetId;
  }

  public String getTargetName() {
    return targetName;
  }

  public String getTargetType() {
    return targetType;
  }
}
