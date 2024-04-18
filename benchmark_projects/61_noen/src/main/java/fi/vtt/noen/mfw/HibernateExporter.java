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

package fi.vtt.noen.mfw;

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.MeasurementSubscription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import org.hibernate.cfg.Configuration;
import org.hibernate.cfg.Environment;
import org.hibernate.tool.hbm2ddl.SchemaExport;

/**
 * @author Teemu Kanstren
 */
public class HibernateExporter {
  public static void main(String[] args) {
    System.out.println("<<<<BELOW IS THE SQL GENERATED FROM HIBERNATE IN ORDER TO CREATE THE DATABASE." + System.getProperty("line.separator") +
            " HOWEVER, REMEMBER TO CHECK THAT YOU MODIFIED THIS GENERATOR TO INCLUDE ALL THE RELEVANT CLASSES THE ARE TO BE PERSISTED.");
    Configuration cfg = new Configuration();
    cfg.addAnnotatedClass(BMDescription.class);
    cfg.addAnnotatedClass(ProbeDescription.class);
    cfg.addAnnotatedClass(TargetDescription.class);
    cfg.addAnnotatedClass(Value.class);
    cfg.addAnnotatedClass(ServerEvent.class);
//    cfg.addAnnotatedClass(MeasurementSubscription.class);
    cfg.setProperty(Environment.USER, "root");
    cfg.setProperty(Environment.PASS, "");
    cfg.setProperty(Environment.URL, "jdbc:mysql://localhost/mfw_db");
    cfg.setProperty(Environment.DIALECT, "org.hibernate.dialect.MySQL5InnoDBDialect");
    cfg.setProperty(Environment.DRIVER, "com.mysql.jdbc.Driver");

    SchemaExport schema = new SchemaExport(cfg);
    schema.setOutputFile("schema.sql");

    schema.create(true, false);
  }
}
