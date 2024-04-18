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

    ChartServlet.java
    Created on 2. September 2001, 14:44
*/

package de.progra.charting.servlet;

import javax.servlet.*;
import javax.servlet.http.*;
import de.progra.charting.*;
import java.io.*;

/** 
 * This Servlet returns image files of diagrams to be embedded in HTML/JSP
 * pages. The Servlet expects the following parameters:<br>
 * <ul>
 * <li>"imageType" Parameter (either GET or POST), one of "gif", "jpeg", "png" 
 * - defines the image format to be returned
 * <li>"chart" Attribute (stored in SessionContext), <code>DefaultChart</code>
 * object to be rendered
 * </ul>
 * <p>This class will be extended to allow easier rendering without assembling
 * the whole DefaultChart object. If the ChartServlet is deployed correctly
 * you can embed it e.g. with 
 * <code>&lt;img src="/charting/ChartServlet?imageType=gif" alt="PieChart as GIF Image"&gt;</code>.
 *
 * @author  mueller
 * @version 1.0
 */
public class ChartServlet extends HttpServlet {
   
    /** Initializes the servlet.
    */  
    public void init(ServletConfig config) throws ServletException {
        super.init(config);

    }

    /** Destroys the servlet.
    */  
    public void destroy() {

    }

    /** Processes requests for both HTTP <code>GET</code> and <code>POST</code> methods.
    * @param request servlet request
    * @param response servlet response
    */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, java.io.IOException {
        
            String imgType = (String)request.getParameter("imageType");
            DefaultChart chart = (DefaultChart)request.getSession(true).getAttribute("chart");

            //response.setContentType("image/"+imgType);
            ServletOutputStream out = response.getOutputStream();
            try {
                if(chart != null) {
                    if(imgType == null)
                        ChartEncoder.createGIF(out, chart);
                    else if(imgType.equals("gif"))
                        ChartEncoder.createGIF(out, chart);
                    else if(imgType.equals("jpeg"))
                        ChartEncoder.createJPEG(out, chart);
                    else
                        ChartEncoder.createPNG(out, chart);
                }
            } catch(EncodingException p) {
                throw new IOException("An Error occurred encoding the Image file.");
            }
        
        /* output your page here
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Servlet</title>");  
        out.println("</head>");
        out.println("<body>");

        out.println("</body>");
        out.println("</html>");
        */
            out.close();
    } 

    /** Handles the HTTP <code>GET</code> method.
    * @param request servlet request
    * @param response servlet response
    */
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, java.io.IOException {
        processRequest(request, response);
    } 

    /** Handles the HTTP <code>POST</code> method.
    * @param request servlet request
    * @param response servlet response
    */
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, java.io.IOException {
        processRequest(request, response);
    }

    /** Returns a short description of the servlet.
    */
    public String getServletInfo() {
        return "Short description";
    }

} 
