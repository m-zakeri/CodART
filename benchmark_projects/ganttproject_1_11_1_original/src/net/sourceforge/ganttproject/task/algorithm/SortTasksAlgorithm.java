package net.sourceforge.ganttproject.task.algorithm;

import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.time.TimeUnit;

import java.util.List;
import java.util.Collections;
import java.util.Comparator;

/**
 * @author bard
 */
public class SortTasksAlgorithm {
    private Comparator mySortByStartDateComparator = new Comparator() {
        public int compare(Object left, Object right) {
            int result = 0;
            TaskActivity leftTask = (TaskActivity) left;
            TaskActivity rightTask = (TaskActivity) right;
            if (!leftTask.equals(rightTask)) {
                result = leftTask.getStart().compareTo(rightTask.getStart());
                if (result==0) {
                    float longResult = 0;
                    TaskLength leftLength = leftTask.getDuration();
                    TaskLength rightLength = rightTask.getDuration();
                    if (leftLength.getTimeUnit().isConstructedFrom(rightLength.getTimeUnit())) {
                        longResult = leftLength.getLength(rightLength.getTimeUnit()) - rightLength.getLength();
                    }
                    else if (rightLength.getTimeUnit().isConstructedFrom(leftLength.getTimeUnit())) {
                        longResult = leftLength.getLength() - rightLength.getLength(leftLength.getTimeUnit());
                    }
                    else {
                        throw new IllegalArgumentException("Lengths="+leftLength+" and "+rightLength+" are not compatible");
                    }
                    if (longResult!=0) {
                        result = (int)(longResult / Math.abs(longResult));
                    }
                }
            }
            return result;
        }

    };

    public void sortByStartDate(List/*<Task>*/ tasks) {
        Collections.sort(tasks, mySortByStartDateComparator);
    }
}
