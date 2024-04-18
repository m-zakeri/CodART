package net.sourceforge.ganttproject.task;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.calendar.AlwaysWorkingTimeCalendarImpl;
import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.calendar.GPCalendarActivity;
import net.sourceforge.ganttproject.shape.ShapePaint;
import net.sourceforge.ganttproject.shape.ShapeConstants;
import net.sourceforge.ganttproject.task.dependency.*;
import net.sourceforge.ganttproject.task.hierarchy.TaskHierarchyItem;
import net.sourceforge.ganttproject.time.TimeUnit;
//import net.sourceforge.ganttproject.resource.ProjectResource;

import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.awt.*;

/**
 * Created by IntelliJ IDEA.
 * 
 * @author bard Date: 31.01.2004
 */
public class TaskImpl implements Task {
    private int myID;

    private final TaskManagerImpl myManager;

    private String myName;

    private String myWebLink = new String("http://");

    private boolean isMilestone;

    private int myPriority;

    private GanttCalendar myStart;

    private GanttCalendar myEnd;

    private int myCompletionPercentage;

    private TaskLength myLength;

    private List myActivities = new ArrayList();

    private boolean isStartFixed;

    private boolean bExpand;

    //private final TaskDependencyCollection myDependencies = new
    // TaskDependencyCollectionImpl();
    private ResourceAssignmentCollectionImpl myAssignments;

    private TaskDependencySlice myDependencySlice;

    private TaskDependencySlice myDependencySliceAsDependant;

    private TaskDependencySlice myDependencySliceAsDependee;

    private boolean myEventsEnabled;

    private final TaskHierarchyItem myTaskHierarchyItem;

    private ShapePaint myShape;

    private Color myColor;

    private String myNotes;

    private MutatorImpl myMutator;

    protected TaskImpl(TaskManager taskManager, int taskID) {
        myManager = (TaskManagerImpl) taskManager;
        if (taskID == -1) {
            myID = myManager.getMaxID();
            myManager.increaseMaxID();
        } else {
            if (myManager.getTask(taskID) != null) {
                throw new IllegalArgumentException("There is a task with ID=" + taskID + " already");
            }
            myID = taskID;

        }
        myAssignments = new ResourceAssignmentCollectionImpl(this, myManager.getConfig().getResourceManager());
        myDependencySlice = new TaskDependencySliceImpl(this, myManager.getDependencyCollection());
        myDependencySliceAsDependant = new TaskDependencySliceAsDependant(this, myManager.getDependencyCollection());
        myDependencySliceAsDependee = new TaskDependencySliceAsDependee(this, myManager.getDependencyCollection());
        myPriority = 1;
        myTaskHierarchyItem = myManager.getHierarchyManager().createItem(this);
        isStartFixed = false;
        myNotes = "";
        bExpand = true;
        myColor = null;
    }

    protected TaskImpl(TaskImpl copy, boolean isUnplugged) {
        myManager = copy.myManager;
        if (!isUnplugged) {
            myTaskHierarchyItem = myManager.getHierarchyManager().createItem(this);
        } else {
            myTaskHierarchyItem = null;
        }
        importData(copy);
    }

    protected void importData(TaskImpl copy) {
        myAssignments = new ResourceAssignmentCollectionImpl(this, myManager.getConfig().getResourceManager());
        myAssignments.importData(copy.getAssignmentCollection());
        myID = copy.myID;
        myName = copy.myName;
        myWebLink = copy.myWebLink;
        isMilestone = copy.isMilestone;
        myPriority = copy.myPriority;
        myStart = copy.myStart;
        myEnd = copy.myEnd;
        myCompletionPercentage = copy.myCompletionPercentage;
        myLength = copy.myLength;
        isStartFixed = copy.isStartFixed;
        myShape = copy.myShape;
        myColor = copy.myColor;
        myNotes = copy.myNotes;
        bExpand = copy.bExpand;
        //
        myDependencySlice = new TaskDependencySliceImpl(this, myManager.getDependencyCollection());
        myDependencySliceAsDependant = new TaskDependencySliceAsDependant(this, myManager.getDependencyCollection());
        myDependencySliceAsDependee = new TaskDependencySliceAsDependee(this, myManager.getDependencyCollection());
        recalculateActivities();
    }

    public Task unpluggedClone() {
        TaskImpl result = new TaskImpl(this, true);
        return result;
    }

    public TaskMutator createMutator() {
        if (myMutator != null) {
            throw new RuntimeException("Two mutators have been requested", myException);
        }
        myMutator = new MutatorImpl();
        myException = new Exception();
        return myMutator;
    }

    private Exception myException;

    // main properties
    public int getTaskID() {
        return myID;
    }

    public String getName() {
        return myName;
    }

    public String getWebLink() {
        return myWebLink;
    }

    public boolean isMilestone() {
        return isMilestone;
    }

    public int getPriority() {
        return myPriority;
    }

    public GanttCalendar getStart() {
        return myMutator == null
            ? myStart
            : myMutator.getStart();
    }

    public GanttCalendar getEnd() {
        if (myMutator == null) {
            if (myEnd == null) {
                myEnd = getStart().Clone();
                myEnd.add((int) getDuration().getLength());
            }
            return myEnd;
        } else {
            return myMutator.getEnd();
        }
    }

    public TaskActivity[] getActivities() {
        List activities = myMutator == null
            ? null
            : myMutator.getActivities();
        if (activities == null) {
            activities = myActivities;
        }
        return (TaskActivity[]) activities.toArray(new TaskActivity[activities.size()]);
    }

    public TaskLength getDuration() {
        return myMutator == null
            ? myLength
            : myMutator.getDuration();
    }

    public int getCompletionPercentage() {
        return myMutator == null
            ? myCompletionPercentage
            : myMutator.getCompletionPercentage();
    }

    public boolean isStartFixed() {
        return isStartFixed;
    }

    public boolean getExpand() {
        return bExpand;
    }

    public ShapePaint getShape() {
        //if (myShape==null) {
        //    myShape = new ShapePaint(ShapeConstants.BACKSLASH, getColor() ,
        // getColor());
        //}
        return myShape;
    }

    public Color getColor() {
        Color result = myColor;
        if (result == null) {
            if (isMilestone() || getNestedTasks().length > 0) {
                result = Color.BLACK;
            } else {
                result = myManager.getConfig().getDefaultColor();
            }
        }
        return result;
    }

    public String getNotes() {
        return myNotes;
    }

    public GanttTaskRelationship[] getPredecessors() {
        return new GanttTaskRelationship[0]; //To change body of implemented
                                             // methods use Options | File
                                             // Templates.
    }

    public GanttTaskRelationship[] getSuccessors() {
        return new GanttTaskRelationship[0]; //To change body of implemented
                                             // methods use Options | File
                                             // Templates.
    }

    public ResourceAssignment[] getAssignments() {
        return myAssignments.getAssignments();
    }

    public ResourceAssignmentCollection getAssignmentCollection() {
        return myAssignments;
    }

    //
    public Task getSupertask() {
        TaskHierarchyItem container = myTaskHierarchyItem.getContainerItem();
        return container.getTask();
    }

    public Task[] getNestedTasks() {
        TaskHierarchyItem[] nestedItems = myTaskHierarchyItem.getNestedItems();
        Task[] result = new Task[nestedItems.length];
        for (int i = 0; i < nestedItems.length; i++) {
            result[i] = nestedItems[i].getTask();
        }
        return result;
    }

    public void move(Task targetSupertask) {
        TaskImpl supertaskImpl = (TaskImpl) targetSupertask;
        TaskHierarchyItem targetItem = supertaskImpl.myTaskHierarchyItem;
        myTaskHierarchyItem.delete();
        targetItem.addNestedItem(myTaskHierarchyItem);
    }

    public void delete() {
        getDependencies().clear();
        getAssignmentCollection().clear();
    }
    public TaskDependencySlice getDependencies() {
        return myDependencySlice;
    }

    public TaskDependencySlice getDependenciesAsDependant() {
        return myDependencySliceAsDependant;
    }

    public TaskDependencySlice getDependenciesAsDependee() {
        return myDependencySliceAsDependee;
    }

    public TaskManager getManager() {
        return myManager;
    }

    //TODO: remove this hack. ID must never be changed
    protected void setTaskIDHack(int taskID) {
        myID = taskID;
    }

    private static interface EventSender {
        void enable();

        void fireEvent();
    }

    private class ProgressEventSender implements EventSender {
        private boolean myEnabled;

        public void fireEvent() {
            if (myEnabled) {
                myManager.fireTaskProgressChanged(TaskImpl.this);
            }
            myEnabled = false;
        }

        public void enable() {
            myEnabled = true;
        }

    }

    private class PropertiesEventSender implements EventSender {
        private boolean myEnabled;

        public void fireEvent() {
            if (myEnabled) {
                myManager.fireTaskPropertiesChanged(TaskImpl.this);
            }
            myEnabled = false;
        }

        public void enable() {
            myEnabled = true;
        }
    }

    private static class FieldChange {
        String myFieldName;

        Object myFieldValue;

        EventSender myEventSender;

        void setValue(Object newValue) {
            myFieldValue = newValue;
            myEventSender.enable();
        }
    }

    private static class DurationChange extends FieldChange {
        Date getCachedDate(int length) {
            if (myDates == null) {
                return null;
            }
            int index = length - myMinLength;
            if (index < 0 || index >= myDates.size()) {
                return null;
            }
            return (Date) myDates.get(index);
        }

        void cacheDate(Date date, int length) {
            if (myDates == null) {
                myDates = new ArrayList();
            }
            int index = length - myMinLength;
            while (index <= -1) {
                myDates.add(0, null);
                index++;
            }
            while (index > myDates.size()) {
                myDates.add(null);
            }
            if (index == -1) {
                myDates.add(0, date);
            } else if (index == myDates.size()) {
                myDates.add(date);
            } else {
                myDates.set(index, date);
            }
        }

        private int myMinLength = 0;

        private List myDates;

    }

    private class MutatorImpl implements TaskMutator {
        private EventSender myPropertiesEventSender = new PropertiesEventSender();

        private EventSender myProgressEventSender = new ProgressEventSender();

        private FieldChange myCompletionPercentageChange;

        private FieldChange myStartChange;

        private FieldChange myEndChange;

        private DurationChange myDurationChange;

        private List myActivities;

        private final List myCommands = new ArrayList();

        public void commit() {
            try {
                boolean fireChanges = false;
                if (myStartChange != null) {
                    GanttCalendar start = getStart();
                    TaskImpl.this.setStart(start);
                }
                if (myDurationChange != null) {
                    TaskLength duration = getDuration();
                    TaskImpl.this.setDuration(duration);
                    myEndChange = null;
                }
                if (myCompletionPercentageChange != null) {
                    int newValue = getCompletionPercentage();
                    TaskImpl.this.setCompletionPercentage(newValue);
                }
                if (myEndChange != null) {
                    GanttCalendar end = getEnd();
                    TaskImpl.this.setEnd(end);
                }

                for (int i = 0; i < myCommands.size(); i++) {
                    Runnable next = (Runnable) myCommands.get(i);
                    next.run();
                }
                myCommands.clear();
                myPropertiesEventSender.fireEvent();
                myProgressEventSender.fireEvent();
            } finally {
                TaskImpl.this.myMutator = null;
            }
        }

        public List getActivities() {
            if (myActivities == null && (myStartChange != null) || (myDurationChange != null)) {
                myActivities = new ArrayList();
                TaskImpl.this.recalculateActivities(myActivities, getStart().getTime(), getEnd().getTime());
            }
            return myActivities;
        }

        public void setName(final String name) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setName(name);
                }
            });
        }

        public void setMilestone(final boolean milestone) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setMilestone(milestone);
                }
            });
        }

        public void setPriority(final int priority) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setPriority(priority);
                }
            });
        }

        
        public void shift(TaskLength shift) {
            TaskImpl.this.shift(shift);
        }

        public void setStart(final GanttCalendar start) {
            if (myStartChange == null) {
                myStartChange = new FieldChange();
                myStartChange.myEventSender = myPropertiesEventSender;
            }
            myStartChange.setValue(start);
            myActivities = null;
        }

        public void setEnd(final GanttCalendar end) {
            if (myEndChange == null) {
                myEndChange = new FieldChange();
                myEndChange.myEventSender = myPropertiesEventSender;
            }
            myEndChange.setValue(end);
            myActivities = null;
        }

        public void setDuration(final TaskLength length) {
            if (myDurationChange == null) {
                myDurationChange = new DurationChange();
                myDurationChange.myEventSender = myPropertiesEventSender;
                myDurationChange.setValue(length);
            } else {
                TaskLength currentLength = (TaskLength) myDurationChange.myFieldValue;
                if (currentLength.getLength() - length.getLength() == 0) {
                    return;
                }
            }
            TaskLength prevLength = (TaskLength) myDurationChange.myFieldValue;
            //System.err.println("new duration="+length+"
            // previous="+prevLength);
            //Date prevEnd =
            // myDurationChange.getCachedDate((int)prevLength.getLength());
            Date prevEnd = null;
            //System.err.println("previously cached shift="+prevEnd);
            myDurationChange.setValue(length);
            GanttCalendar newEnd;
            Date shifted;
            if (prevEnd == null) {
                //System.err.println("no prev, length="+length.getLength());
                shifted = TaskImpl.this.shiftDate(getStart().getTime(), length.getTimeUnit(), length.getLength());
            } else {
                //System.err.println("yes prev,
                // length="+(length.getLength()-prevLength.getLength()));
                shifted = TaskImpl.this.shiftDate(prevEnd, length.getTimeUnit(), length.getLength()
                        - prevLength.getLength());
            }
            //System.err.println("caching shift="+shifted+" for
            // duration="+length);
            //myDurationChange.cacheDate(shifted, (int)length.getLength());
            newEnd = new GanttCalendar(shifted);
            setEnd(newEnd);
            myActivities = null;
        }

        public void setExpand(final boolean expand) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setExpand(expand);
                }
            });
        }

        public void setCompletionPercentage(final int percentage) {
            if (myCompletionPercentageChange == null) {
                myCompletionPercentageChange = new FieldChange();
                myCompletionPercentageChange.myEventSender = myProgressEventSender;
            }
            myCompletionPercentageChange.setValue(new Integer(percentage));
        }

        public void setStartFixed(final boolean isFixed) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setStartFixed(isFixed);
                }
            });
        }

        public void setShape(final ShapePaint shape) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setShape(shape);
                }
            });
        }

        public void setColor(final Color color) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setColor(color);
                }
            });
        }

        public void setNotes(final String notes) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.setNotes(notes);
                }
            });
        }

        public void addNotes(final String notes) {
            myCommands.add(new Runnable() {
                public void run() {
                    TaskImpl.this.addNotes(notes);
                }
            });
        }

        public int getCompletionPercentage() {
            return myCompletionPercentageChange == null
                ? TaskImpl.this.myCompletionPercentage
                : ((Integer) myCompletionPercentageChange.myFieldValue).intValue();
        }

        GanttCalendar getStart() {
            return myStartChange == null
                ? TaskImpl.this.myStart
                : (GanttCalendar) myStartChange.myFieldValue;
        }

        GanttCalendar getEnd() {
            return myEndChange == null
                ? TaskImpl.this.myEnd
                : (GanttCalendar) myEndChange.myFieldValue;
        }

        TaskLength getDuration() {
            return myDurationChange == null
                ? TaskImpl.this.myLength
                : (TaskLength) myDurationChange.myFieldValue;
        }

        public void shift(float unitCount) {

            Task result = getPrecomputedShift(unitCount);
            if (result == null) {
                result = TaskImpl.this.shift(unitCount);
                cachePrecomputedShift(result, unitCount);
            }
            //System.err.println("[MutatorImpl] shift(): result="+result);
            setStart(result.getStart());
            setDuration(result.getDuration());
            setEnd(result.getEnd());
        }

        private void cachePrecomputedShift(Task result, float unitCount) {
        }

        private Task getPrecomputedShift(float unitCount) {
            return null;
        }

    }

    public void setName(String name) {

        myName = name;
    }

    public void setWebLink(String webLink) {

        myWebLink = webLink;
    }

    public void setMilestone(boolean milestone) {
        isMilestone = milestone;
    }

    public void setPriority(int priority) {
        myPriority = priority;
    }

    public void setStart(GanttCalendar start) {
        Date closestWorkingStart = myManager.findClosestWorkingTime(start.getTime());
        start.setTime(closestWorkingStart);
        GanttCalendar oldStart = myStart == null
            ? null
            : myStart.Clone();
        myStart = start;
        if (areEventsEnabled()) {
            myManager.fireTaskScheduleChanged(this, oldStart, getEnd());
        }
        recalculateActivities();
    }

    public void setEnd(GanttCalendar end) {
        GanttCalendar oldFinish = myEnd == null
            ? null
            : myEnd.Clone();
        myEnd = end;
        recalculateActivities();
        //System.err.println("we have "+myActivities.size()+" activities");
        if (areEventsEnabled()) {
            myManager.fireTaskScheduleChanged(this, myStart.Clone(), oldFinish);
        }
    }

    public void shift(TaskLength shift) {
        float unitCount = shift.getLength(myLength.getTimeUnit());
        if (unitCount!=0f) {
            Task resultTask = shift(unitCount);
            GanttCalendar oldStart = myStart;
            GanttCalendar oldEnd = myEnd;
            myStart = resultTask.getStart();
            myLength = resultTask.getDuration();
            myEnd = resultTask.getEnd();
            if (areEventsEnabled()) {
                myManager.fireTaskScheduleChanged(this, oldStart, oldEnd);
            }
            recalculateActivities();
        }
    }
    
    public Task shift(float unitCount) {
        Task clone = unpluggedClone();
        if (unitCount > 0) {
            TaskLength length = myManager.createLength(myLength.getTimeUnit(), unitCount);
            //clone.setDuration(length);
            Date shiftedDate = shiftDate(myStart.getTime(), length.getTimeUnit(), length.getLength(), RESTLESS_CALENDAR);
            clone.setStart(new GanttCalendar(shiftedDate));
            clone.setDuration(myLength);
        } else {
            //TODO: hack assuming unit=day
            //clone.setStart(clone.getStart().newAdd((int)unitCount));
            Date newStart = shiftDate(clone.getStart().getTime(), clone.getDuration().getTimeUnit(), (long) unitCount);
            clone.setStart(new GanttCalendar(newStart));
            clone.setDuration(myLength);
        }
        return clone;
    }

    public void setDuration(TaskLength length) {
        GanttCalendar oldFinish = myEnd == null
            ? null
            : myEnd.Clone();
        myLength = length;
        Date newEndDate = shiftDate(myStart.getTime(), length.getTimeUnit(), length.getLength());
        myEnd = new GanttCalendar(newEndDate);
        //        myEnd = myStart.newAdd((int) length.getLength());
        recalculateActivities();
        if (areEventsEnabled()) {
            myManager.fireTaskScheduleChanged(this, myStart.Clone(), oldFinish);
        }
    }

    private Date shiftDate(Date input, TimeUnit timeUnit, long length) {
        return shiftDate(input, timeUnit, length, myManager.getConfig().getCalendar());
    }
    
    private Date shiftDate(Date input, TimeUnit timeUnit, long length, GPCalendar calendar) {
        List activities = calendar.getActivities(input, timeUnit, length);
        if (activities.isEmpty()) {
            throw new RuntimeException("Can't set length=" + length + " start=" + input);
        }
        Date result;
        if (length >= 0) {
            GPCalendarActivity lastActivity = (GPCalendarActivity) activities.get(activities.size() - 1);
            result = lastActivity.getEnd();
        } else {
            GPCalendarActivity firstActivity = (GPCalendarActivity) activities.get(0);
            result = firstActivity.getStart();
        }
        return result;
        
    }

    public TaskLength translateDuration(TaskLength duration) {
        return myManager.createLength(myLength.getTimeUnit(), translateDurationValue(duration));
    }

    private float translateDurationValue(TaskLength duration) {
        if (myLength.getTimeUnit().equals(duration.getTimeUnit())) {
            return duration.getValue();
        }
        if (myLength.getTimeUnit().isConstructedFrom(duration.getTimeUnit())) {
            return duration.getValue() / myLength.getTimeUnit().getAtomCount(duration.getTimeUnit());
        }
        if (duration.getTimeUnit().isConstructedFrom(myLength.getTimeUnit())) {
            return duration.getValue() * duration.getTimeUnit().getAtomCount(myLength.getTimeUnit());
        }
        throw new RuntimeException("Can't transalte duration=" + duration + " into units=" + myLength.getTimeUnit());
    }

    private void recalculateActivities() {
        if (myEnd == null || myManager == null) {
            return;
        }
        recalculateActivities(myActivities, myStart.getTime(), myEnd.getTime());
        int length = 0;
        for (int i = 0; i < myActivities.size(); i++) {
            TaskActivity next = (TaskActivity) myActivities.get(i);
            if (next.getIntensity() > 0) {
                length += next.getDuration().getLength(getDuration().getTimeUnit());
            }
        }
        myLength = getManager().createLength(myLength.getTimeUnit(), length);
    }

    private void recalculateActivities(List output, Date startDate, Date endDate) {
        GPCalendar calendar = myManager.getConfig().getCalendar();
        List activities = calendar.getActivities(startDate, endDate);
        output.clear();
        for (int i = 0; i < activities.size(); i++) {
            GPCalendarActivity nextCalendarActivity = (GPCalendarActivity) activities.get(i);
            TaskActivityImpl nextTaskActivity;
            if (nextCalendarActivity.isWorkingTime()) {
                nextTaskActivity = new TaskActivityImpl(this, nextCalendarActivity.getStart(), nextCalendarActivity
                        .getEnd());
            } else if (i > 0 && i + 1 < activities.size()) {
                nextTaskActivity = new TaskActivityImpl(this, nextCalendarActivity.getStart(), nextCalendarActivity
                        .getEnd(), 0);
            } else {
                continue;
            }
            output.add(nextTaskActivity);
        }
    }

    public void setCompletionPercentage(int percentage) {
        myCompletionPercentage = percentage;
    }

    public void setStartFixed(boolean isFixed) {
        isStartFixed = isFixed;
    }

    public void setShape(ShapePaint shape) {
        myShape = shape;
    }

    public void setColor(Color color) {
        myColor = color;
    }

    public void setNotes(String notes) {
        myNotes = notes;
    }

    public void setExpand(boolean expand) {
        bExpand = expand;
    }

    public void addNotes(String notes) {
        myNotes += notes;
    }

    protected void enableEvents(boolean enabled) {
        myEventsEnabled = enabled;
    }

    protected boolean areEventsEnabled() {
        return myEventsEnabled;
    }

    /**
     * Allows to determine, if a special shape is defined for this task.
     * 
     * @return true, if this task has its own shape defined.
     */
    public boolean shapeDefined() {
        return (myShape != null);
    }

    /**
     * Allows to determine, if a special color is defined for this task.
     * 
     * @return true, if this task has its own color defined.
     */

    public boolean colorDefined() {

        return (myColor != null);

    }

    public String toString() {
        return myName + ": " + myStart.getTime() + "-" + myLength;
    }

    public boolean isUnplugged() {
        return myTaskHierarchyItem == null;
    }
    
    private static final GPCalendar RESTLESS_CALENDAR = new AlwaysWorkingTimeCalendarImpl();
}