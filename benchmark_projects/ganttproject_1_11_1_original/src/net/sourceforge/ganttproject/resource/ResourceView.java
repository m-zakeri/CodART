/*
 * Created on 21.06.2003
 *
 */
package net.sourceforge.ganttproject.resource;

/**
 * @author dbarashev
 *
 */
public interface ResourceView {
	/**
	 * This method is called whenever new resource appears in the resource manager
	 * @param event Resource event object
	 */
	public void resourceAdded (ResourceEvent event);

	public void resourcesRemoved (ResourceEvent event);
}
