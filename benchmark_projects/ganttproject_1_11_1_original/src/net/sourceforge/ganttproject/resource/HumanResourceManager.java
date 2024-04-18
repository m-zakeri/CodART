/*
 * HumanResourceManager.java
 *
 * Created on 27. Mai 2003, 22:13
 */

package net.sourceforge.ganttproject.resource;

import net.sourceforge.ganttproject.roles.Role;

import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 *
 * @author  barmeier
 */
public class HumanResourceManager implements ResourceManager {
    
    private List myViews = new ArrayList();    
    private  ArrayList resources=new ArrayList();
    private  int nextFreeId=0;
    private final Role myDefaultRole;

    public HumanResourceManager(Role defaultRole) {
        myDefaultRole = defaultRole;
    }

    public HumanResource newHumanResource() {
        HumanResource result = new HumanResource();
        result.setRole(myDefaultRole);
        return result;
    }
    
    public ProjectResource create(String name, int i) {
        HumanResource hr=new HumanResource(name,i);
        hr.setRole(myDefaultRole);
        add(hr);
        return (hr);
    }


    public  void add(ProjectResource resource) {
        if (resource.getId() == -1) {
            resource.setId(nextFreeId);
        }
        if (resource.getId() >= nextFreeId) {
            nextFreeId=resource.getId()+1;
        }
        resources.add (resource);
        fireResourceAdded(resource);
    }
    
    public  ProjectResource getById(int id) {
        // Linear search is not really efficent, but we dont have so many resources !?
        ProjectResource pr=null;
        for (int i=0; i<resources.size(); i++)
            if (((ProjectResource) resources.get(i)).getId()==id) {
                pr=(ProjectResource) resources.get(i);
                break;
            }
        return pr;
    }
    
    public  ArrayList getResources() {
        return resources;
    }
    
    public void remove(ProjectResource resource) {
        fireResourcesRemoved (new ProjectResource[] {resource});
        resources.remove(resource);
    }
    
    public void removeById(int id) {
        ProjectResource pr = getById(id);
        if (pr!=null)
            remove(pr);
    }
    
    public void save(OutputStream target) {
    }
    

    public void clear() {
        fireCleanup();
        resources.clear();
    }
    

    public void addView(ResourceView view) {
        myViews.add(view);
    }
    
    private void fireResourceAdded(ProjectResource resource) {
        ResourceEvent e = new ResourceEvent(this, resource);   
    	for (Iterator i = myViews.iterator(); i.hasNext();) {
    		ResourceView nextView = (ResourceView)i.next();
    		nextView.resourceAdded(e);
    	}
    }

    private void fireResourcesRemoved(ProjectResource[] resources) {
        ResourceEvent e = new ResourceEvent(this, resources);
        for (int i=0; i<myViews.size(); i++) {
            ResourceView nextView = (ResourceView)myViews.get(i);
            nextView.resourcesRemoved(e);
        }
    }

    private void fireCleanup() {
        fireResourcesRemoved((ProjectResource[])resources.toArray(new ProjectResource[resources.size()]));
    }
	
	/** Move up the resource number index*/
	public void up(int index) {
		HumanResource human = (HumanResource)resources.remove(index);
		resources.add(index-1, human);
	}
	
	/** Move down the resource number index*/
	public void down(int index) {
		HumanResource human = (HumanResource)resources.remove(index);
		resources.add(index+1, human);

	}

    public void importData(ResourceManager resourceManager) {
        if (resourceManager instanceof HumanResourceManager==false) {
            throw new IllegalArgumentException("I expect resource manager to be HumanResourceManager");
        }
        HumanResourceManager hrManager = (HumanResourceManager) resourceManager;
        List resources = hrManager.getResources();
        for (int i=0; i<resources.size(); i++) {
            HumanResource next = (HumanResource) resources.get(i);
            importData(next);
        }
    }

    private void importData(HumanResource next) {
        HumanResource imported = (HumanResource) create(next.getName(), next.getId());
        imported.setName(next.getName());
        imported.setDescription(next.getDescription());
        imported.setMail(next.getMail());
        imported.setPhone(next.getPhone());
        imported.setRole(next.getRole());
    }
}
