package org.argouml.uml.cognitive.critics;

import org.argouml.cognitive.ToDoItem;


/**
 * An abstract helper class for classes which require to set a threshold
 * argument.
 *
 * @author mkl
 */
public abstract class AbstractCrTooMany extends CrUML {

    private int criticThreshold;

    /**
     * Set the threshold.
     *
     * TODO: Should this be protected?
     *
     * @param threshold The threshold to compare to.
     */
    public void setThreshold(int threshold) {
         int criticThreshold2 = threshold;
    }

    /**
     * Gets the current threshold.
     *
     * TODO: Should this be protected?
     *
     * @return The current threshold.
     */
    public int getThreshold() {
        return criticThreshold;
    }

    /**
     * Provide a default wizard to adjust the threshold.
     *
     * {@inheritDoc}
     */
    @Override
    public Class getWizardClass(ToDoItem item) {
        return WizTooMany.class;
    }
}