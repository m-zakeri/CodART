package net.sourceforge.ganttproject.task.dependency;

import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.task.dependency.constraint.FinishStartConstraintImpl;

import java.util.*;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 * Date: 14.02.2004
 * Time: 16:02:48
 * To change this template use File | Settings | File Templates.
 */
public class TaskDependencyCollectionImpl implements TaskDependencyCollection {
    private Set myDependencies = new HashSet();
    private SortedMap mySearchKey2dependency = new TreeMap();
    private final EventDispatcher myEventDispatcher;

    public TaskDependencyCollectionImpl(EventDispatcher myEventDispatcher) {
        this.myEventDispatcher = myEventDispatcher;
    }

    public TaskDependency[] getDependencies() {
        return (TaskDependency[]) myDependencies.toArray(new TaskDependency[0]);
    }

    public TaskDependency[] getDependencies(Task task) {
        SearchKey fromKey = new RangeSearchFromKey(task);
        SearchKey toKey = new RangeSearchToKey(task);
        SortedMap submap = mySearchKey2dependency.subMap(fromKey, toKey);
        return (TaskDependency[]) submap.values().toArray(new TaskDependency[0]);
    }

    public TaskDependency[] getDependenciesAsDependant(Task dependant) {
        SearchKey fromKey = new SearchKey(SearchKey.DEPENDANT, dependant.getTaskID(), -1);
        SearchKey toKey = new SearchKey(SearchKey.DEPENDEE, dependant.getTaskID(), -1);
        SortedMap submap = mySearchKey2dependency.subMap(fromKey, toKey);
        return (TaskDependency[]) submap.values().toArray(new TaskDependency[0]);
    }

    public TaskDependency[] getDependenciesAsDependee(Task dependee) {
        SearchKey fromKey = new SearchKey(SearchKey.DEPENDEE, dependee.getTaskID(), -1);
        SearchKey toKey = new SearchKey(Integer.MAX_VALUE, dependee.getTaskID(), -1);
        SortedMap submap = mySearchKey2dependency.subMap(fromKey, toKey);
        return (TaskDependency[]) submap.values().toArray(new TaskDependency[0]);
    }

    public TaskDependency createDependency(Task dependant, Task dependee) throws TaskDependencyException {
        TaskDependency result = auxCreateDependency(dependant, dependee);
        addDependency(result);
        return result;
    }

    public boolean canCreateDependency(Task dependant, Task dependee) {
        if (dependant==dependee) {
            return false;
        }
        return (getTaskHierarchy().areUnrelated(dependant, dependee));
    }
    public void deleteDependency(TaskDependency dependency) {
        delete(dependency);
    }

    public void clear() {
        doClear();
    }

    public TaskDependencyCollectionMutator createMutator() {
        return new MutatorImpl();
    }

    private class MutatorImpl implements TaskDependencyCollectionMutator {
        private Map myQueue = new LinkedHashMap();
        private MutationInfo myCleanupMutation;

        public void commit() {
            List mutations = new ArrayList(myQueue.values());
            if (myCleanupMutation!=null) {
                mutations.add(myCleanupMutation);
            }
            Collections.sort(mutations);
            for (int i=0; i<mutations.size(); i++) {
                MutationInfo next = (MutationInfo) mutations.get(i);
                switch (next.myOperation) {
                    case MutationInfo.ADD:
                        {
                            try {
                                addDependency(next.myDependency);
                            } catch (TaskDependencyException e) {
                                e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
                            }
                            break;
                        }
                    case MutationInfo.DELETE: {
                        delete(next.myDependency);
                        break;
                    }
                    case MutationInfo.CLEAR: {
                        doClear();
                        break;
                    }
                }
            }
        }

        public void clear() {
            myQueue.clear();
            myCleanupMutation = new MutationInfo(null, MutationInfo.CLEAR);
        }

        public TaskDependency createDependency(Task dependant, Task dependee) throws TaskDependencyException {
            TaskDependency result = auxCreateDependency(dependant, dependee);
            myQueue.put(result, new MutationInfo(result, MutationInfo.ADD));
            return result;
        }

        public void deleteDependency(TaskDependency dependency) {
            MutationInfo info = (MutationInfo) myQueue.get(dependency);
            if (info==null) {
                myQueue.put(dependency, new MutationInfo(dependency, MutationInfo.DELETE));
            }
            else if (info.myOperation==MutationInfo.ADD) {
                myQueue.remove(dependency);
            }
        }


    }

    private static class MutationInfo implements Comparable {
        static final int ADD = 0;
        static final int DELETE = 1;
        static final int CLEAR = 2;
        final TaskDependency myDependency;
        final int myOperation;
        final int myOrder = ourOrder++;
        static int ourOrder;

        public MutationInfo(TaskDependency myDependency, int myOperation) {
            this.myDependency = myDependency;
            this.myOperation = myOperation;
        }

        public int compareTo(Object o) {
            MutationInfo rvalue = (MutationInfo) o;
            return myOrder - rvalue.myOrder;
        }
    }
    private TaskDependency auxCreateDependency(Task dependant, Task dependee) {
        TaskDependency result = new TaskDependencyImpl(dependant, dependee, this);
        result.setConstraint(new FinishStartConstraintImpl());
        return result;
    }

    void addDependency(TaskDependency dep) throws TaskDependencyException {
        if (myDependencies.contains(dep)) {
            throw new TaskDependencyException("Dependency="+dep+" already exists");
        }
        myDependencies.add(dep);
        //
        mySearchKey2dependency.put(new SearchKey(SearchKey.DEPENDANT, (TaskDependencyImpl)dep), dep);
        mySearchKey2dependency.put(new SearchKey(SearchKey.DEPENDEE, (TaskDependencyImpl)dep), dep);
        myEventDispatcher.fireDependencyAdded(dep);
    }

    void delete(TaskDependency dep) {
        myDependencies.remove(dep);
        SearchKey key1 = new SearchKey(SearchKey.DEPENDANT, dep.getDependant().getTaskID(), dep.getDependee().getTaskID());
        SearchKey key2 = new SearchKey(SearchKey.DEPENDEE, dep.getDependee().getTaskID(), dep.getDependant().getTaskID());
        mySearchKey2dependency.remove(key1);
        mySearchKey2dependency.remove(key2);
        myEventDispatcher.fireDependencyRemoved(dep);
//        SearchKey fromKey = new RangeSearchFromKey(dep.getDependant());
//        SearchKey toKey = new RangeSearchToKey(dep.getDependant());
//        mySearchKey2dependency.subMap(fromKey, toKey).clear();
//        fromKey = new RangeSearchFromKey(dep.getDependee());
//        toKey = new RangeSearchToKey(dep.getDependee());
//        mySearchKey2dependency.subMap(fromKey, toKey).clear();
    }

    public void doClear() {
        myDependencies.clear();
        mySearchKey2dependency.clear();
    }


    protected TaskContainmentHierarchyFacade getTaskHierarchy() {
        return null;
    }

}
