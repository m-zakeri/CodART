package net.sourceforge.ganttproject.task.algorithm;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyException;

import java.util.*;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public abstract class RecalculateTaskScheduleAlgorithm extends AlgorithmBase {

    private Set myMarkedTasks = new HashSet();
    private SortedMap myDistance2dependencyList = new TreeMap();
    private Set myModifiedTasks = new HashSet();
    private final AdjustTaskBoundsAlgorithm myAdjuster;
    private int myEntranceCounter;
    private boolean isRunning;

    public RecalculateTaskScheduleAlgorithm(AdjustTaskBoundsAlgorithm adjuster) {
        myAdjuster = adjuster;
    }

    public void run(Task changedTask) throws TaskDependencyException {
        if (!isEnabled()) {
            return;
        }
        isRunning = true;
        myEntranceCounter++;
        myMarkedTasks.clear();
        buildDistanceGraph(changedTask);
        fulfilDependencies();
        myDistance2dependencyList.clear();
        myModifiedTasks.add(changedTask);
        myAdjuster.run((Task[])myModifiedTasks.toArray(new Task[0]));
        myDistance2dependencyList.clear();
        myModifiedTasks.clear();
        myEntranceCounter--;
        isRunning = false;
    }

    public void run() throws TaskDependencyException {
        isRunning = true;
        TaskContainmentHierarchyFacade facade = createContainmentFacade();
        Set independentTasks = new HashSet();
        traverse(facade, facade.getRoot(), independentTasks);
        for (Iterator it = independentTasks.iterator(); it.hasNext();) {
            Task next = (Task) it.next();
            buildDistanceGraph(next);
        }
        fulfilDependencies();
        isRunning = false;
    }

    public boolean isRunning() {
        return isRunning;
    }
    private void traverse(TaskContainmentHierarchyFacade facade, Task root, Set independentTasks) {
        TaskDependency[] asDependant = root.getDependenciesAsDependant().toArray();
        if (asDependant.length==0) {
            independentTasks.add(root);
        }
        Task[] nestedTasks = facade.getNestedTasks(root);
        for (int i=0; i<nestedTasks.length; i++) {
            traverse(facade, nestedTasks[i], independentTasks);
        }
    }

    private void fulfilDependencies() throws TaskDependencyException {
        //System.err.println("[RecalculateTaskSchedule] >>>fulfilDependencies()");
        for (Iterator distances = myDistance2dependencyList.entrySet().iterator(); distances.hasNext();) {
            Map.Entry nextEntry = (Map.Entry) distances.next();
            List nextDependenciesList = (List) nextEntry.getValue();
            for (int i=0; i<nextDependenciesList.size(); i++) {
                TaskDependency nextDependency = (TaskDependency) nextDependenciesList.get(i);
                TaskDependencyConstraint nextConstraint = nextDependency.getConstraint();
                TaskDependencyConstraint.Collision collision = nextConstraint.getCollision();
                if (collision.isActive()) {
                    fulfilConstraints(nextDependency);
                }
            }
        }
        //System.err.println("[RecalculateTaskSchedule] <<<fulfilDependencies()");
    }

    private void fulfilConstraints(TaskDependency dependency) throws TaskDependencyException {
        Task dependant = dependency.getDependant();
        TaskDependency[] depsAsDependant = dependant.getDependenciesAsDependant().toArray();
        if (depsAsDependant.length>0) {
            ArrayList startLaterVariations = new ArrayList();
            ArrayList startEarlierVariations = new ArrayList();
            ArrayList noVariations = new ArrayList();
            //
            for (int i=0; i<depsAsDependant.length; i++) {
                TaskDependency next = depsAsDependant[i];
                TaskDependencyConstraint.Collision nextCollision = next.getConstraint().getCollision();
                GanttCalendar acceptableStart = nextCollision.getAcceptableStart();
                switch (nextCollision.getVariation()) {
                    case TaskDependencyConstraint.Collision.START_EARLIER_VARIATION: {
                        startEarlierVariations.add(acceptableStart);
                        break;
                    }
                    case TaskDependencyConstraint.Collision.START_LATER_VARIATION: {
                        startLaterVariations.add(acceptableStart);
                        break;
                    }
                    case TaskDependencyConstraint.Collision.NO_VARIATION: {
                        noVariations.add(acceptableStart);
                        break;
                    }
                }
            }
            if (noVariations.size()>1) {
                throw new TaskDependencyException("Failed to fulfill constraints of task="+dependant+". There are "+noVariations.size()+" constraints which don't allow for task start variation");
            }
            //
            Collections.sort(startEarlierVariations);
            Collections.sort(startLaterVariations);
            //
            GanttCalendar solution;
            GanttCalendar earliestStart = (GanttCalendar) (startEarlierVariations.size()==0 ?
                    null : startEarlierVariations.get(0));
            GanttCalendar latestStart = (GanttCalendar) (startLaterVariations.size()>=0 ?
                    startLaterVariations.get(startLaterVariations.size()-1) : null);
            if (earliestStart==null && latestStart==null) {
                solution = dependant.getStart();
            }
            else {
                if (earliestStart==null && latestStart!=null) {
                    earliestStart = latestStart;
                }
                else if (earliestStart!=null && latestStart==null) {
                    latestStart = earliestStart;
                }
                if (earliestStart.compareTo(latestStart) < 0) {
                    throw new TaskDependencyException("Failed to fulfill constraints of task=" + dependant);
                }
            }
            if (noVariations.size()>0) {
                GanttCalendar notVariableStart = (GanttCalendar) noVariations.get(0);
                if (notVariableStart.compareTo(earliestStart)<0 || notVariableStart.compareTo(latestStart)>0) {
                    throw new TaskDependencyException("Failed to fulfill constraints of task="+dependant);
                }
                solution = notVariableStart;
            }
            else {
                solution = latestStart;
            }
            //
            modifyTaskStart(dependant, solution);
        }
    }

    private void modifyTaskStart(Task task, GanttCalendar newStart) {
        TaskLength duration = task.getDuration();
        task.setStart(newStart);
        task.setDuration(duration);
        myModifiedTasks.add(task);
    }

    private void modifyTaskEnd(Task task, GanttCalendar taskEnd) {
        task.setEnd(taskEnd);
        myModifiedTasks.add(task);
    }


    private void buildDistanceGraph(Task changedTask) {
        TaskDependency[] depsAsDependee = changedTask.getDependenciesAsDependee().toArray();
        buildDistanceGraph(depsAsDependee, 1);
    }

    private void buildDistanceGraph(TaskDependency[] deps, int distance) {
        if (deps.length==0) {
            return;
        }
        Integer key = new Integer(distance);
        List depsList = (List) myDistance2dependencyList.get(key);
        if (depsList==null) {
            depsList = new ArrayList();
            myDistance2dependencyList.put(key, depsList);
        }
        depsList.addAll(Arrays.asList(deps));
        for (int i=0; i<deps.length; i++) {
            Task dependant = deps[i].getDependant();
            TaskDependency[] nextStepDeps = dependant.getDependenciesAsDependee().toArray();
            buildDistanceGraph(nextStepDeps, ++distance);
        }
    }


    /*
    private void forwardScheduling(Task changedTask, TaskContainmentHierarchyFacade containmentFacade) {
        //new Exception().printStackTrace();
        //System.out.println("forword scheduling: "+count++); //for Debug CL
        /////////////////////////////////
        //setAllDependencies();
////Code should be deleted after the depend has been replaced by successors
        ////////////////////////////////
        ArrayList taskNodes = null;//getAllTasks();
        for (int i = 0; i < taskNodes.size(); i++) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) taskNodes.get(i);
            if (node.getChildCount() == 0) { //it is not a mother task
                GanttTask task = (GanttTask) node.getUserObject();
                if (!task.isChecked()) {
                    findEarliestStart(task);
                }
            }
        }
        //Treat the mother task. (the children have been scheduled.)
        //start date of mother task should be the earliest start date of its children
        //finish date of mother task is the last finish date of its children
        for (int i = 0; i < taskNodes.size(); i++) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) taskNodes.get(i);
            if (node.getChildCount() != 0) { //it is a mother task
                if (node.isRoot()) {
                    continue;
                }
                Task task = (Task) node.getUserObject();
                GanttCalendar earliestStartDate = new GanttCalendar(2949, 10, 1);
                GanttCalendar earliestFinishDate = new GanttCalendar(1049, 10, 1);
                //find the earliest date of children's start dates
                //find the last finish date of children's finish dates
                Enumeration childNodes = node.children();
                while (childNodes.hasMoreElements()) {
                    Task childTask = (Task) ((DefaultMutableTreeNode)
                            childNodes.nextElement()).
                            getUserObject();
                    if (earliestStartDate.compareTo(childTask.getStart()) > 0) {
                        earliestStartDate = childTask.getStart().Clone();
                    }
                    if (earliestFinishDate.compareTo(childTask.getEnd()) < 0) {
                        earliestFinishDate = childTask.getEnd().Clone();
                    }
                }
                task.setStart(earliestStartDate);
                task.setEnd(earliestFinishDate);
            }
        }
    }

    //static int countFindEarliestStart=0;//for Debug CL
    private void findEarliestStart(Task task) {
        //System.out.println("I m in findEarliestStart for "+countFindEarliestStart++);//for Debug CL

        GanttCalendar earliestStart = new GanttCalendar(1099, 10, 1); //set the earliest start date to be some date impossible. at least where I don't care:)
        if (!isMarked(task)) {
            TaskDependency[] asDependant = task.getDependenciesAsDependant().toArray();
            //for the task without predecessor, the start date is the earliest start date
            if (asDependant.length==0) {
                markTask(task);
                return;
            }

            //If there are predecessors, the earliest date should be depended
            //on the relationship type and start or end date of each predecessor.
            for (int i = 0; i < asDependant.length; i++) {
                Task predecessorTask = asDependant[i].getDependee();
                int relationshipType = ((GanttTaskRelationship) predecessors.get(i)).getRelationshipType();
                if (relationshipType == GanttTaskRelationship.FS) {
                    ////////////////////////////////////
                    //FS realtionship: the earliest start date should be the
                    //latest earliest finish date of all the predecessors
                    ////////////////////////////////////
                    if (!predecessorTask.isChecked()) { //If ther predecessor has not been checked, check it here. It is a recursive algorithm
                        findEarliestStart(predecessorTask);
                    }
                    if (predecessorTask.isChecked()) { //if checked, the start and end date are valid
                        GanttCalendar temp = predecessorTask.getEnd().Clone();
                        //temp.add(1); //should be one day behind the predecessor finish date.
                        if (temp.compareTo(earliestStart) > 0) { //if the current earliest start is earlier than the end date of one of its prodecessor, it set equal to the end date of this predecessor
                            earliestStart = temp;
                        }
                    }
                } else if (relationshipType == GanttTaskRelationship.FF) {
                    ////////////////////////////////////
                    //FF realtionship: As soon as the predecessor task finishes,
                    //the successor task can finish
                    ////////////////////////////////////
                    if (!predecessorTask.isChecked()) {
                        findEarliestStart(predecessorTask); //check the predecessor
                    }
                    if (predecessorTask.isChecked()) {
                        GanttCalendar temp = predecessorTask.getEnd().Clone();
                        GanttCalendar earliestFinish = earliestStart;
                        earliestFinish.add(task.getLength());
                        if (earliestFinish.compareTo(temp) < 0) { //if the earliest finish is earlier than the end date of its predecessor, it set equal to the end date of predecessor
                            earliestFinish = temp.Clone();
                            earliestStart = earliestFinish.Clone();
                            earliestStart.add(-task.getLength());
                        } else { //do nothing, if it is behind end date of predecessor

                        }
                    }
                } else if (relationshipType == GanttTaskRelationship.SF) {
                    ////////////////////////////////////
                    //SF realtionship: As soon as the predecessor task starts,
                    //the successor task can finish.
                    ////////////////////////////////////
                    if (!predecessorTask.isChecked()) {
                        findEarliestStart(predecessorTask); //if the predecessor has not been checked, check it here. it is a recursive algorithm
                    }
                    if (predecessorTask.isChecked()) {
                        GanttCalendar temp = predecessorTask.getStart().Clone();
                        GanttCalendar earliestFinish = earliestStart;
                        earliestFinish.add(task.getLength());

                        if (earliestFinish.compareTo(temp) < 0) { //if the earliest finish of the task is earlier than the start date of one of its predecessors, it set equal to the start date of the predecessor
                            earliestFinish = temp.Clone();
                            earliestStart = earliestFinish.Clone();
                            earliestStart.add(-task.getLength());
                        } else { //already satisfied the SF relationship, do nothing

                        }
                    }
                } else if (relationshipType == GanttTaskRelationship.SS) {
                    ////////////////////////////////////
                    //SS realtionship: As soon as the predecessor task starts,
                    //the successor task can start.
                    ////////////////////////////////////
                    if (!predecessorTask.isChecked()) {
                        findEarliestStart(predecessorTask); //if the predecessor has not been checked, check it here. it is a recursive algorithm
                    }
                    if (predecessorTask.isChecked()) {
                        GanttCalendar temp = predecessorTask.getStart().Clone();

                        if (earliestStart.compareTo(temp) < 0) { // if the start date of the task is earlier than the start date of its predecessor, it set equal to the start date of predecessor
                            earliestStart = temp.Clone();
                        } else { //already satisfied the SS relationship, do nothing.

                        }
                    }
                }
            }
            if (earliestStart.compareTo(task.getStart()) < 0) { //if the actual start is behind earliest start, don't need to do anything

            } else {
                task.setStart(earliestStart);
                GanttCalendar temp = earliestStart.Clone();
                temp.add(task.getLength());
                task.setEnd(temp);
            }
            task.setChecked(true);
        }
        return;
    }
    */
    private void markTask(Task task) {
        myMarkedTasks.add(task);
    }


    private boolean isMarked(Task task) {
        return myMarkedTasks.contains(task);
    }

    protected abstract TaskContainmentHierarchyFacade createContainmentFacade();
}
