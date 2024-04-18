/*
 JOpenChart Java Charting Library and Toolkit
 Copyright (C) 2001  Sebastian Müller
 http://jopenchart.sourceforge.net

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 JDBCPlotter.java
 Created on 9. October 2002
 Based on SQLPlotter.java, created on 29. December 2001
 
 */

package de.progra.charting.model;

import java.sql.*;
import java.util.ArrayList;


/**
 * The class is used to convert database queries into ChartDataModels.
 * You can initialize the Plotter with database parameters and afterwards
 * you can run consecutive queries resulting in a new database.
 */
public class JDBCPlotter {

    /** The SQL connection. */
    protected Connection conn;

    /**
     * Creates a new JDBCPlotter using the given driver and URL.
     * @param jdbcDriver the fully qualified classname of the SQL driver class.
     * @param jdbcURL the URL of the JDBC database to connect to.
     * @param username the username for the JDBC resource
     * @param password the user's password
     */
    public JDBCPlotter(String jdbcDriver, String jdbcURL, String username, String password) 
            throws JDBCPlotterException {
        try {
            Class.forName( jdbcDriver);
            conn = DriverManager.getConnection(jdbcURL, username, password);
        } catch(Exception e) {
            throw new JDBCPlotterException("Exception while creating a database connection.", e);
        }
    }

    /** 
     * Given a SQL query and the row titles this method creates a DefaultChartDataModel.
     * The columns are initialized with values starting from 0.
     * @param sqlQuery the SQL query to be performed
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel and which
     * will be used as the DataSet titles.
     */
    public DefaultChartDataModel createChartDataModelInstance(String sqlQuery, String[] sqlRows) 
            throws JDBCPlotterException {
        return createChartDataModelInstance(sqlQuery, sqlRows, sqlRows);
    }
    
    /** 
     * Given a SQL query and the row titles this method creates a DefaultChartDataModel.
     * The columns are initialized with values starting from 0.
     * @param sqlQuery the SQL query to be performed
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel
     * @param dataSets the DataSet titles which should be given to the ChartDataModel instead of the sqlRows titles
     */
    public DefaultChartDataModel createChartDataModelInstance(String sqlQuery, String[] sqlRows, String[] dataSets) 
            throws JDBCPlotterException {
        try {
            Statement stmt = conn.createStatement();
            ResultSet sqlResult = stmt.executeQuery(sqlQuery);

            ArrayList model[]   = new ArrayList[sqlRows.length];
            ArrayList columnList = new ArrayList();

            for(int i = 0; i < model.length; i++) {
                model[i]=new ArrayList(); 
            }

            double x = 0.0;
            while(sqlResult.next()) {

                columnList.add(new Double(x));
                x += 1.0;

                for(int i = 0; i < sqlRows.length; i++) {
                    model[i].add(new Double(sqlResult.getDouble(sqlRows[i])));

                }
            }

            Number[][] modelArray = new Number[model.length][];
            
            for(int i = 0; i < model.length; i++)
                modelArray[i] = (Number[])model[i].toArray(new Number[0]);
            
            double[] columns = new double[columnList.size()];
            
            for(int i = 0; i < columns.length; i++)
                columns[i] = ((Double)columnList.get(i)).doubleValue();
            
            return new DefaultChartDataModel(modelArray, columns, dataSets);
            
        } catch( Exception e ) {
            throw new JDBCPlotterException("Exception while performing task.", e);
        }
    }

    /** 
     * Given a SQL query and the row titles this method creates a DefaultChartDataModel.
     * The columns are initialized with values from columnRow.
     * @param sqlQuery the SQL query to be performed
     * @param columnRow the row from the ResultSet which should be taken as the column (x-axis) values
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel and which
     * will be used as the DataSet titles.
     */
    public DefaultChartDataModel createChartDataModelInstance(String sqlQuery, String columnRow, String[] sqlRows) 
            throws JDBCPlotterException {
        return createChartDataModelInstance(sqlQuery, columnRow, sqlRows, sqlRows);
    }
    
    /** 
     * Given a SQL query and the row titles this method creates a DefaultChartDataModel.
     * The columns are initialized with values from columnRow.
     * @param sqlQuery the SQL query to be performed
     * @param columnRow the row from the ResultSet which should be taken as the column (x-axis) values
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel
     * @param dataSets the DataSet titles which should be given to the ChartDataModel instead of the sqlRows titles
     */
    public DefaultChartDataModel createChartDataModelInstance(String sqlQuery, String columnRow, String[] sqlRows, String[] dataSets) 
            throws JDBCPlotterException {
        try {
            Statement stmt = conn.createStatement();
            ResultSet sqlResult = stmt.executeQuery(sqlQuery);

            ArrayList model[]   = new ArrayList[sqlRows.length];
            ArrayList columnList = new ArrayList();

            for(int i = 0; i < model.length; i++) {
                model[i]=new ArrayList(); 
            }

            while(sqlResult.next()) {

                columnList.add(new Double(sqlResult.getDouble(columnRow)));
                
                for(int i = 0; i < sqlRows.length; i++) {
                    model[i].add(new Double(sqlResult.getDouble(sqlRows[i])));

                }
            }

            Number[][] modelArray = new Number[model.length][];
            
            for(int i = 0; i < model.length; i++)
                modelArray[i] = (Number[])model[i].toArray(new Number[0]);
            
            double[] columns = new double[columnList.size()];
            
            for(int i = 0; i < columns.length; i++)
                columns[i] = ((Double)columnList.get(i)).doubleValue();
            
            return new DefaultChartDataModel(modelArray, columns, dataSets);
        } catch( Exception e ) {
            throw new JDBCPlotterException("Exception while performing task.", e);
        }
    }

    /** 
     * Given a SQL query and the row titles this method creates a ObjectChartDataModel.
     * The columns are initialized with values from row columnRow.
     * @param sqlQuery the SQL query to be performed
     * @param columnRow the row from the ResultSet which should be taken as the column (x-axis) values
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel and which
     * will be used as the DataSet titles.
     */
    public ObjectChartDataModel createObjectChartDataModelInstance(String sqlQuery, String columnRow, String[] sqlRows) 
            throws JDBCPlotterException {
        return createObjectChartDataModelInstance(sqlQuery, columnRow, sqlRows, sqlRows);
    }

    /** 
     * Given a SQL query and the row titles this method creates an ObjectChartDataModel.
     * The columns are initialized with values of row columnRow.
     * @param sqlQuery the SQL query to be performed
     * @param columnRow the row from the ResultSet which should be taken as the column (x-axis) values
     * @param sqlRows the rows from the ResultSet which should be included in the ChartDataModel
     * @param dataSets the DataSet titles which should be given to the ChartDataModel instead of the sqlRows titles
     */
    public ObjectChartDataModel createObjectChartDataModelInstance(String sqlQuery, String columnRow, String[] sqlRows, String[] dataSets) 
            throws JDBCPlotterException {
        try {
            Statement stmt = conn.createStatement();
            ResultSet sqlResult = stmt.executeQuery(sqlQuery);

            ArrayList model[]   = new ArrayList[sqlRows.length];
            ArrayList columnList = new ArrayList();

            for(int i = 0; i < model.length; i++) {
                model[i]=new ArrayList(); 
            }

            while(sqlResult.next()) {

                columnList.add(sqlResult.getString(columnRow));

                for(int i = 0; i < sqlRows.length; i++) {
                    model[i].add(new Double(sqlResult.getDouble(sqlRows[i])));

                }
            }

            Number[][] modelArray = new Number[model.length][];
            
            for(int i = 0; i < model.length; i++)
                modelArray[i] = (Number[])model[i].toArray(new Number[0]);
            
            String[] columns = (String[])columnList.toArray(new String[0]);
            
            return new ObjectChartDataModel(modelArray, columns, dataSets);
        } catch( Exception e ) {
            throw new JDBCPlotterException("Exception while performing task.", e);
        }
    }
}
